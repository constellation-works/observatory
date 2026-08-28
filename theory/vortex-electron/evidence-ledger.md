## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| The friction-vortex response rule (outcome = sign(axis · current), deterministic or stochastic) reproduces single-particle spin statistics | supported | [vortex-bell](../../../orrery/lab/sims/vortex-bell/) `vortex_bell.py` — contextual single-spin behavior works, echoing Bell's own 1964 single-spin model |
| The same rule reproduces two-particle Bell correlations | refuted | [vortex-bell](../../../orrery/lab/sims/vortex-bell/): optimized over all detector settings, \|S\| saturates at exactly 2.000; E(22.5°) = −0.75 vs QM's −0.924; corkscrew and tilt-enumeration variants (`corkscrew_bell.py`, `tilt_enumeration.py`) hit the same ceiling |
| Nature itself respects the \|S\| ≤ 2 ceiling (so the model could still be right) | refuted | loophole-free experiments measure \|S\| ≈ 2.4–2.7 — [studies/chsh-bounds](../../studies/chsh-bounds.md) |
| A tabletop analog (ping-pong balls with hidden tilt axes) demonstrates the classical ceiling empirically | supported | [pingpong-bell](../../../orrery/lab/sims/pingpong-bell/): protocol + analysis give \|S\| = 1.49 ± 0.17 on sample data — within the classical bound, as any local mechanism must be (protocol: almanac `20-projects/pingpong-bell/`) |
