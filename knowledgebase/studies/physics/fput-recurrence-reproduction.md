---
node: fput-recurrence-reproduction
domain: physics
experiment: experiments/physics/fput-recurrence-reproduction
ran_on: 2026-09-12
verdict: inconclusive
strength: suggestive
---

# FPUT recurrence reproduction

## What was run

Nothing numerical yet. The reproduction protocol is frozen for a future
independent reconstruction of Fig. 1 in E. Fermi, J. Pasta, S. Ulam (with M.
Tsingou), *Studies of Nonlinear Problems, I*, Los Alamos report LA-1940 (May
1955), report page 12 / PDF page 14. The target is the first five modal-energy
curves over approximately 30,000 computational cycles for `N=32`,
`alpha=1/4`, and caption value `delta t^2=1/8`.

## Provenance and reference

The primary source is the OSTI copy at
<https://www.osti.gov/servlets/purl/4376203>, DOI
<https://doi.org/10.2172/4376203>. Its manifest pins the 1,570,076-byte PDF
with SHA-256
`3155813b1851da4fa6fba5818986718b197d68873d38965f3cd7489c14f396f1`; the PDF
is public-domain US Government work and is intentionally not tracked. The
Fig. 1 crop and CSV are digitized calibration evidence with ±250-cycle and
±5-energy-unit uncertainty, not original numerical output. Dauxois, Peyrard
and Ruffo, *The Fermi–Pasta–Ulam numerical experiment: history and pedagogical
perspectives* (Eur. J. Phys. 26 (2005) S3, arXiv:nlin/0501053), is retained as
secondary historical context, not as the target source.

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
  original MANIAC data.

## What came out

Reproduction status: **protocol frozen, not yet run**. There is no numerical
verdict to promote. The future run must report M1–M4, controls C1–C3, the
declared discrepancy rule, and its runtime and input hashes.

## What is shaky

The historical figure is a dense raster with overlapping curves and finite
grid resolution. The exact original integration ordering is inferred from the
report rather than recovered from source code. These uncertainties are
explicit in `protocol/v1.md` and the reference README; they must not be tuned
away after seeing a result.

## Next

Implement the runner and independent reference only in the next milestone,
then promote the measured run and figure into this study without editing the
frozen v1 protocol.
