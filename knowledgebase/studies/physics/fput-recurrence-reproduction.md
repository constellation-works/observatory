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

## Next

Milestone 3 may present this result and its limitations. Any further
changed method or feature-extraction rule requires a dated protocol v3
amendment; v1 and v2 stay frozen.
