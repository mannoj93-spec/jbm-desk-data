# Streaming collector (stream-1.0)

A separate, continuously running service for the second-scale data the 15-minute GitHub
collector cannot observe: order-book reconstruction, trades and forced-flow messages. It is
**not** run by GitHub Actions and nothing it records is committed to this repository.

**Status: implemented and tested; not deployed.** No always-on host has been authorised. The
remaining decision is listed at the end of this file.

## What it records

| Venue | Channels (public, no credentials) | Continuity check |
|---|---|---|
| Deribit | `book.BTC-PERPETUAL.100ms`, `trades.BTC-PERPETUAL.100ms`; heartbeat via `public/set_heartbeat` (10 s) with `public/test` replies | `prev_change_id` must equal the last `change_id`; otherwise the book is invalidated, a gap is written and the channel is re-subscribed for a fresh snapshot |
| Bybit (linear) | `orderbook.50.BTCUSDT`, `publicTrade.BTCUSDT`, `allLiquidation.{BTC,ETH,SOL}USDT`, `adlAlert.USDT` (filtered to BTC/ETH/SOL before storage; the filter is named in the channel) | update id `u` must increase by exactly 1 (verified live: 3,073 consecutive deltas, no exceptions); `u = 1` or a snapshot resets the book; a jump invalidates and re-subscribes |
| Hyperliquid | `l2Book` and `trades` for BTC, ETH, SOL; `{"method":"ping"}` keep-alive | each push is a whole snapshot; older-or-equal pushes are dropped; silence > 15 s is a gap |

Measured on 2026-09-23 from the development environment: Hyperliquid `l2Book` pushes arrived
every 5.0-5.5 s (documented minimum 0.5 s), so Hyperliquid 1-second samples can be up to ~5.5 s old
(`book_age_ms` is stored) and module E does not use them. Bybit REST returned HTTP 403 from the
development environment while the Bybit WebSocket worked; only the WebSocket is used. Deribit
hides the trade `liquidation` flag from the public for the first hour, so Deribit forced flow is
counted but not relied on. Bybit `allLiquidation` prices are bankruptcy prices (Bybit docs) and are
labelled so wherever they are summed.

Documentation checked: Hyperliquid WebSocket subscriptions and rate limits (10 connections,
1000 subscriptions, 2000 messages/minute per IP); Deribit `public/get_book_summary_by_currency`,
`book.{instrument}.{interval}`, `public/set_heartbeat`; Bybit V5 public `orderbook`,
`publicTrade`, `allLiquidation`, `adlAlert`. This service uses 3 connections and 14 subscriptions.

## Storage layout (under `STREAM_DATA_DIR`)

```
raw/<venue>/<channel>/<YYYY-MM-DD>/<HH>.jsonl.gz     every message as received + receive time
derived/book1s/<venue>/<instrument>/<day>/<HH>.jsonl.gz
                                                     1-second samples of VALID, FRESH books only:
                                                     bid, ask, mid, depth within 10 bp per side,
                                                     book timestamp, book age
derived/gaps/<day>.jsonl                             disconnects, sequence gaps, silences, restarts
derived/triggers/<day>.jsonl                         trigger and control log
captures/<day>/<capture_id>.jsonl.gz                 rolling buffer: 5 min before + 15 min after
                                                     each trigger and each hourly control
manifest/<day>.jsonl                                 uploaded partitions: key, bytes, sha256
heartbeat.json, state.json                           liveness and upload/restart state
```

Gzip members are appended every `flush_s` (5 s) with fsync, so a crash loses at most the
unflushed tail and never corrupts earlier members. A missing second in `book1s` means the book was
invalid, stale or disconnected - the gap log says which - never a quiet book. Triggers: a
1-second mid move beyond `mid_move_sigma` sigma over `window_s` (per book, cooldown), and Bybit
liquidations above `liq_burst_usd_60s` (bankruptcy-price notional) in 60 s. Scheduled controls fire
every `controls_every_s`, so every trigger type has baseline captures.

## Run

```
python -m stream.service --config stream/config.example.json            # forever
python -m stream.service --config stream/config.example.json --duration 60
python -m stream.check_heartbeat /var/lib/jbm-stream                     # exit 1 if stale/down
```

Standard library only (Python 3.11+). `HTTPS_PROXY` is honoured when set. Deployment files:
`deploy/Dockerfile` (python:3.11-slim, non-root, healthcheck) and `deploy/jbm-stream.service` with
`deploy/jbm-stream-check.{service,timer}` for systemd (MemoryMax 512M, CPUQuota 50%).

## Durable backend (optional, reversible)

Set `storage.backend` to `"s3"` and export the two variables named in the config
(`JBM_STREAM_S3_KEY`, `JBM_STREAM_S3_SECRET`). Any S3-compatible bucket works (AWS S3, Cloudflare
R2, Backblaze B2). Closed hourly partitions are uploaded every `upload_every_s`, verified by size,
listed in the manifest with their sha256, and only then become eligible for local retention
deletion. Upload failures are counted in the heartbeat and retried; they never stop capture.
Without a backend nothing is ever deleted unless `local_only_deletion` is set to true. The signer
is AWS SigV4, cross-checked against botocore 1.35.0 on fixed vectors (see the tests).

## Resource estimate (measured 2026-09-23, 120 s live run, quiet market)

| Item | Measured | Per day | Notes |
|---|---|---|---|
| CPU | 2.3 s CPU per 120 s | ~2% of one core | parsing + gzip |
| Memory | 29 MB max RSS | - | rolling buffer capped at 64 MB (`buffer.max_bytes`) |
| Raw partitions | 351 KB / 120 s | ~250 MB | ~7.5 GB/month; Bybit orderbook is ~2/3 |
| Derived (book1s, gaps) | 21 KB / 120 s | ~15 MB | this is what the lab reads |
| Captures | - | ~25-40 MB | 24 hourly controls + triggers, 20 minutes each |

Message rates in a volatile market can be several times higher; size the disk for ~3x. With
7-day raw and 30-day derived local retention: ~2 GB (raw) + 0.5 GB (derived) + captures; 20 GB of
disk leaves ample room. Egress to a bucket equals the raw figure.

## How the lab uses it

Module E (`lab/modules/liquidity.py`) reads `derived/book1s` and `derived/gaps` from
`STREAM_DATA_DIR`. Without them it reports "unavailable" and produces nothing. The GitHub research
workflow cannot see this directory, so E stays unavailable there until one of the two options
below is chosen.

## Remaining decision (owner authorisation needed; nothing has been provisioned)

1. **Host**: any always-on Linux machine or small VM (1 vCPU, 1 GB RAM, 20 GB disk) with outbound
   HTTPS to the three venues. Run the Docker image or the systemd unit.
2. **Where module E runs**, either
   - on that host (`STREAM_DATA_DIR=/var/lib/jbm-stream python -m lab.run update --no-write`,
     reading this repository's data from a checkout), or
   - in the GitHub research workflow, after syncing `derived/` (~15 MB/day) to an S3-compatible
     bucket and adding read-only bucket credentials as repository secrets.
3. **Optional bucket** for durable raw partitions (~7.5 GB/month at the measured rate).
