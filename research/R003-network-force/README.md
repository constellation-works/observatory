---
id: R003
title: Network force
status: done
tags: [physics, galaxies, sparc]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: [H002]
---

# R003 — Network force

Origin: [`_archive/lineage/nodes/network-force.md`](../../_archive/lineage/nodes/network-force.md).
Tests [`H002`](../../hypotheses/H002-network-fluctuations-supply-the-sparc-extra-acceleration.md).

## Question

If the acceleration beyond visible baryons comes from a dynamic,
connection-forming network, how large can a coherent galaxy-to-galaxy
fluctuation in that term be without broadening the radial acceleration relation
beyond its observed 0.11-dex Gaussian width?

## Method

`code/rar-network-fluctuation-limit/main.py` builds a seeded mock of 153
galaxies and exactly 2693 resolved points, matching the quality-cut scale of the
original SPARC RAR analysis, with
`g_RAR = g_bar / (1 - exp(-sqrt(g_bar/g_dagger)))`, `g_dagger = 1.20e-10 m/s²`,
and an injected network term `g_obs = g_bar + (g_RAR - g_bar) * 10^delta`,
`delta ~ Normal(0, sigma_net)` in dex, coherent across radii within a galaxy.
The observable is the standard deviation of `log10(g_obs) - log10(g_RAR(g_bar))`;
a `sigma_net` is excluded at 95% when at least 95% of mock populations come out
broader than 0.11 dex. Deterministic; refreshes `code/.../assets/results.json`
and `exclusion-curve.png`. No SPARC bytes are consumed.

## Result

`sigma_net < 0.171` dex at 95% confidence. Recorded as `inconclusive` on `H002`:
it excludes large coherent fluctuations, but a smaller value is not supported by
the test, merely not excluded.

## Limitations

Log-normal, fully coherent, time-independent fluctuations only. Non-log-normal,
baryon-linked and time-averaged fluctuations are unresolved, and the mock is
SPARC-*like* rather than SPARC. No network model yet predicts a number to compare
the bound against, so the kill condition cannot fire either way.

## Next

A network mechanism that predicts a fluctuation amplitude. Without one, tightening
the bound settles nothing.
