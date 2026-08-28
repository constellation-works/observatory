## The superposition adjudication — the ORB-10157 measurement

The second derivation gate has run (faraday,
[lattice-two-source-superposition](../../../orrery/lab/sims/lattice-two-source-superposition/),
seed 42): a 129² shared-budget counting lattice — 50,000 anonymous slots per cell, full
outer reservoir — embeds a compact one-cell source (peak exposure 0.1) at the center of an
extended uniform-disk depletion well (radius 0.31 lattice widths) and measures the source's
paired field (the radial gradient of its increment to stored scarcity, projected onto its
isolated-source gradient over radii 4–18 cells) as ambient depletion D sweeps 0.01–0.90 in
12 levels, with the full profile recorded to D = 0.995. Depletion is literally anonymous:
every attempt picks a slot blind to source and state (survivors sampled exactly as
Binomial(C, e^(−H))), and compact hits can clear only slots the background left alive. All
12 seeded finite-count means (32 replicates each) lie within 2.31 standard errors of the
exact expectation; reruns are byte-identical.

| Candidate superposition law | Reading it operationalizes | log-RMSE (D ≤ 0.90) | Verdict |
|---|---|---|---|
| A = 1 (independence) | the exemption ORB-10097 called "screened": the Sun generates as if alone, ephemerides exactly Newtonian | 1.074 | refuted |
| A = 1/(1−D) (inverse-headroom enhancement) | the shared budget amplifies an embedded source's field | 2.077 | refuted — and no exhaustion upturn appears even at D = 0.995 (amplitude 0.0029 of isolated) |
| A = 1−D (plain local headroom) | turn 7: wells dug from remaining capacity | 0.0711 | right family |
| **A = (1−D)^1.07079 (measured)** | survivor-fraction screening; the exponent's excess over 1 is annulus geometry (headroom varies across the 4–18-cell band) | **0.0031** | **the mechanic's answer** — resolution checks 1.0725 (97²) / 1.0700 (161²), amplitude shifts ≤ 4.4×10⁻⁴ |

**The adjudication: which premise of the ORB-10156 derivation fails.** The derivation ran:
the fitted boost is a position-dependent coupling G_eff(r) = G·q(r)/q(R₀) keyed to
accumulated background depletion; depletion on a shared budget is anonymous; *therefore* an
embedded source generates with the background's coupling — the fitted factor, with its
fitted gain. The apparatus is faithful to the mechanic as stated — anonymity is implemented
literally, and the stored field is the model's additive draw bookkeeping (removals per
cell), not some second convention — so the inapplicability defense is not available. What
the measurement shows is that the anonymity premise proves less than the derivation drew
from it. Anonymity establishes only that an embedded source is *not exempt* from the shared
budget (independence: refuted). The modulation the budget itself supplies is the trivial
counting factor — a source's attempts can clear only surviving slots, so its field carries
exactly one factor of local survivor fraction, (1−D)^1.07, unit gain, keyed to *local
occupancy*. The derived rule needed something anonymity does not provide: a coupling that
responds to the *accumulated* dilution level with the fitted gain β. No counting rule in
the mechanic does that, and faraday's declared scope caveat names the gap exactly — a rule
whose depletion-attempt rate varies with occupancy is a *different microscopic model*.
**The failing step is the transplant:** "generates with the background's coupling" silently
substituted the fitted macroscopic factor for the mechanic's actual transfer function,
which had never been computed. The `supported` verdict is superseded and stays on the
ledger as the record of that mistake.

Two sign facts keep the bookkeeping honest, because the branch names have become
treacherous. First, the measured "screening" is *not* ORB-10097's "screened branch": that
branch meant exemption — the Sun's own depletion pins the local level, the galactic factor
never reaches its generation, ephemerides come out exactly Newtonian — which on the lattice
is the *independence* candidate, and it is refuted; what ORB-10156's point 3 argued against
the exemption survives with its variable transposed. Second, the refuted "multiplicative
enhancement" is not the sign ORB-10097 integrated: the integrated factor
exp[(βF(R₀)/R₀²)(r_gal − R₀)] makes the Sun's field *weaker* where galactic depletion is
higher — suppression-signed, like the measured law. What ORB-10097 imported that the
mechanic does not supply is the gain and the variable, not the direction.

**Relation to the fitted form — which reading the rotation-curve fit actually tested.** The
measured law is the original turn-7 headroom idea, returned by the mechanic itself at unit
gain: turn 9's ODE was ds/dr = G₀(1−s)·M(r)/r² — effective G proportional to remaining
headroom — and "wells dug from remaining capacity" is literally what the apparatus measured.
The fitted q(r) form is that rule in continuum dress with the gain promoted to the fitted β
on *accumulated* dilution. So the measured law sits squarely in the fitted form's own family
— headroom suppression, boost rising where depletion falls — where the enhancement
operationalization was its sign-mirror. What the ORB-10077/ORB-10082 fit tested was
therefore the *shape as phenomenology*: q(r) with one free gain, decisively better than the
no-halo control regardless of microscopic carrier. What it never tested is the carrier —
and the measured carrier reproduces the fitted boost only under a demanding identification:
for (1−D_gal(r))^1.071 to equal the fitted 0.70 → 1.36 boost across 5–18.75 kpc, ambient
*occupancy* depletion must vary O(1) across the disk (headroom ratio ≈ 1.94^(1/1.07) ≈ 1.86,
i.e. D ≳ 0.46 at 5 kpc even with the outer band fully undepleted) — a normalization
statement about how much lattice occupancy the Galaxy's mass consumes that the
accumulated-dilution picture never made and nothing has fixed. The alternatives now on the
table are sharper than multiplicative-vs-screened ever was: (i) the fitted boost *is* the
measured screening law, at O(1) galactic occupancy depletion; (ii) the boost requires a new
occupancy-coupled generation rule carrying the fitted gain — faraday's "different
microscopic model", owing its own lattice test; (iii) the boost is phenomenology the
counting mechanic does not carry.

**The ORB-10097 consequence, stated precisely.** The Uranus tension attached to the model
through the claim that the mechanic itself hands the Sun the fitted factor. Measured, it
does not — so the tension is **conditioned: neither detached nor retained outright**. On
reading (i), everything ORB-10097 integrated stands unchanged, because the boost's local
log-gradient at R₀ is a property of the fitted shape, not of its carrier: any multiplicative
modulation reproducing the fitted boost hands the Sun's field the same 3.2×10⁻¹⁰/AU
differential, and the 1.89×-rms primary-orientation excess (six-axis envelope 0.66–3.0×) is
again the model's own. On readings (ii)/(iii), ORB-10097's integration tested a rule the
mechanic doesn't have, and no solar-system prediction exists until the occupancy
normalization or the new coupling is fixed. What no reading recovers is the free escape:
the exemption branch that would have left ephemerides exactly Newtonian is the lattice's
independence candidate, measured dead at log-RMSE 1.074. The ORB-10097 ledger row carries
the condition; its integrated numbers are unretired.

**Apparatus caveats, and what they gate.** Three, all declared by faraday. (i) *2D static
pinned geometry:* both sources are fixed exposure maps on a 129² lattice (97² and 161²
checks move the exponent by ≤ 0.002), not emergent, moving, or self-consistently digging
depleters. (ii) *Anonymous fixed-coupling attempts:* the depletion-attempt rate never
responds to occupancy — one microscopic reading of "shared budget", and exactly the
mechanic as stated in every prior sim. (iii) *Declared, not emergent, profiles:* the
Poisson-solved exposure maps say where attempts land; superposition enters only through the
shared slots. None gates the verdict on the mechanic *as stated* — fidelity on (ii) is the
point of the experiment, and (i)/(iii) are the same declared-geometry idealization every
static-sector sim in this ledger uses. All three gate *extrapolation*: an occupancy-coupled
rule (reading (ii) of the fitted-form question above) is untested by construction, and a
moving or emergent source could in principle superpose differently — no current rule
supplies a mechanism for either, and conjuring one is new model-building, not this
measurement's problem. Cross-reference: the parent's boost citations in
[two-substance-vortex-vacuum](../two-substance-vortex-vacuum/) (§A3 and its Branch A ledger
rows) are updated to carry the same conditioning.
