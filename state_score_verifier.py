"""Read-only numerical replay outside the frozen state-v2 research identity."""
from lab.data import Store
from research_tools.state_v2 import study, models


def verify(base, rows, now):
    scores = study.bound_scores(base, rows)
    if not scores:
        return scores
    bars = Store(base, now).bars('binance_klines_1m_BTCUSDT_perp')
    byid = {f['id']: f['data'] for f, _ in rows}
    for key, score in scores.items():
        d = byid[key]
        if not d['prepared_ms'] <= score['scored_ms'] <= now:
            raise ValueError('State-v2 score has an invalid scoring clock')
        outcome = models.price_outcome(bars, d['entry'], 240, score['scored_ms'])
        if not outcome:
            raise ValueError('State-v2 score lacks its complete as-of outcome path')
        losses = {arm: (p - outcome['y']) ** 2 for arm, p in d['probabilities'].items()}
        expected = {'study': 'state', 'slot': d['slot'], 'outcome': outcome, 'losses': losses,
                    'primary_difference': losses['full'] - losses['baseline'], 'event': d['row'].get('event', False)}
        if any(score.get(k) != v for k, v in expected.items()):
            raise ValueError('State-v2 cached score failed independent numerical reproduction: ' + key)
    return scores
