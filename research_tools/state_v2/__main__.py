"""Main-branch-only state-v2 stages; a failed v2 stage cannot prevent v1 persistence."""
import sys
from desk import stream_util as U
from research_tools.market_studies.core import STREAM as V1_STREAM
from . import core as K, study


def paused(base):
    return any((base / stream / 'paused.json').exists() for stream in (V1_STREAM, K.STREAM))


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args not in (['prepare'], ['confirm'], ['score'], ['report']):
        raise SystemExit('usage: python -m research_tools.state_v2 prepare|confirm|score|report')
    K.production()
    stage, now = args[0], U.clock_ms()
    try:
        K.register(K.ROOT, now)
        stopped = paused(K.ROOT)
        if stage == 'prepare' and not stopped:
            study.prepare(K.ROOT)
        elif stage == 'confirm':
            K.confirm(K.ROOT)
        elif stage == 'score':
            study.score(K.ROOT, U.clock_ms())
        elif stage == 'report':
            study.write(K.ROOT, U.clock_ms())
        state = 'paused' if stopped and stage == 'prepare' else 'completed'
        K.Journal(K.ROOT, 'runs').add(f'{stage}-{now}', {'stage': stage, 'started_ms': now,
            'ended_ms': U.clock_ms(), 'state': state, 'run': U.run_meta()})
    except Exception as exc:
        K.Journal(K.ROOT, 'runs').add(f'{stage}-{now}', {'stage': stage, 'started_ms': now,
            'ended_ms': U.clock_ms(), 'state': 'error', 'error': type(exc).__name__ + ': ' + str(exc)[:600],
            'run': U.run_meta()})
        raise


if __name__ == '__main__':
    main()
