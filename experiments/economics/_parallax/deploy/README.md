---
title: "Deploying the Crypto Recorders"
summary: "Checklist for moving Parallax crypto capture from the Mac to dk-server-1."
tags: [parallax, crypto, deployment, recorder]
related: ["docs/research/R01-crypto/DATA.md", "docs/research/R01-crypto/MICROSTRUCTURE.md", "deploy/CONSUMER_GOODS.md"]
created_on: 2026-08-01
updated_on: 2026-08-03
status: active
---

# Deploying the recorders on dk-server-1

The one-time R03 Google Trends pilot import has a separate guide in
[`CONSUMER_GOODS.md`](CONSUMER_GOODS.md). It does not run as a service. This document remains focused
on continuous R01 crypto recorders.

Checklist for moving capture off the Mac. Order matters.

## 0. Preconditions (from the Mac, tonight)

- Parallax has a remote and is in `operations/scripts/repos.tsv`; `agent-main` pushed.
- Mac recorders keep running until the box units are confirmed up — overlap is fine,
  a hole is not.

## 1. On the box

```sh
df -h                              # THE gate: June audit showed ~21 GB free on root.
                                   # Full spot+futures is 2-6 GB/day. Decide mode first.
cd ~/constellation/codebases/parallax   # adjust to the box layout
git pull
uv sync --group capture
uv run parallax book record --symbol BTCUSDT   # smoke test, ctrl-c after a few seconds
```

Disk decision:

| Free space | Mode |
|---|---|
| > 150 GB | Full spot + full futures (default units) |
| 30–150 GB | Full spot; futures with `--streams "aggTrade,bookTicker,forceOrder,markPrice@1s"` |
| < 30 GB | Do not deploy capture here; keep it on the Mac until dk-server-2 |

## 2. Install units

```sh
mkdir -p ~/.config/systemd/user
cp deploy/systemd/parallax-record-*.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now parallax-record-spot.service parallax-record-futures.service
journalctl --user -u parallax-record-spot -f    # watch it connect
```

Linger is already enabled on the box (dsearch units rely on it), so user units survive
logout and start on boot.

## 3. Verify, then hand over

```sh
ls -lh data/R01-crypto/raw/book/BTCUSDT/*/ | tail   # files growing
uv run parallax book build --symbol BTCUSDT     # reconstructs with gaps=0-ish
```

Only after both units have run cleanly for an hour: stop the Mac recorders, then rsync
the Mac's capture into the box tree. If the handover hour exists on both sides, keep
both copies (e.g. put the Mac tree under its own day-directory) — the reader dedupes
overlapping diffs by update id, but an overwritten file is unrecoverable.

## 4. Watchdog

Capture that silently stops is worse than capture that never ran. The stall watchdog
(`parallax-capture-watchdog.{service,timer}`) checks every 5 minutes that some capture
file is newer than 10 minutes; on stall it logs at err priority (tag
`parallax-watchdog`) and writes `data/R01-crypto/raw/book/.stall-alert` (removed on recovery). It
is a detector only — recorder restarts belong to the recorder units' `Restart=always`.

```sh
cp deploy/systemd/parallax-capture-watchdog.* ~/.config/systemd/user/   # + path adjust
systemctl --user daemon-reload
systemctl --user enable --now parallax-capture-watchdog.timer
journalctl --user -t parallax-watchdog -n 5     # stall alerts, if any
```

## dk-server-2 (late August)

The mirror box takes over full-depth capture on arrival; these same units move over
with only the `WorkingDirectory` path changing. Retention policy and cutover order:
almanac `20-projects/dk-server-2/deployment-plan.md`.
