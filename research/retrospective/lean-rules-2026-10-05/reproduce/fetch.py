import sys, json, datetime as dt, time, urllib.request
sys.path.insert(0,'/root/in29/crypto-desk')
import jbm_archive as ja
from concurrent.futures import ThreadPoolExecutor
t0=time.time()
st,rows,man=ja.load_klines_span(dt.date(2020,1,1), dt.date(2026,10,4), '4h')
bad=[m for m in man if m.get('state')!='ok'] if isinstance(man,list) else []
print('klines',st,len(rows),'non-ok files',len(bad), round(time.time()-t0,1)); json.dump(rows,open('k4h.json','w'))
# metrics (Binance BTCUSDT OI etc.), last ~24 months
days=[dt.date(2024,10,1)+dt.timedelta(days=i) for i in range((dt.date(2026,10,4)-dt.date(2024,10,1)).days+1)]
def one(d):
    for a in range(3):
        try:
            s,r,_=ja.load_metrics(d); return d.isoformat(),s,r
        except Exception as e: err=str(e); time.sleep(1)
    return d.isoformat(),'retrieval_error',[]
t0=time.time()
with ThreadPoolExecutor(12) as ex: res=list(ex.map(one,days))
states={}
out=[]
for d,s,r in res:
    states[s]=states.get(s,0)+1
    out+= [{'t':x['available_at_utc'],'stamp':x['archive_stamp_utc'],'oi':x['oi_btc']} for x in r if x.get('oi_btc') is not None]
print('metrics days',len(days),states,'rows',len(out),round(time.time()-t0,1)); json.dump({'rows':out,'states':{d:s for d,s,_ in res}},open('metrics.json','w'))
# funding history
B='https://www.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=1000&startTime='
start=int(dt.datetime(2020,1,1,tzinfo=dt.timezone.utc).timestamp()*1000); fr=[]
while True:
    js=json.load(urllib.request.urlopen(B+str(start),timeout=30))
    if not js: break
    fr+=js; start=js[-1]['fundingTime']+1
    if len(js)<1000: break
    time.sleep(0.3)
print('funding',len(fr),fr[0]['fundingTime'],fr[-1]['fundingTime']); json.dump(fr,open('funding.json','w'))
