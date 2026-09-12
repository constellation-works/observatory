# FPUT recurrence reproduction

Domain: `physics` · Node: `neb show fput-recurrence-reproduction` · Started: 2026-09-12

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

Protocol v1 freezes the independent reconstruction specification. The
baseline uses the quadratic FPUT chain, N=32, α=0.25, β=0, fixed ends,
from-rest single-sine initial displacement, float64 arithmetic, and an
explicit central-difference/Störmer–Verlet integrator. The five mode-energy
series will be compared with the digitized LA-1940 Fig. 1 features. Controls
and tolerances are in [`protocol/v1.md`](protocol/v1.md); the machine-readable
runner input is [`protocol/v1.json`](protocol/v1.json).

The reference image and CSV are digitized from the public-domain OSTI/LANL
scan. They are calibration evidence, not the original numerical dataset.

## Run

```sh
uv run experiments/physics/fput-recurrence-reproduction/run.py baseline
```

The runner interprets “first local maximum” literally on the sampled modal
energy series, without smoothing or a reference-derived prominence threshold.
Consequently, M3 retains early small local maxima caused by nonlinear exchange
rather than selecting later peaks to resemble the digitized figure. A
`--cycles` override is available only as a non-baseline diagnostic, and
`--force-control-failure C1|C2|C3` exercises the auditable failure path.

## Result

Protocol v1 was run without tuning. M1 and M2 pass, but convergence control C3
fails: halving the time step moves the physical recurrence time by 5.106%
against a strict 1% tolerance. The scientific assessment is therefore
inconclusive and the failed baseline summary is retained under `attempts/`.
