"""Immediate, bounded selected-contract books; separate diagnostics, never original quote eligibility."""
import json
from pathlib import Path
import time

from desk import stream_util as U
from research_tools.options_pilot import study as P
from research_tools.options_30d import study as M
from research_tools.market_studies.network import fetch
from options_pilot_report import distribution

DIRECTORY = 'options/selected_contract_books'


def selection(cap):
    original, maturity = P.compare(cap), M.compare(cap)
    return {'candidates': {'original': original['candidates'], 'maturity': maturity['candidates']},
            'horizons': {**original['horizons'], '30-maturity': maturity['horizons']['30']}}


def capture(cap, get=fetch, clock=U.clock_ms):
    selected = selection(cap)
    selected_ms = clock()
    # Bound the union to the original 16-contract, four-worker, 60-second book budget.
    book = P.books(selected, cap['observed_at'], get=get, clock=clock)
    return {'schema': 'immediate-selected-books/1', 't': cap['t'], 'source': cap,
            'source_sha256': U.sha(cap), 'selected_ms': selected_ms, 'selection': selected,
            'books': book, 'completed_ms': clock(),
            'interpretation': 'Separate later book measurement; not size evidence at the source quote clock.'}


def collect(C):
    # Read the exact durably written capture rather than manufacturing an observed_at clock.
    source = Path(C.BASE) / 'data/options/deribit_btc_quotes' / (C.day(C.NOW) + '.jsonl')
    caps = [json.loads(line) for line in source.read_text().splitlines()]
    cap = next((c for c in reversed(caps) if c['t'] == C.NOW), None)
    if cap is None:
        return {'state': 'no-new-source'}
    stops = [getattr(C, name, None) for name in ('DEADLINE', 'STAGE_DEADLINE', 'SOURCE_DEADLINE')]
    if any(stop is not None and stop - time.monotonic() < 65 for stop in stops):
        row = {'schema': 'immediate-selected-books/1', 't': cap['t'], 'state': 'budget-skipped',
               'source_ms': cap['observed_at'], 'source_sha256': U.sha(cap)}
    else:
        row = capture(cap)
    C.append_rows(DIRECTORY, [row], partition=C.day)
    return {'state': row.get('state', row.get('books', {}).get('state')), 'source_ms': cap['observed_at']}


def report(base, now):
    from replay_precision import matches
    records, expected, attempted, usable, lags, states = 0, 0, 0, 0, [], {}
    sources = {}
    for path in sorted((Path(base) / 'data/options/deribit_btc_quotes').glob('*.jsonl')):
        for line in path.read_text().splitlines():
            cap = json.loads(line)
            if now - 86400000 <= cap['observed_at'] <= now:
                sources[U.sha(cap)] = cap
    seen = set()
    for path in sorted((Path(base) / 'data' / DIRECTORY).glob('*.jsonl')):
        for line in path.read_text().splitlines():
            row = json.loads(line)
            if row['observed_at'] > now or row['observed_at'] < now - 86400000:
                continue
            records += 1
            if row['source_sha256'] in seen:
                raise ValueError('Duplicate immediate book source')
            seen.add(row['source_sha256'])
            if row['source_sha256'] not in sources:
                # A recent book can refer to a source just outside the rolling day.
                source_ms = row.get('source_ms', row.get('source', {}).get('observed_at'))
                if source_ms is None or source_ms >= now - 86400000:
                    raise ValueError('Immediate book lacks its retained source capture')
            if row.get('state') == 'budget-skipped':
                states['budget-skipped'] = states.get('budget-skipped', 0) + 1
                continue
            cap, selected, books = row['source'], row['selection'], row['books']
            if U.sha(cap) != row['source_sha256'] or not cap['observed_at'] <= row['selected_ms'] <= row['completed_ms'] <= row['observed_at']:
                raise ValueError('Immediate book source/clock mismatch')
            if not matches(selection(cap), selected, lambda p: len(p) == 5 and p[0] == 'candidates'
                           and p[3] == 'pair' and p[4] in ('call_iv', 'put_iv')):
                raise ValueError('Immediate book selection failed reproduction')
            P.verify_books(books, selected, cap['observed_at'], row['selected_ms'])
            if books.get('ended_ms', books['started_ms']) > row['completed_ms']:
                raise ValueError('Immediate book completed before its batch')
            expected += books['expected']; attempted += len(books['raw'])
            usable += sum(q['state'] == 'ok' for q in books['quotes'])
            lags += [q['source_to_book_ms'] for q in books['quotes'] if q['source_to_book_ms'] is not None]
            states[books['state']] = states.get(books['state'], 0) + 1
    return {'source_captures_last_24h': len(sources), 'missing_book_records': len(set(sources)-seen),
            'records_last_24h': records, 'expected': expected, 'attempted': attempted, 'usable': usable,
            'source_to_book_ms': distribution(lags), 'states': states,
            'interpretation': 'Immediate collector diagnostic, separate from both prospective pilots. '
                              'Missing and budget-skipped captures are explicit; later sizes never replace original quotes.'}
