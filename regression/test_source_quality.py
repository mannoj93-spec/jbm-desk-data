import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import source_quality as Q
import state_score_verifier as V
from regression import test_state_v2 as fixture_module
from research_tools.state_v2 import core as K, study as S, models as M


class Quality(unittest.TestCase):
    def bars(self,n=5):
        return {i*K.MIN:{'t':i*K.MIN,'o':100,'h':100,'l':100,'c':100,'n':0,'v':0,'avail':(i+1)*K.MIN} for i in range(n)}

    def test_threshold_missing_counts_gaps_and_price_changes(self):
        self.assertEqual(Q.flat_runs(self.bars(4)),[])
        self.assertEqual(Q.flat_runs(self.bars())[0]['minutes'],5)
        for kind in ['missing','gap','price']:
            b=self.bars()
            if kind=='missing':del b[2*K.MIN]['n']
            elif kind=='gap':del b[2*K.MIN]
            else:b[2*K.MIN].update(o=101,h=101,l=101,c=101)
            self.assertEqual(Q.flat_runs(b),[])

    def test_recovery_and_immutable_incident_history(self):
        b=self.bars();incident=Q.flat_runs(b)[0];self.assertEqual(incident['state'],'unresolved')
        incident['id']='test';incident['affected_score_windows']=[]
        with tempfile.TemporaryDirectory() as tmp:
            report={'generated_ms':10*K.MIN,'incidents':[incident]};Q.persist(tmp,report)
            path=Path(tmp)/Q.PATH;first=path.read_bytes()
            report['generated_ms']+=K.MIN;Q.persist(tmp,report);self.assertEqual(first,path.read_bytes())
            b[5*K.MIN]=dict(b[4*K.MIN],n=1,v=1,avail=6*K.MIN)
            recovered=dict(Q.flat_runs(b)[0],id='test',affected_score_windows=[])
            report['incidents']=[recovered];Q.persist(tmp,report)
            rows=[json.loads(x) for x in path.read_text().splitlines()]
            self.assertEqual(len(rows),2);self.assertEqual(rows[0]['first_detected_ms'],rows[1]['first_detected_ms'])
            path.write_text(path.read_text().replace('recovered','tampered'))
            with self.assertRaisesRegex(ValueError,'corruption'):Q.persist(tmp,report)

    def test_overlap_uses_exclusive_end_and_only_btc(self):
        with tempfile.TemporaryDirectory() as tmp:
            Q.K.Journal(tmp,'scores').add('f',{'study':'state','outcome':{'entry':5*K.MIN,'end':9*K.MIN}})
            incident={'series':Q.SERIES[0],'start_ms':0,'end_ms':5*K.MIN}
            self.assertEqual(Q.impacts(tmp,incident),[])
            incident['end_ms']+=1;self.assertEqual(len(Q.impacts(tmp,incident)),1)
            incident['series']=Q.SERIES[1];self.assertEqual(Q.impacts(tmp,incident),[])


class Replay(unittest.TestCase):
    def test_scores_reproduce_and_rehashed_mutations_fail(self):
        fixture=fixture_module.Publication();fixture.setUp();self.addCleanup(fixture.doCleanups)
        fixture.activate();f=fixture.forecast();base=fixture.base;slot=fixture.slot
        K.confirm(base,clock=lambda:slot+2*K.MIN,fetch=fixture.remote)
        entry=f['data']['entry'];now=slot+5*K.HOUR
        bars={entry+i*K.MIN:{'o':100.,'h':102.,'l':99.,'c':101.,'avail':entry+(i+1)*K.MIN} for i in range(240)}
        with patch.object(S,'Store') as source:
            source.return_value.bars.return_value=bars;S.score(base,now)
        original=copy.deepcopy(K.Journal(base,'scores').rows[0]['data'])
        with patch.object(V,'Store') as source:
            source.return_value.bars.return_value=bars
            self.assertEqual(len(V.verify(base,K.verified(base),now)),1)
            for mutate in [lambda d:d.update(primary_difference=99), lambda d:d['losses'].update(full=99),
                           lambda d:d['outcome'].update(bars_sha='bad'),lambda d:d.update(scored_ms=now+1)]:
                d=copy.deepcopy(original);mutate(d);(base/K.STREAM/'scores.jsonl').unlink()
                K.Journal(base,'scores').add(f['id'],d)
                with self.assertRaises(ValueError):V.verify(base,K.verified(base),now)
            (base/K.STREAM/'scores.jsonl').unlink();K.Journal(base,'scores').add(f['id'],original)
            del bars[entry]
            with self.assertRaisesRegex(ValueError,'complete'):V.verify(base,K.verified(base),now)


if __name__=='__main__':unittest.main()
