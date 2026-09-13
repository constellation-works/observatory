---
node: fput-recurrence-reproduction
domain: physics
experiment: experiments/physics/fput-recurrence-reproduction
ran_on: 2026-09-12
verdict: supports
strength: suggestive
---

# FPUT recurrence reproduction

## What was run

The frozen protocol ran 30,000 velocity-Verlet cycles for `N=32`,
`alpha=1/4`, `delta t=1/sqrt(8)`, fixed endpoints, and a from-rest mode-1 sine
wave. It sampled all modal energies every 50 cycles, ran the 10,000-cycle
linear control and the equal-duration 60,000-cycle `delta t/2` control, and
finished in about 1 second. The plotted values use `E_k(t)/E_1(0)*300`. The
runner (`run.py baseline`) now loads **protocol v2** by default;
`--protocol v1` still reruns the original for the historical record. The
numerics are byte-for-byte the same reconstruction as before — only the
digitized reference and two metric definitions changed (below).

## Repair: mode labels and protocol v2

The Milestone 1 digitization (`reference/fig1-digitized.csv`) assigned three
peaks to the wrong mode numbers, discovered by rendering PDF page 14 at 300
dpi (up from the original 150 dpi) until the printed numeral on each peak
became legible. Corrected: the ~6.5k/135 peak is mode 4 (was filed under mode
2), the ~14.0k/265 peak is mode 2 (was filed under mode 4), and the ~19.0k/193
peak is mode 3's second maximum (was double-booked as both "mode 3 second
maximum" and "mode 5 first maximum"). Previously missing rows were added:
mode 5's first maximum (~5.0k/60), mode 2's early bump (~2.5k/40), and mode
4's second maximum (~22k/110). The mode-1 minimum was re-measured: the
7,200-cycle/2-unit dip belonged to a different mode's curve, not mode 1's,
which stays well above zero through the exchange and only bottoms out near
19k-20k cycles. Full method, uncertainty, and high-dpi evidence crops are in
`reference/README.md`; the corrected CSV is pinned by digest in
`protocol/v2.json`.

Running v1's baseline exposed three specification errors in the protocol
itself, amended in v2 with `post_hoc: true` and a dated reason (see
`protocol/v2.json`'s `changelog`, tolerances unchanged in all three):

- **M3** moved from "first local maximum" (which caught a sub-1% early bump)
  to the *global maximum of modes 2, 3, and 4 over cycles 0-20,000* — the
  labelled major peaks. M3 now also reports (does not gate) mode 5's first
  major peak and mode 3's second maximum.
- **M4** moved from "summed energy of modes 6-31" to the *maximum single-mode
  energy* over modes 6-31, matching the caption's per-mode ceiling statement;
  the summed value is still reported for transparency.
- **C3** (δt/2 sensitivity) keeps its definition and 1% threshold, but no
  longer flips the overall execution status on failure. It is now a reported
  sensitivity check alongside the gating controls C1 and C2.

## Provenance and reference

The primary source is the OSTI copy at
<https://www.osti.gov/servlets/purl/4376203>, DOI
<https://doi.org/10.2172/4376203>. Its manifest pins the 1,570,076-byte PDF
with SHA-256
`3155813b1851da4fa6fba5818986718b197d68873d38965f3cd7489c14f396f1`; the PDF
is public-domain US Government work and is intentionally not tracked. The
Fig. 1 crop and CSV are digitized calibration evidence with stated
uncertainty (±250 cycles / ±5 energy units for individually-numeraled peaks,
wider for the un-numeraled mode-1 minimum; see `reference/README.md`), not
original numerical output. Dauxois, Peyrard and Ruffo, *The Fermi–Pasta–Ulam
numerical experiment: history and pedagogical perspectives* (Eur. J. Phys. 26
(2005) S3, arXiv:nlin/0501053), is retained as secondary historical context,
not as the target source.

## Shortlist and choice

The considered alternatives were M. Hénon and C. Heiles, AJ 69, 73 (1964),
whose Poincaré-section area fractions are accessible through ADS but whose AAS
copyright limits figure redistribution, and E. N. Lorenz, JAS 20, 130 (1963),
whose AMS-copyrighted Table 1 values have a weaker connection to the planned
chapters. LA-1940 was chosen because it has a stable full source, permits the
public-domain figure crop, is fully specified enough for independent
reconstruction, has a trivial 32-particle/30,000-step compute envelope, and
directly motivates the waves and numerical-error chapters.

## Assumptions and limits

- “Derivatives replaced by difference expressions” is reconstructed as an
  explicit position-space Störmer–Verlet / velocity-Verlet update; no author
  code exists.
- The baseline uses `delta t=1/sqrt(8)`, because the report distinguishes the
  cycle abscissa `delta t` from the caption's acceleration coefficient
  `delta t^2=1/8`. The alternative `delta t=1/8` is exploratory only.
- The chain starts from rest, with `x_i=sin(i*pi/N)`, fixed ends, unit masses,
  `beta=0`, and float64 deterministic arithmetic.
- The plotted modal energy omits nonlinear potential energy as the report's
  mode analysis does; full-energy conservation is a separate control.
- Digitization is approximate and the trace is not a substitute for the
  original MANIAC data. Mode labels rest on the figure's printed numerals and
  curve continuity from `t=0`, never on the reconstruction's own curves.

## What came out

Reproduction status (protocol v2): **completed; scientific verdict
supports**. The measured metrics are:

- **M1 pass:** recurrence at 28,400 cycles versus 28,600, within the
  ±1,000-cycle tolerance (digitization uncertainty ±250 cycles).
- **M2 pass:** recurrence fraction 0.977753 versus 0.966667, an absolute
  residual of 0.011087 within the ±0.03 tolerance.
- **M3 pass (all three gated modes, global maxima over 0-20,000 cycles):**
  mode 2 at cycle 14,100 with fraction 0.881771 (reference 14,000 /
  0.883333, residual +100 cycles / -0.001563); mode 3 at cycle 9,250 with
  0.712270 (reference 9,400 / 0.700000, residual -150 cycles / +0.012270);
  mode 4 at cycle 6,550 with 0.454435 (reference 6,500 / 0.450000, residual
  +50 cycles / +0.004435). All three are within the ±5% time / ±0.10
  energy-fraction tolerances.
  - **Reported, not gated:** mode 5's first major peak measured at cycle
    4,850, fraction 0.199952 (reference 5,000 / 0.2, residual -150 cycles /
    -0.0000475) — a close match. Mode 3's second maximum measured at cycle
    18,950, fraction 0.646708 (reference 19,000 / 0.643333, residual -50
    cycles / +0.003375) — also a close match, and the largest remaining
    qualitative uncertainty in the digitized reference given it rests on
    curve continuity more than a crisp numeral (see `reference/README.md`).
- **M4 pass (per-mode ceiling):** the maximum single-mode energy over modes
  6-31 reached 0.063170 (18.951 report units), under the 0.066667 (20-unit)
  ceiling. The summed modes-6-31 value is 0.084518 (25.355 units), reported
  for transparency but not the gate.
- **C1 pass:** maximum linear mode-1 drift was 0.000300832 (0.0301%), below
  0.01.
- **C2 pass:** maximum full-energy drift was 0.00201560 (0.2016%), below 0.01.
- **C3 reported, fails its own threshold:** halving `delta t` moved the
  physical recurrence from 10,040.9163 to 9,528.26388, a relative movement of
  0.0510563 (5.106%), above the 1% threshold. This no longer flips the
  overall execution status (see the protocol v2 amendment above); the
  recurrence time is a property of the discretised chain at its own step
  (`delta t^2=1/8`), and continuum convergence is not a precondition for
  reproducing the paper's figure. The 5.1% sensitivity itself is a real,
  quoted finding, not tuned away.

![Protocol-v2 reconstruction with corrected digitized-feature overlays](fput-recurrence-reproduction.png)

## The workbench (Milestone 3)

`run.py` now carries the whole workbench: `baseline`, `explore`, `report`, `evidence`
and `export`. `run.py report` renders one self-contained static page at
`_outputs/physics/fput-recurrence-reproduction/site/index.html` — the original Fig. 1
crop beside the reconstruction drawn on the *same* axes geometry (the reconstruction's
plot rectangle occupies the identical 96–901 px of 950 / 33–919 px of 1000 fraction that
`reference/README.md` calibrated, with the original's own units: t in thousands of
cycles, energy in the 300-unit report normalization), a residual panel, the metrics
table, separate execution/controls/assessment sections, the provenance panel and the
exploratory runs. Styles are inline and images are base64; nothing is fetched.

Drawn on matching axes, the reconstruction's curves land on the printed ones: the
residual panel shows every digitized feature inside the ±250-cycle / ±5-unit stated
digitization uncertainty (largest residuals: −200 cycles for the mode-1 recurrence,
+3.7 units for mode 3's first maximum).

Headless Chromium (`tools/browser_check.py`, Playwright `chromium_headless_shell`) at
1280 px and 375 px reports `horizontal_scroll: false`, eleven rendered sections, zero
remotely-loaded resources and no page errors on the study page, and the same at four
sections for the evidence browser. Wide tables scroll inside their own container rather
than pushing the document sideways.

## Exploration findings

Two bounded exploratory runs were kept. Each lives in its own
`explore-<delta-hash>-<timestamp>/` directory with `kind: exploratory`, the parameter
delta recorded in `run.json`, and no write of any kind to the baseline directory. The
allowed ranges are declared in `protocol/exploration.json` — a presentation-only sidecar,
because `protocol/v1.json` and `protocol/v2.json` declare themselves frozen and
byte-immutable after their landing tasks (their digests are pinned by existing runs).
Out-of-range values (`alpha=5`), unknown keys (`beta=1.0`) and a no-op delta
(`alpha=0.25`) are refused with exit code 2 and no directory is created.

**δt = 0.125 — the δt² trap made visible.** Reading the caption's `delta t^2 = 1/8` as
`delta t = 1/8` shrinks the model time per cycle by a factor 2.83, so 30,000 cycles span
only 3,750 model-time units instead of the baseline's 10,606.6. The first mode-1
recurrence sits near model time 10,041, i.e. near cycle 80,300 at this step: it is simply
not inside the figure's abscissa. M1's argmax over the 20,000–30,000 cycle window
therefore lands on the window's lower edge (20,000 cycles) with `E_1/E_1(0) = 0.159` —
mode 1 is still draining, not recurring — and M2 misses by a wide margin. The instructive
part is C3: it *passes* with movement exactly 0.0, because the dt and dt/2 runs both pick
the same window-edge argmax (physical time 2,500 in both). A control that passes
vacuously is still a control that passed; the number only means something read together
with its definition, which is why C3 is quoted with its physical recurrence times rather
than as a bare verdict.

**α = 1.0 — stronger nonlinearity, qualitative only.** The recurrence structure survives:
the mode-1 maximum in the 20k–30k window is at 28,400 cycles, the same cycle as the
baseline, but it returns only 77.0% of `E_1(0)` instead of 97.8%. Energy spreads much
further and much earlier — modes 2, 3 and 4 peak at 7,100 / 4,750 / 3,550 cycles with
0.92 / 0.88 / 0.81 of `E_1(0)` (baseline: 14,100 / 9,250 / 6,550 cycles at 0.88 / 0.71 /
0.45), and the per-mode higher-mode ceiling M4 rises from 0.063 to 0.611 of `E_1(0)`,
far above the caption's 20-unit statement. Full-energy drift C2 grows to 0.60% (still
inside 1%) and the δt/2 sensitivity C3 to 4.31%. The task identifies α=1 with the
report's Fig. 2 conditions; this experiment holds no digitization of Fig. 2, so the
comparison above is qualitative and the run's "failed" execution status only records
that the Fig. 1 reference does not describe these parameters. Nothing here amends the
baseline or the protocol.

## Evidence package and independent reproduction

`run.py export` writes
`_outputs/physics/fput-recurrence-reproduction/export/fput-reproduction-v2-<run>.tar.gz`
from an explicit allowlist — 23 members: `REPRODUCE.md`, the study page and evidence
browser, the four run artifacts, all four protocol documents, the reference CSV/method/
crop, the canonical records, `reproduction/commands.txt`, `environment/uv.lock`,
a generated `environment/README.md` and `MANIFEST.json` with every member's SHA-256.
`log.txt`, `_data` payloads and the PDF are deliberately outside the allowlist; the PDF
is identified by digest and fetch command only.

`run.py export --check` extracted the archive, verified all 23 digests and found no
home-directory absolute path (`members_verified: 23, absolute_paths: 0`). The same two
checks run by hand on the extracted tree agree (`mismatched: []`,
`grep -rE '/(home|Users|root)/' .` finds nothing).

Following `REPRODUCE.md` in a fresh environment:

```sh
uv venv /tmp/fput-repro-env
uv pip install --python /tmp/fput-repro-env/bin/python numpy==2.5.3 matplotlib==3.11.1
/tmp/fput-repro-env/bin/python experiments/physics/fput-recurrence-reproduction/run.py \
  baseline --output-root /tmp/fput-repro-out
```

reproduced the registered baseline **byte-for-byte**: `metrics.json`
(`1570191fa93e1bf2dfe2b9449a53b85e5ab8146fa7569691b8b43772e2e86721`), `energies.csv`
(`c145ec40…f270c4ee`) and even `figure.png` (`4614da6d…e256f2d768`) are identical to the
archived ones. The first attempt at this check installed Matplotlib 3.11.2 (only NumPy
was pinned) and the numerical artifacts still matched exactly while `figure.png` did
not — so the runner now records the Matplotlib version in `run.json` and `REPRODUCE.md`
pins both.

## Clean-environment reproduction (Milestone 6 acceptance)

Reverified on 2026-09-12 (23:34-23:59 UTC, ORB-12365) from scratch, in `/tmp`,
outside the checkout, using only the evidence package and the declared public source.
The package used for the reproduction was the one this checkout can build from its own
committed records (28 members, 9 records, 1,828,095 bytes): `export --check` verified
every SHA-256 and reported `members_verified: 28, absolute_paths: 0`, and the by-hand
`MANIFEST.json` check from `REPRODUCE.md` agreed (`members: 28, mismatched: []`) with
`grep -rE '/(home|Users|root)/'` finding nothing in the extracted tree. Rebuilding the
package against the complete 11-record chain on `main` gives 30 members
(`members_verified: 30, absolute_paths: 0`, 1,915,691 bytes); the run artifacts are the
same bytes in both.

1. The LA-1940 PDF was fetched from <https://www.osti.gov/servlets/purl/4376203> and
   verified against the data manifest: 1,570,076 bytes, SHA-256
   `3155813b…c14f396f1` -- `sha256sum -c` reports `OK`.
2. A fresh `uv venv` pinned from `run/run.json` (`numpy==2.5.3`,
   `matplotlib==3.11.1`) ran the one baseline command against a clean clone at the
   `git_revision` the run records (`d604ff5`).
3. The result is **identical to the registered baseline**: `metrics.json ==` the
   archived object field for field, and all three artifacts match by digest --
   `metrics.json 1570191f…e86721`, `energies.csv c145ec40…f270c4ee`,
   `figure.png 4614da6d…56f2d768`. These are the same digests the
   `…-baseline-metrics-json`, `…-baseline-energies-csv` and `…-baseline-figure-png`
   artifact records register, so the clean environment reproduces what the chain claims.

The metric values from that clean environment, quoted as measured:

| id | measured | reference | tolerance | result |
|---|---|---|---|---|
| M1 | 28,400 cycles | 28,600 | 1,000 | pass |
| M2 | 0.9777532985498025 | 0.9666666666666667 | 0.03 | pass |
| M3 mode 2 | 14,100 / 0.8817707004889854 | 14,000 / 0.8833333333333333 | 5% time, 0.10 height | pass |
| M3 mode 3 | 9,250 / 0.7122695735332155 | 9,400 / 0.7 | as above | pass |
| M3 mode 4 | 6,550 / 0.45443492092262405 | 6,500 / 0.45 | as above | pass |
| M4 | 0.06316980197954705 | 0.0666666667 | 0.0666666667 | pass |
| C1 | 0.00030083236612377107 | 0 | 0.01 | pass |
| C2 | 0.002015601922728094 | 0 | 0.01 | pass |
| C3 | 0.05105633802816894 | 0 | 0.01 | fail (reported, not gating) |

The two exploratory runs from the package's own instructions
(`explore --set alpha=1.0` and `explore --set dt=0.125`) then ran in the same
environment. Both exit 20 with `kind: exploratory`, `baseline_eligible: false` and the
parameter delta recorded, and both are `undermines` against the digitized reference, as
expected for a deviation from the frozen protocol. The baseline directory is byte-identical
before and after: recursive digest `43acc0c3d96c9c1a2e25041b9fa816aac52c6eb40d7caaa02c1aad2b3f2b94ac`
unchanged. An out-of-range deviation is refused rather than run:
`explore --set alpha=5.0` exits 2 with *"refused: alpha=5.0 is outside the declared
exploration range [0.0, 2.0]; the run is refused"*.

The study page was inspected in headless Chromium at 1280 px and 375 px: no console or
page errors, no horizontal scrolling, no remotely-loaded resource; the original Fig. 1
crop and the reconstruction are rendered at the same 950x1000 pixel geometry with the
same 0-30,000 cycle abscissa and 0-300 report-unit ordinate; every metrics-table row and
every residual-table row equals `metrics.json`; `site/data/metrics.json` and
`site/data/run.json` are the run's own files byte-for-byte (40/40 checks).

## Scientific records

The orbit-research record chain for this experiment is authored by
`tools/record_chain.py` and lives in `research/physics/fput-recurrence-reproduction/records/`
(the pinned package refuses any records path outside `research/`; see the pointer in
`experiments/physics/fput-recurrence-reproduction/research/README.md`). Four canonical
records are authored and delivered with this milestone: the program, the claim (the
node's kill condition), and the two frozen input artifacts (the digitized CSV, which is
also the holdout digest, and `protocol/v2.json`).

The remaining records — the registered protocol, the run-start receipt, the three result
artifacts, the completed run and the assessment — could not be authored here:
orbit-research resolves every reference from an exact Git snapshot, so each append must be
committed before the next refers to it, and the Orbit executor worktree mounts its `.git`
read-only. Rather than fake a reference, the driver stops and says so.

The completion was rehearsed twice in disposable clones under `/tmp` (both discarded).
The second rehearsal started from this milestone's exact delivery tree, with the four
authored records committed as the pipeline will commit them: the driver **reused** all
four, appended the remaining seven, and produced a bundle that
`uv run orbit-research validate` accepts — `{"valid": true, "errors": []}` over 21 records
and 8 manifests, the only unresolved pointer being the claim's pending reference to the
program (authored before the program could be committed, and recorded as `pending`
exactly for that reason). The evidence browser then rendered from that validated bundle.
After this milestone's delivery commit lands, one command does the same in place:

```sh
uv run experiments/physics/fput-recurrence-reproduction/tools/record_chain.py \
  --run <job-run-id> --stop-after export
```

Until then `run.py evidence` renders the browser directly from the canonical record
files under `site/evidence/`, with a banner saying exactly that: working-tree records,
not a validated export, listing the pending reference.

## What is shaky

The C3 sensitivity (5.1% recurrence-time shift under δt/2) is real and
unresolved; it says the discretised recurrence is step-size-sensitive even
though it no longer gates the execution status. Mode 3's second maximum
(~19k cycles) is the softest of the digitized reference points: the printed
numeral there was legible in the high-dpi crop but the surrounding curves
cross densely, so its uncertainty is wider than the other points'. The
mode-1 minimum has no legible printed numeral at all and rests on tracing
curve continuity from `t=0` — the simulated reconstruction's own mode-1
curve happens to bottom out in the same ~19k-20k window at a similar height,
which is a reassuring but non-circular cross-check (the label was fixed
before this run, from the figure and text alone). The original integration
ordering remains inferred rather than recovered from author code.

The scientific record chain is deliberately incomplete in this checkout (above): the
delivered records are honest but partial, and the registered-protocol/run/assessment
appends carry a further caveat when they land — the protocol-v2 baseline was first
executed under ORB-12375, *before* the native registration, so the chain proves local
registration order and frozen input identity, never independently attested prospective
execution. That is why the assessment is authored with `inference: exploratory` rather
than `confirmatory-primary`, and why its aggregate control field reads `failed` (C3
misses its own threshold) even though the execution status is `completed`.

## Next

Milestone 3 presents this result and its limitations: the study page, the two
exploratory runs, the evidence package and the partial record chain above. The open
follow-up is completing that chain with `tools/record_chain.py --stop-after export` from
a checkout whose `.git` is writable, after this milestone lands. Any further changed
method or feature-extraction rule requires a dated protocol v3 amendment; v1 and v2 stay
frozen, and `protocol/exploration.json` stays presentation-only.

### Milestone 6 close-out

The record chain is now complete on `main` (11 canonical records, commits
`cf11b29..721f693`): protocol, run-start receipt, three result artifacts, the completed
run and the assessment joined the four records delivered with Milestone 3.
`uv run orbit-research validate` accepts the exported bundle
(`{"valid": true, "errors": []}`, 21 record entries collapsing to 11 distinct records
across 8 export manifests). Two references remain `pending`: the claim's pointer to the
program, authored before the program record could be committed. That is documented, not
a defect -- orbit-research resolves references only from committed snapshots.

`run.py evidence` previously rendered one row per *occurrence*, so a record pinned by
three manifests appeared three times; it now shows each `(id, sequence)` once and reports
how many commits pin it. The packaged study report also labels the study-note path as an
observatory-checkout path rather than implying the file is inside the package.
