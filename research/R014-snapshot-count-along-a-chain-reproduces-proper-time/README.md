---
id: R014
title: Snapshot count along a chain reproduces proper time
status: done
tags: [physics, relativity, discrete-spacetime, causal-sets]
derived_from: [Q002]
created: 2026-09-22
updated: 2026-09-22
tests: []
---

# R014 — Snapshot count along a chain reproduces proper time

Origin: the derivation [Q002](../../questions/Q002-is-proper-time-a-count-of-snapshots-along-a-worldline.md)
asks for, worked out in conversation on 2026-09-22 and checked numerically.
Units c = 1, 1+1 dimensions unless stated.

| File | What |
|---|---|
| [code/sprinkle.py](code/sprinkle.py) | Poisson sprinkling, longest chain by the Ulam reduction, the three checks below |
| [code/sprinkled-spacetime/index.html](code/sprinkled-spacetime/index.html) | One-canvas interactive companion: worldline, twin turnaround, tilted rod slab, whole-scene boost and lattice control |

## Question

Does a Poisson-sprinkled discrete spacetime, with "snapshot count" defined as
the length of the longest chain, give (a) the √(1 − v²) rate, (b) mutual time
dilation between passing observers with no preferred frame, and (c) length
contraction as a change of antichain? If so, the snapshot picture in Q002 is
causal set theory seen from inside one worldline; whatever fails is the
picture's own content. No hypothesis is tested; this item answers a question.

## Method

### Interactive companion

From the repository root, run `make serve` and open
[the web sim](http://localhost:8000/research/R014-snapshot-count-along-a-chain-reproduces-proper-time/code/sprinkled-spacetime/).
It was scaffolded with `_lib/tools/new-sim.sh R014 sprinkled-spacetime --kind web`
and uses the shared `canvas2d.js`, `panel.js` and `loop.js`.

Drag **Velocity v** to change the path on one fixed realization. **Twin
turnaround** holds the departure and reunion fixed and draws the unconstrained
longest chain alongside the sum of two chains forced through a virtual kink.
**Rod + tilted slab** shows a stationary worldtube and the slab intersection;
changing **Slab observer w** unlinks that observer from v. **Moving-observer
view** applies the boost at v to every dot and geometric layer. **Regrid**
switches to a square lattice of the same density. **Resprinkle** advances the
seed; **Animate v** sweeps velocity without regenerating the fabric. Layer
toggles, sliders and buttons also work with the keyboard.

The model uses c = 1, T = 6, density ρ = 64, rod length ℓ = 3.5 and observer
slab thickness Δt′ = 0.55. Independent, seeded unit tiles each draw a Poisson
number of events, then uniform locations. Tiles are generated as needed in
the inverse-transformed viewport so boosting exposes no artificial empty
boundary. Changing view preserves the original events and measured regions;
the fixed camera can clip their display without changing their counts.
The lattice has spacing a = 1/8 and includes null links.

The sim reconstructs actual longest chains in O(n log n), with null-coordinate
ties handled for the lattice. Counts exclude the artificial endpoint and
turnaround markers (the older Python helper adds two endpoint markers).
The two segment chains cannot exceed the unconstrained chain, but finite
samples can tie; forcing a virtual waypoint can reduce the count even at v = 0.
The rod inset shows the noisy estimate N/(ρΔt′) with an analytic ℓ/γ tick,
not a noiseless count presented as a measurement. The slab's lower edge is
t = 3 + wx and its rest-frame thickness is Δt′/γ(w).

Run the standalone scientific checks with:

```sh
node --test research/R014-snapshot-count-along-a-chain-reproduces-proper-time/code/sprinkled-spacetime/model.test.mjs
```

These check Poisson mean and variance, reproducible tile regeneration, boosted
viewport coverage against brute enumeration, chain reconstruction against an
independent quadratic causal-order solver, boost invariance, twin constraints,
slab geometry, ensemble count scaling and the lattice's coordinate-time count.
They validate the implemented model, not an independent physical hypothesis.

### Derivation and original numerical experiment

**Setup.** Sprinkle points into Minkowski space by a Poisson process of density
ρ. x ≺ y iff y lies in x's causal future. The snapshot count between events
p ≺ q is L(p,q), the number of elements on the longest chain from p to q.
Brightwell and Gregory (1991): E[L] → m_d (ρV)^{1/d} as ρV → ∞, where V is the
volume of the causal diamond between p and q, m₂ = 2 and m₄ ≈ 2.2.

**(a) Rate.** In light-cone coordinates u = t − x, v = t + x the diamond from
the origin to (t, x) is the rectangle 0 ≤ u ≤ t − x, 0 ≤ v ≤ t + x, so
V = ½(t² − x²) = τ²/2 and

  E[L] = 2 √(ρτ²/2) = τ √(2ρ).

In d dimensions V ∝ τ^d, so L ∝ ρ^{1/d} τ: linear in proper time in every
dimension. An inertial worldline at velocity v has τ = t√(1 − v²), so the
count per unit reference time is √(2ρ)·√(1 − v²). No frame enters: V is
Lorentz-invariant and a Poisson sprinkling has no preferred direction
(Bombelli, Henson, Sorkin 2009).

Two corollaries. For a curved worldline, chop it into segments with ρV_i ≫ 1
and sum: ∫√(1 − v²) dt with the same constant, and only each segment's
velocity enters, which is the clock hypothesis. The single longest chain
between the endpoints is the geodesic's count and exceeds any summed curved
path: the twin paradox. And L fluctuates: in 1+1 the longest chain is Ulam's
longest-increasing-subsequence problem, whose spread scales as (ρV)^{1/6}
(Baik, Deift, Johansson 1999; Tracy–Widom), so a sand clock carried along a
path has grain-count noise ∝ τ^{1/3}.

**Lattice control (analytic).** On a square lattice of spacing a in the (t, x)
plane, every causal step advances t by at least a and steps (a, 0), (a, ±a)
are all allowed, so the longest chain from the origin to (t, vt) is t/a for
every |v| < 1. The count is the lattice frame's coordinate time; there is no
dilation at all. A regular sprinkling smuggles in a frame and fails (a).

**(b) Mutual dilation.** Observers A and B meet at O with relative velocity v.
For P on A's line, L(O,P) = kτ_A with k = √(2ρ). The event Q on B's line that
A calls simultaneous with P has τ_B = τ_A√(1 − v²), so L(O,Q) = L(O,P)√(1 − v²).
With the roles swapped B picks a different pair (P′, Q′) and finds
L(O,P′) = L(O,Q′)√(1 − v²). Both hold at once because each count is an
invariant volume; the only frame-dependent input is which pair of events is
compared, i.e. which maximal antichain is called "now". The symmetry lives in
the chains, the asymmetry in the antichain, and the sprinkling owns no
antichain of its own.

**(c) Length contraction.** A rod of rest length ℓ is two parallel worldlines;
the strip W between them is its worldtube. A rest-frame slab of thickness Δt
(a thickened constant-t antichain) cuts an ℓ × Δt rectangle out of W with
expected count ρℓΔt. A moving observer's slab 0 ≤ t′ ≤ Δt′, with
t′ = γ(t − vx), cuts the parallelogram 0 ≤ x ≤ ℓ, vx ≤ t ≤ vx + Δt′/γ out of the
same W: area ℓΔt′/γ, expected count ρℓΔt′√(1 − v²). Elements per unit slab
thickness is the only length a causal set offers without a spatial metric,
and with that definition the moving rod is ℓ√(1 − v²).

**Numerics.** `code/sprinkle.py` sprinkles the diamond in light-cone
coordinates, takes the longest chain as the longest non-decreasing
subsequence of v after sorting by u, and runs (a) at ρ = 2000, t = 1 over
seven velocities; the noise exponent over ρV = 10²…10⁵; and the slab count at
ℓ = 1, Δt′ = 0.05. 200 trials each, seed 2026, three seconds on a laptop.

## Result

All three fall out.

(a) Chain count from the origin to (1, v), 200 trials:

| v | ⟨L⟩ | sd | ⟨L⟩/⟨L_rest⟩ | √(1 − v²) | τ√(2ρ) |
|---|---|---|---|---|---|
| 0.00 | 59.72 | 2.96 | 0.992 | 1.000 | 63.25 |
| 0.30 | 57.08 | 2.67 | 0.948 | 0.954 | 60.33 |
| 0.60 | 47.69 | 2.53 | 0.792 | 0.800 | 50.60 |
| 0.80 | 35.80 | 2.40 | 0.595 | 0.600 | 37.95 |
| 0.90 | 26.02 | 2.04 | 0.432 | 0.436 | 27.57 |
| 0.95 | 18.31 | 1.67 | 0.304 | 0.312 | 19.75 |
| 0.99 | 8.51 | 1.39 | 0.141 | 0.141 | 8.92 |

The ratio tracks √(1 − v²) to within 1% down to v = 0.99. The absolute count
sits ~6% below the asymptotic 2√(ρV) at ρV = 1000, the known slow approach of
the Brightwell–Gregory constant from below; the ratio cancels it.

(b) Spread of L against ρV: sd = 1.59, 2.52, 3.64, 5.43 at ρV = 10², 10³, 10⁴,
10⁵. Fitted exponent 0.176 against the Tracy–Widom 1/6 = 0.167.

(c) Elements of the worldtube inside a moving observer's slab:

| v | ⟨count⟩ | sd | ρℓΔt′√(1 − v²) |
|---|---|---|---|
| 0.00 | 99.6 | 9.3 | 100.0 |
| 0.60 | 80.9 | 9.5 | 80.0 |
| 0.80 | 60.4 | 8.1 | 60.0 |
| 0.95 | 30.3 | 5.7 | 31.2 |

**Reading against Q002.** The snapshot picture is causal sets seen from inside
one chain. The "persistent frame at c" reading is V = 0 ⇒ E[L] = 0 and adds
nothing to the null interval. The one thing the picture carried that causal
sets do not is a global sequence, and that is exactly what must go: within a
single worldline order and sequence coincide, globally there is no sequence,
and putting one in (the lattice) destroys (a). The "frame-independent limit on
frames per distance" does not exist as a rate cap: the only invariant cadence
is ρ, snapshots per unit spacetime *volume*; snapshots per unit distance along
a path are √(2ρ)√(1 − v²)/v, unbounded at low v and zero at c. The speed of
light is where the diamond's volume vanishes, not a ceiling on a rate.

**The scan picture of length contraction** (raised alongside Q002: a frame as
a scan of the rod from the ends inward, faster rod ⇒ shorter scan ⇒ collapse)
is the tilted-slab statement in (c) as a slogan and wrong as a mechanism. An
ends-inward scan samples both ends at the same instant and records exactly ℓ,
displacing only the middle. A one-way scan changes the recorded length by
±v × (scan delay) with the sign set by scan direction, so front-to-back
stretches; relativity never stretches and depends on no scan rate. Scan speed
belongs to the scanner, not the rod. The salvageable core: in the rod's rest
frame the moving observer's "now" is a rear-first scan with the front end
sampled vℓ later, but the rod is at rest there and the ends are still ℓ apart;
the contraction comes from the observer's ruler sliding v·vℓ during the scan,
times the γ of the ruler's own contraction, γℓ(1 − v²) = ℓ/γ. The rod never
collapses, and it says the same about the observer's rod. A literal camera
scan (light travel time) gives Terrell–Penrose rotation, not contraction.

## Limitations

- Lorentz invariance is put in, not derived: the sprinkling is Poisson *in
  Minkowski space*. The count reproduces proper time given the metric; it does
  not explain why c is frame-independent. Q002's last bullet stands.
- (c) is length contraction as an element count per slab thickness. It is not
  a spatial distance, which remains an open problem in causal set theory
  (Rideout and Wallden 2009).
- Numerics are 1+1 only, where V = τ²/2 and the Ulam reduction apply. In 3+1
  the argument is the same (V ∝ τ⁴, L ∝ ρ^{1/4}τ) but m₄ is only known
  numerically and the fluctuation exponent differs.
- The original Python lattice control is analytic. The interactive companion
  now constructs and counts the lattice explicitly; its chain has 47 sampled
  events for T = 6 across the displayed velocity range, excluding endpoints.
- (b) is a derivation on top of (a); the numerics do not construct the two
  observers' antichains explicitly. A maximal antichain in a sprinkling is a
  jagged object and its correspondence to a smooth "now" needs thickening
  (Major, Rideout, Surya 2009).
- ⟨L⟩ at ρV = 1000 is 6% under the asymptotic constant; the ratios in (a) are
  the evidence, not the absolute counts.

## Next

- A hypothesis is the productive form of what this leaves: *c is not a rate
  limit on snapshots but the vanishing of the causal diamond's volume; the only
  invariant cadence is ρ.* Q002 was kept a question because it was not yet a
  claim a run could come out against; that one is.
- If the τ^{1/3} clock noise is worth pursuing as a prediction, the 3+1
  fluctuation exponent of the longest chain is the number to pin down
  numerically; it is not Tracy–Widom there.
- Construct the two observers' thickened antichains explicitly in the
  sprinkling and count (b) directly rather than via (a).
