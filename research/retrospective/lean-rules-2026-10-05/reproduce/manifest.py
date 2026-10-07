import sys, json, datetime as dt, hashlib
sys.path.insert(0,'/root/in29/crypto-desk')
import jbm_archive as ja
from concurrent.futures import ThreadPoolExecutor
st,rows,man=ja.load_klines_span(dt.date(2020,1,1), dt.date(2026,10,4), '4h')
def one(d):
    s,r,rep=ja.load_metrics(d); return {"day":d.isoformat(),"entry":ja.manifest_entry(s,rep)}
days=[dt.date(2024,10,1)+dt.timedelta(days=i) for i in range((dt.date(2026,10,4)-dt.date(2024,10,1)).days+1)]
with ThreadPoolExecutor(12) as ex: mets=list(ex.map(one,days))
out={"code_version":ja.VERSION,"klines_4h":{"state":st,"bars":len(rows),"files":man},"metrics":mets}
b=json.dumps(out,sort_keys=True,separators=(",",":")).encode()
open('data_manifest.json','wb').write(b)
print('klines',st,len(rows),len(man),'metrics days',len(mets),'states',{s:sum(1 for m in mets if m['entry'].get('state')==s) for s in set(m['entry'].get('state') for m in mets)},'sha256',hashlib.sha256(b).hexdigest())
