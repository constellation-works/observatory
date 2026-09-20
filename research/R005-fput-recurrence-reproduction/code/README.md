# FPUT recurrence reproduction — the workbench

How to run the reproduction. The result is written up one directory up, in the
research record's [`README.md`](../README.md). Started 2026-09-12.

## Question

Can an independent Störmer–Verlet reconstruction of the LA-1940 experiment
recover the first mode-1 recurrence in Fig. 1 without tuning the frozen
protocol?

## Kill condition

An independent Störmer–Verlet reconstruction of LA-1940 Fig. 1 (N=32,
α=1/4, δt²=1/8) does not show the first mode-1 recurrence within ±1000 cycles
of the digitized figure, or returns less than 94% of the initial mode-1 energy
at that recurrence.

## Method

Protocol v2 freezes the independent reconstruction specification (v1 stays
frozen and describes the pre-repair reading). The baseline uses the quadratic
FPUT chain, N=32, α=0.25, β=0, fixed ends, from-rest single-sine initial
displacement, float64 arithmetic, and an explicit central-difference/Störmer–
Verlet integrator. The five mode-energy series are compared with the digitized
LA-1940 Fig. 1 features. Controls and tolerances are in
[`protocol/v2.md`](protocol/v2.md); the machine-readable runner input is
[`protocol/v2.json`](protocol/v2.json).

The reference image and CSV are digitized from the public-domain OSTI/LANL
scan. They are calibration evidence, not the original numerical dataset.

## The workbench: seven steps, seven commands

Every command below runs from the repository root after `uv sync --extra research`.
`R=research/R005-fput-recurrence-reproduction/code` shortens the runner path;
generated output lands in `research/R005-fput-recurrence-reproduction/output/`, which is
never tracked by Git.

**1. Verify the target.** The LA-1940 PDF is never tracked. Fetch it to a temporary
path and check it against the data manifest:

```sh
curl -L --fail -o /tmp/la-1940.pdf https://www.osti.gov/servlets/purl/4376203
echo "3155813b1851da4fa6fba5818986718b197d68873d38965f3cd7489c14f396f1  /tmp/la-1940.pdf" | sha256sum -c -
```

**2. Read the frozen protocol.** `protocol/v2.md` is the human document and
`protocol/v2.json` is what the runner loads; `protocol/exploration.json` declares which
parameters an exploratory run may move and how far. Frozen files are never edited — a
changed method needs a new version.

**3. Run the registered baseline.**

```sh
uv run $R/run.py baseline            # --protocol v1 reruns the original for the record
```

Exit codes: `0` completed, `10` inconclusive, `20` failed (including a failed gating
control), `2` usage, `3` infrastructure. The run directory holds `run.json`,
`energies.csv`, `metrics.json`, `figure.png` and `log.txt`.

**4. Render the study page and look at it.**

```sh
uv run $R/run.py report              # --run <dir> to report a specific run
LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
  uv run --with playwright python $R/tools/browser_check.py \
  research/R005-fput-recurrence-reproduction/output/site/index.html
```

The page is one self-contained HTML file: the original Fig. 1 crop beside the
reconstruction on matching axes, the residual panel with the digitization uncertainty,
the metrics table, separate execution/controls/assessment sections, the provenance panel
and the exploratory runs. The browser check reports horizontal scrolling, page errors
and any remotely-loaded resource at 1280 px and 375 px.

**5. Explore bounded alternatives.**

```sh
uv run $R/run.py explore --set alpha=1.0     # the report's Fig. 2 conditions
uv run $R/run.py explore --set dt=0.125      # the naive reading of the caption
```

Each writes its own `explore-<delta-hash>-<timestamp>/` directory with
`kind: exploratory` and the parameter delta in `run.json`, never touching the baseline.
Unknown keys and out-of-range values are refused with exit code 2.

**6. Register the scientific records and build the evidence browser.** The append-only
orbit-research chain (`program → claim → artifact → preregister → begin-run →
record-run → assess`) lives in `_archive/records/fput/`
at the repository root; see [`research/README.md`](research/README.md) for why, and for
the exact `--owner-root/--repository/--records` arguments. One idempotent driver authors
it, commits each append (orbit-research resolves references only from committed
snapshots), exports the bundle, validates it and renders the browser:

```sh
uv run $R/tools/record_chain.py --run <job-run-id> --stop-after export
```

In a checkout that cannot be committed to — the Orbit executor worktree mounts `.git`
read-only — run `--no-commit --stop-after inputs`: the appends that need no resolved
reference are authored and the driver stops rather than faking a pin. The equivalent
manual commands, once the records are committed, are:

```sh
uv run orbit-research export --owner-root "$PWD" --repository observatory \
  --records _archive/records/fput \
  --source-revision "$(git rev-parse HEAD)" --output /tmp/fput-records-export.json
uv run orbit-research validate /tmp/fput-records-export.json
uv run $R/run.py evidence --bundle /tmp/fput-records-export.json   # or: run.py evidence
```

`run.py evidence` with no bundle browses the canonical record files directly and labels
the page as working-tree records rather than a validated export.

**7. Export the evidence package and verify it.**

```sh
uv run $R/run.py export
uv run $R/run.py export --check
```

`export` writes `research/R005-fput-recurrence-reproduction/output/export/fput-reproduction-<protocol>-<run>.tar.gz`
from an explicit allowlist (study page, evidence browser, run artifacts, protocols,
reference material, records, `REPRODUCE.md`, the environment lock and a digest
manifest). `--check` extracts it, verifies every recorded SHA-256 and refuses absolute
paths, traversal and unlisted members. [`REPRODUCE.md`](REPRODUCE.md) is the recipient's
instruction sheet: verify, create an environment, run the one baseline command, compare
`metrics.json`.

## Run

```sh
uv run research/R005-fput-recurrence-reproduction/code/run.py baseline
```

The runner interprets “first local maximum” literally under protocol v1, without
smoothing or a reference-derived prominence threshold; protocol v2 instead takes the
labelled major peaks as global maxima over cycles 0–20,000. A `--cycles` override is
available only as a non-baseline diagnostic, and `--force-control-failure C1|C2|C3`
exercises the auditable failure path.

## Result

Protocol v2 was run without tuning. M1–M4 and the gating controls C1 and C2 pass; the
reported sensitivity check C3 still fails its own 1% threshold (halving `delta t` moves
the physical recurrence time by 5.106%), which v2 records rather than gates. The
execution status is *completed* and the scientific assessment is *supports*; the study
note carries the numbers, the exploration findings and the export verification.
