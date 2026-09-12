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

Milestone 1 freezes the independent reconstruction specification only. The
baseline will use the quadratic FPUT chain, N=32, α=0.25, β=0, fixed ends,
from-rest single-sine initial displacement, float64 arithmetic, and an
explicit central-difference/Störmer–Verlet integrator. The five mode-energy
series will be compared with the digitized LA-1940 Fig. 1 features. Controls
and tolerances are in [`protocol/v1.md`](protocol/v1.md); the machine-readable
runner input is [`protocol/v1.json`](protocol/v1.json).

The reference image and CSV are digitized from the public-domain OSTI/LANL
scan. They are calibration evidence, not the original numerical dataset.

## Run

```sh
uv run python experiments/physics/fput-recurrence-reproduction/run.py
```

## Result

Protocol status: frozen, not yet run. A later milestone will add the runner
and promote measured results to
`knowledgebase/studies/physics/fput-recurrence-reproduction.md`.
