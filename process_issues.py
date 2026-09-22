#!/usr/bin/env python3
"""Owner-only public forecast intake plus reconciliation of still-open issues.

Issue content remains data. Success is acknowledged only after git push succeeds.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from intake import extract
from registration import register
from schema import ms, prepare, validate
from storage import atomic_json, canonical, read_json


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def comment(number, message):
    with tempfile.NamedTemporaryFile(mode='w',suffix='.md') as fh:
        fh.write(message)
        fh.flush()
        gh('issue','comment',str(number),'--body-file',fh.name)


def process(issue, base, owner, now):
    login = (issue.get('author') or issue.get('user') or {}).get('login')
    if login != owner or not issue.get('title','').lower().startswith('forecast'):
        return
    number = int(issue['number'])
    receipt_path = base/'state/intake_receipts.json'
    receipts = read_json(receipt_path,{})
    body = issue.get('body') or ''
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    old = receipts.get(str(number))
    if old and old['body_sha256'] == body_hash:
        if old['status'] == 'registered':
            # A previous run may have pushed successfully and failed before commenting/closing.
            entry = read_json(base/'state/forecast_manifest.json',{}).get(old['forecast_id'])
            if not entry or entry['sha256'] != old['forecast_sha256']:
                raise ValueError('intake receipt does not match frozen registration')
            subprocess.run(['bash','scripts/commit_push.sh','registry','state'],cwd=base,check=True)
            comment(number, f"Registered `{old['forecast_id']}` at {old['registered_utc']}. Forecast SHA-256: `{old['forecast_sha256']}`.")
            gh('issue','close',str(number))
        return
    try:
        fc = prepare(extract(body),now)
        errors = validate(fc,now)
    except Exception as exc:
        errors = [str(exc)]
    if not errors:
        target = base/'registry'/f"{fc['id']}.json"
        if target.exists() or fc['id'] in read_json(base/'state/forecast_manifest.json',{}):
            errors = ['forecast ID already exists; use a new ID']
    if errors:
        # Comment first: if persistence fails, retry may duplicate a comment, never a score.
        comment(number,'Not registered:\n- '+'\n- '.join(errors)+'\n\nEdit this issue to retry. Its contents are public.')
        receipts[str(number)] = {'body_sha256':body_hash,'status':'invalid'}
        atomic_json(receipt_path,receipts)
        subprocess.run(['bash','scripts/commit_push.sh','state'],cwd=base,check=True)
        return
    atomic_json(target,fc)
    _, registration_errors = register(base,now)
    entry = read_json(base/'state/forecast_manifest.json',{}).get(fc['id'])
    if not entry or entry['registered'] >= ms(fc['start_utc']):
        raise ValueError('registration failed or missed start: '+'; '.join(registration_errors))
    registered_utc = dt.datetime.fromtimestamp(entry['registered']/1000,dt.timezone.utc).isoformat()
    receipts[str(number)] = {'body_sha256':body_hash,'status':'registered','forecast_id':fc['id'],
                             'forecast_sha256':entry['sha256'],'registered_utc':registered_utc}
    atomic_json(receipt_path,receipts)
    subprocess.run(['bash','scripts/commit_push.sh','registry','state'],cwd=base,check=True)
    comment(number,f"Registered `{fc['id']}` at {registered_utc}. Forecast SHA-256: `{entry['sha256']}`. Saved to the repository.")
    gh('issue','close',str(number))


def main():
    base = Path(__file__).resolve().parent
    owner = os.environ['GITHUB_REPOSITORY_OWNER']
    event = read_json(os.environ.get('GITHUB_EVENT_PATH',''),{})
    number = os.environ.get('INPUT_ISSUE_NUMBER','').strip()
    if 'issue' in event:
        # Read current issue state; queued edited events may contain an obsolete body.
        issues = [json.loads(gh('issue','view',str(event['issue']['number']),'--json','number,title,body,author,state'))]
    elif number:
        if not number.isdigit():
            raise ValueError('issue_number must be numeric')
        issues = [json.loads(gh('issue','view',number,'--json','number,title,body,author,state'))]
    else:
        # Paginate all open issues so missed events cannot fall outside a fixed limit.
        pages = json.loads(gh('api','--paginate','--slurp',f'repos/{os.environ["GITHUB_REPOSITORY"]}/issues?state=open&per_page=100'))
        issues = [issue for page in pages for issue in page if 'pull_request' not in issue]
    for issue in issues:
        if issue.get('state','open').lower() == 'open':
            process(issue,base,owner,int(time.time()*1000))


if __name__ == '__main__':
    main()
