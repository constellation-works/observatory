---
title: "The swirl-ball electron and the photon correspondence"
status: resolved
families: [swirl-photon]
almanac: 15-discussions/26-06/swirl-photon-correspondence.md
created: 2026-07-09
updated: 2026-08-20
---

# The swirl-ball electron and the photon correspondence

**The idea.** An accelerating electron sheds a detaching vortex ("the swirl") — is that swirl
a photon? Opened with *"the swirl is the photon, no?"* and landed, after walking the
Maxwell→QED chain, on the precise answer: **the swirl is the classical state of the field
mode whose quanta are photons.** The correspondence is real and the sims render it; the fully
classical reading is blocked by single-photon phenomenology.

Doc status is `resolved`: this line converged with established physics rather than dying —
kept as the correspondence record the other threads build on.

## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| The turn sheds a genuinely detaching 1/r field (radiation) distinct from the bound 1/r² velocity field | supported | [swirl-ball](../../orrery/lab/sims/swirl-ball/) (v6 renders both: gold bound field, cyan radiation kink); standard Liénard–Wiechert / Purcell kink construction |
| The detached swirl is self-sustaining in the far zone (E and B regenerating each other, carrying energy, momentum, angular momentum) | supported | the standard source-free Maxwell radiation solution — concretely, the 1/r acceleration term [swirl-ball](../../orrery/lab/sims/swirl-ball/) computes exactly and renders detaching from the bound field. **Audit 2026-08-20:** [swirl-ball-far-field](../../orrery/lab/sims/swirl-ball-far-field/) is illustration only, not the previously claimed "free wave-equation solution" — its rings are spawned at the emitter and expanded kinematically, with their count set by the emission-density slider, so any apparent discreteness or pocket structure is put in by the renderer, not emergent. The source-free-solution citation belongs in the same `../studies/` note as the antibunching row |
| The swirl *is* a photon, classically | refuted | a one-photon state has ⟨E⟩ = 0 everywhere, and Grangier–Roger–Aspect antibunching (1986) shows a single photon never triggers both beamsplitter outputs while self-interfering — needs a `../studies/` note to carry the citation properly |
| The swirl is the classical field mode whose quantized excitations are photons | supported | the resolution of the thread; consistent with both sims and the antibunching constraint |

## Where it feeds

- [vortex-electron](vortex-electron.md) leans on this correspondence for its photon objection
  (interference from the mode, discreteness only at detection).
- Asset: `../../orrery/lab/sims/swirl-ball/assets/photon-field.png` — the captured frame the almanac note
  embeds.
