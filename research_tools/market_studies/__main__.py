"""Production entry point; mutations are restricted to the main-branch workflow."""
import sys
from desk import stream_util as U
from .core import ROOT, STREAM, Journal, activation, confirm, production, register
from . import collectors, experiments, report


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args not in (['prepare'], ['confirm'], ['execute'], ['collect'], ['score'], ['report']):
        raise SystemExit('usage: python -m research_tools.market_studies prepare|confirm|execute|collect|score|report')
    production()
    stage = args[0]
    now = U.clock_ms()
    try:
        register(ROOT, now)
        paused = (ROOT / STREAM / 'paused.json').exists()
        if stage == 'prepare' and not paused:
            experiments.prepare(ROOT)
        elif stage == 'confirm':
            confirm(ROOT)
        elif stage == 'execute' and not paused:
            experiments.execute(ROOT)
        elif stage == 'collect' and not paused:
            a = activation(ROOT)
            if a:
                collectors.pilots(ROOT, a['first_slot'], U.clock_ms())
        elif stage == 'score':
            experiments.score(ROOT, U.clock_ms())
        elif stage == 'report':
            report.write(ROOT, U.clock_ms())
        Journal(ROOT, 'runs').add(f'{stage}-{now}', {'stage': stage, 'started_ms': now, 'ended_ms': U.clock_ms(),
                                                   'state': 'paused' if paused and stage in ('prepare', 'execute', 'collect') else 'completed',
                                                   'run': U.run_meta()})
    except Exception as exc:
        Journal(ROOT, 'runs').add(f'{stage}-{now}', {'stage': stage, 'started_ms': now, 'ended_ms': U.clock_ms(),
                                                   'state': 'error', 'error': type(exc).__name__ + ': ' + str(exc)[:600], 'run': U.run_meta()})
        raise


if __name__ == '__main__':
    main()
