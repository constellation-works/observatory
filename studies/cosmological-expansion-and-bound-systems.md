---
title: "Cosmological expansion and bound systems — where expansion reaches, and where it does not"
status: active
created: 2026-08-08
updated: 2026-08-08
---

# Cosmological expansion and bound systems

The wall around any claim in this corpus that cosmic expansion does something to a galaxy, a solar
system, or an atom. The short answer is that bound systems do not expand: the cosmological
contribution to local dynamics is a tidal term, it is \(2\times10^{-4}\) of self-gravity at the
visible edge of a galaxy, and it only wins at ~1 Mpc — where it does something real and observed,
namely set the maximum size of a bound structure.

This note exists because the naive intuition ("space expands, so things in it get stretched") has
two seductive numerical near-coincidences attached to it, both recorded below. Neither survives.
The single most useful correction to the intuition is that **locally, dark energy is a centrifugal
term** — same equation, same effective potential, \(\omega^{2}=\Lambda c^{2}/3\). Everything else
here follows from that.

## The local equation of motion

Carve a bound system out of the cosmological fluid (Einstein–Straus vacuole; exterior
Schwarzschild–de Sitter). In the locally inertial Fermi normal frame — the frame relevant to
astronomical observation — the radial equation of motion picks up one extra term:

\[
\ddot r=-\frac{GM}{r^{2}}+\frac{\Lambda c^{2}}{3}\,r .
\]

Two things about that term matter and are routinely gotten wrong.

**It is \(\Lambda c^2/3\), not \(\ddot a/a\) of the background FRW solution.** A local bound system
sits in an overdense region that has decoupled from the cosmic mean; the mean matter density is not
acting on it in addition to its own \(GM/r^2\). What survives in the vacuole exterior is the
vacuum-energy piece alone. Numerically \(\Lambda c^{2}/3=\Omega_\Lambda H_0^{2}\):

| \(H_0\) (km/s/Mpc) | \(\Lambda c^{2}/3\) (s\(^{-2}\)) |
|---|---|
| 67.4 | 3.29×10⁻³⁶ |
| 70.0 | 3.55×10⁻³⁶ |
| 73.0 | 3.86×10⁻³⁶ |

(\(\Omega_\Lambda=0.69\); \(\Lambda\approx1.19\times10^{-52}\ \mathrm{m^{-2}}\).) The \(H_0\)
tension moves this by <20%, and moves every length scale below by <6%.

**Its sign follows \(\ddot a\), so it has not always pushed outward.** Under matter domination
\(\ddot a<0\) and the cosmological term is *compressive*. The outward push is a late-time,
\(\Lambda\)-dominated feature. Any argument that expansion has been stretching bound systems
throughout cosmic history has the sign backwards for most of that history.

**Sign of the effect on orbits.** A *weaker* effective potential moves bound orbits **outward**, not
inward. There is no regime in which weakening the binding contracts a galaxy.

## The rotating-frame correspondence

The single most useful intuition for everything below. Compare the local de Sitter problem with a
Newtonian orbit written in a **rotating frame**:

| | equation of motion | effective potential |
|---|---|---|
| rotating frame | \(\ddot r=-GM/r^{2}+\omega^{2}r\) | \(-GM/r-\tfrac{1}{2}\omega^{2}r^{2}\) |
| local de Sitter | \(\ddot r=-GM/r^{2}+\tfrac{\Lambda c^{2}}{3}r\) | \(-GM/r-\tfrac{1}{6}\Lambda c^{2}r^{2}\) |

They are the same problem with \(\omega^{2}=\Lambda c^{2}/3\). **Locally, dark energy is a
centrifugal term.** The crossing radius is then the same formula in both cases,
\((GM/\omega^{2})^{1/3}\), which is why the maximum turnaround radius below has three familiar
cousins:

| system | \(\omega\) | crossing radius |
|---|---|---|
| Earth, one rotation per day | \(7.29\times10^{-5}\) s⁻¹ | 42,163 km — the geosynchronous radius |
| Earth in the Sun's field | orbital | 1.50×10⁶ km — the Hill radius |
| \(10^{12}M_\odot\) galaxy | \(\omega_\Lambda=1.88\times10^{-18}\) s⁻¹ | 1.08 Mpc — the max turnaround radius |

\(\omega_\Lambda\) corresponds to a "rotation period" of **106 Gyr**, about 7.7× the age of the
universe. That single number is why the effect is invisible at galaxy scales.

The Hill sphere is also the right precedent for the all-or-nothing behaviour: a moon inside it stays
bound, outside it is stripped, and nobody describes a moon as *partially* stripped.

**Where the correspondence breaks.** Rotation has an axis; \(\Lambda\) does not. As tidal-field
eigenvalues:

| source | eigenvalues | trace |
|---|---|---|
| tide from a distant mass | \((-2,+1,+1)\times GM/d^{3}\) | 0 — as vacuum requires |
| rotation | \((0,+1,+1)\times\omega^{2}\) | \(2\omega^{2}\), and picks out an axis |
| de Sitter | \((+1,+1,+1)\times\Lambda c^{2}/3\) | \(\Lambda c^{2}\), isotropic |

So de Sitter behaves like rotation about every axis at once. The nonzero trace is
\(\nabla^{2}\Phi=-\Lambda c^{2}\neq0\) everywhere — legitimate here, because vacuum energy genuinely
is a source filling space, in contrast to the delayed-center postulate refuted on exactly this
diagnostic in
[theory/moving-source-field-consistency](../theory/moving-source-field-consistency.md).

**Do not import the fluid.** A common mental image for "expansion pushes things apart" is a stirred
medium — a spinning object dragging particles, nearby ones carried along, distant ones flung off.
That picture has a driven source doing viscous work on a material, with real dissipation and real
energy transfer, and it is the origin of the energy objection answered in the next section. The
correct analogy is the *rotating frame*, which has no medium, no viscosity, and nothing being
driven.

## Where does the energy go?

The natural objection: if a bound system "resists" expansion, something must be paying for it —
orbits should decay, atoms should give up energy somewhere. They do not, and the reason is
structural rather than a matter of small numbers.

**The local problem is conservative.** The cosmological term derives from a potential,
\(V(r)=-GM/r-\tfrac{1}{6}\Lambda c^{2}r^{2}\), so \(E=\tfrac{1}{2}v^{2}+V(r)\) is a constant of the
motion. Inspect the equation of motion: it contains \(r\); it contains **no** \(\dot r\).
Dissipation requires a velocity-dependent term and there is none, so there is no mechanism capable
of draining an orbit. A static potential does zero net work around a closed orbit, exactly as the
Sun's gravity does zero net work on Earth despite pulling for 4.5 Gyr. Numerically, an eccentric
orbit integrated over many periods holds its apsides with \(|\Delta E/E|\) at integrator noise.

**And it is conservative for a reason, not by accident.** Schwarzschild–de Sitter is a *static*
metric — the static patch has a timelike Killing vector — so Noether hands you an exactly conserved
energy for a local bound system. Nobody asks where the energy goes for a satellite at
geosynchronous orbit; the centrifugal term is a static potential too.

Scale for an atom: the \(\Lambda\) force on the electron in hydrogen is \(1.7\times10^{-76}\) N
against a Coulomb force of \(8.2\times10^{-8}\) N — a fractional perturbation of
\(2\times10^{-69}\), applied once.

**But energy is genuinely not conserved in cosmology**, and this should be conceded plainly rather
than argued around. Photons redshift and the energy is not transferred anywhere. Dark-energy density
stays constant while comoving volume grows, so the total increases without bound and nothing pays
for it. The reason is Noether again, run backwards: conservation requires time-translation
symmetry, FRW has no timelike Killing vector, so there is no globally conserved energy whose
disappearance needs explaining. "Where did it go" presupposes a symmetry the spacetime lacks.

The distinction that matters: **that pathology lives entirely in the unbound sector** — photons in
transit, the expanding background, free particles whose peculiar momentum decays as \(p\propto1/a\).
Bound systems are precisely the ones sitting in a static patch with a conserved energy. The energy
weirdness is the reason bound systems are the boring case, not a hole in the argument.

### What a real energy sink looks like

The structural argument above is worth pairing with the empirical one, because orbits *do* drift and
we *do* measure it — and in every case there is an identifiable sink. The contrast is the point.

| system | measured drift | sink |
|---|---|---|
| Earth's orbit | **expands** ~1.4 cm/yr | solar mass loss, \(\dot M\approx5.8\times10^{9}\) kg/s (radiation + wind), \(a\propto1/M\) |
| Earth–Moon | recedes ~3.8 cm/yr | tidal friction, paid out of Earth's rotational angular momentum |
| PSR B1913+16 (Hulse–Taylor) | orbit decaying | gravitational-wave emission — matches GR's quadrupole formula to **0.2%** over three decades ([arXiv:1407.3404](https://arxiv.org/pdf/1407.3404), [arXiv:1402.5594](https://arxiv.org/pdf/1402.5594)) |
| WASP-12b | transits arrive **29 ± 2 ms/yr** earlier, decay timescale 3.25 ± 0.23 Myr | tidal dissipation into the star; decay favored over apsidal precession by a Bayes factor of \(7\times10^{4}\) ([ApJL 2019](https://iopscience.iop.org/article/10.3847/2041-8213/ab5c16), [arXiv:1911.09131](https://arxiv.org/abs/1911.09131)). Rate is too fast for equilibrium tides; obliquity tides proposed ([arXiv:1812.01624](https://arxiv.org/abs/1812.01624)) |
| dark energy, any bound orbit | 13.4 pm for Earth, once, total | **none** |

Hulse–Taylor is the decisive case for any "the energy has to go somewhere" objection: when a sink
exists, the orbit decays, the budget balances, and the agreement is at the 0.2% level. The absence
of expansion-driven decay is therefore not an unexplained silence — it is what "no sink" looks like,
measured against four systems where there is one.

Note also the sign: the largest real secular effect on Earth's orbit makes it **grow**, from the Sun
losing mass, and even that is \(\sim10^{9}\times\) the total dark-energy offset.

## "But expansion need not weaken the potential, if expansion is itself gravitational"

A natural objection to the sign discussion above: expansion is not some external agent diluting the
potential — in general relativity the expansion *is* gravitational dynamics, so perhaps the local
potential simply does not weaken and no size change follows. Three separate things are tangled
here, and they come apart cleanly.

**1. The conclusion is right, and the standard reason is stronger than the argument.** A virialized
galaxy's potential is set by its own \(M\) and \(R\); it is not a function of the scale factor at
all. The system decoupled from the expansion when it collapsed — that is the content of the
all-or-nothing result. So "the potential does not weaken" is correct, but it holds because bound
systems ignore expansion entirely, not because two effects happen to offset.

**2. "Expansion driven by gravity" has a sign problem.** The Friedmann acceleration equation is

\[
\frac{\ddot a}{a}=-\frac{4\pi G}{3}\left(\rho+\frac{3p}{c^{2}}\right).
\]

For ordinary gravitating matter (\(p=0\)) this is negative: **gravity decelerates expansion**.
Gravity is what fights expansion, not what drives it. Acceleration requires \(p<-\rho c^{2}/3\),
i.e. \(w<-1/3\) — which is the dark-energy problem restated, not a route around it. Any proposal
that expansion is gravity-driven owes an account of a gravitating source with strongly negative
pressure.

**3. The version that is a real physical proposal is measured, and dead.** If the gravitational
*coupling* tracked the expansion — the natural reading of "these are one phenomenon" — one expects
\(\dot G/G\sim H_0\approx7.2\times10^{-11}\,\mathrm{yr^{-1}}\). This is Dirac's Large Numbers
Hypothesis (1937), \(G\propto1/t\). Lunar laser ranging measures

\[
\dot G/G=(7.1\pm7.6)\times10^{-14}\ \mathrm{yr^{-1}}
\]

(Hofmann & Müller 2018, *Class. Quantum Grav.* **35**, 035015; carried by
[gravitational-time-dilation](gravitational-time-dilation.md)) — consistent with zero and bounding
any tracking at \(\sim10^{-3}\) of \(H_0\). Three orders of magnitude. The same bound already
kills the accumulating variant of
[theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md).

So: the intuition survives as a *conclusion* (local potentials do not track expansion) and dies as
a *mechanism* (the coupling does not track it either, and gravity has the wrong sign to drive
expansion in the first place).

## Magnitude: expansion does not reach galaxy scales

Ratio of the cosmological push to self-gravity, \(\left(\Lambda c^{2}/3\right)R^{3}/GM\):

| system | ratio |
|---|---|
| Milky Way inside 15 kpc | 4.4×10⁻⁵ |
| Milky Way-ish, 30 kpc (visible disk edge) | 2.1×10⁻⁴ |
| \(10^{12}M_\odot\) halo, 100 kpc | 7.9×10⁻⁴ |
| \(10^{12}M_\odot\) halo, 300 kpc (virial) | 2.1×10⁻² |
| Local Group, 1 Mpc | 1.6×10⁻¹ |

At the visible edge of a galaxy the cosmological term is **0.02% of the galaxy's own gravity**.
This is why Cooperstock, Faraoni & Vollick, computing the cosmological correction in the Fermi
normal frame, find the effect insignificant at solar-system, galactic, *and* cluster scales
([astro-ph/9803097](https://arxiv.org/pdf/astro-ph/9803097)).

The deeper structural result is Price & Romano's: a bound system exhibits **"all or nothing"**
behaviour — after initial transients it either completely follows the cosmological expansion or
completely ignores it, with no partial stretching
([gr-qc/0508052](https://arxiv.org/abs/gr-qc/0508052);
[Am. J. Phys. 80, 376](https://pubs.aip.org/aapt/ajp/article/80/5/376/1045862/In-an-expanding-universe-what-doesn-t-expand)).

The mechanism is the effective potential of § The rotating-frame correspondence, and it is
junior-level mechanics rather than relativity. Gravity falls as \(1/r^{2}\); the cosmological push
grows as \(r\). Two such curves cross **once**, and the crossing is *unstable*, so \(r_c\) is a
barrier maximum.

### The valley exists — it just does not migrate

An earlier draft of this note said "no stable minimum exists," which is wrong and worth correcting
explicitly. That is true only for the radial (\(L=0\)) problem. Any *orbiting* body carries angular
momentum, and

\[
V_{\rm eff}(r)=-\frac{GM}{r}+\frac{L^{2}}{2r^{2}}-\frac{\Lambda c^{2}}{6}r^{2}
\]

does have a stable minimum: \(V_{\rm eff}''=GM/r^{3}-\Lambda c^{2}/3>0\) for \(r<r_c\). **The valley
is the orbit itself**, sitting outside its Newtonian radius by the one-time fractional offset
\(\delta=(\Lambda c^{2}/3)r^{3}/GM\) — 13 picometers for Earth, \(2\times10^{-4}\) at a galaxy's
disk edge.

So the reason there is no secular stretching is not the absence of an equilibrium. It is that
\(\Lambda\) is constant, so **the equilibrium never moves.** Partial stretching would require the
valley to migrate outward with time, and in de Sitter it does not.

The clean statement of all-or-nothing is then a bifurcation rather than an absence: the minimum and
the maximum approach each other as \(r\) grows and **annihilate exactly at \(r_c\)** — a saddle-node.
Inside \(r_c\) a stable orbit exists; outside it, none does. That is the boundary, and it is sharp.

### Caveat: "exactly" is a de Sitter statement

The strict dichotomy, and the exact energy conservation in § Where does the energy go?, hold where
\(\ddot a/a\) is **constant** — i.e. de Sitter. Faraoni & Jacques showed the all-or-nothing
behaviour does not generalise ([0707.1350](https://arxiv.org/pdf/0707.1350)). In a general FRW the
barrier radius moves with time, so the local potential is time-dependent, local energy is *not*
exactly conserved, and a system can in principle cross the barrier. This is a real correction, not a
technicality — but it is still not dissipation (no \(\dot r\) term appears at any stage), and the
residual secular effect on an Earth-like orbit is of order \(10^{-22}\) fractional. Since the
universe is asymptoting to de Sitter, the exact statements become better approximations with time,
not worse. "Galaxies expand a little bit" remains unavailable.

## Where expansion does reach: the turnaround radius

Set the two terms equal. The result is the **maximum turnaround radius** — the largest radius at
which a mass \(M\) can still hold a shell against dark energy:

\[
R_{\rm ta,max}=\left(\frac{3GM}{\Lambda c^{2}}\right)^{1/3}.
\]

Pavlidou & Tomaras show this is independent of cosmic epoch, of the exact nature of dark matter,
and of baryonic effects ([JCAP 09 (2014) 020](https://iopscience.iop.org/article/10.1088/1475-7516/2014/09/020)).
This is the same critical radius as the all-or-nothing barrier above and as the corotation radius of
§ The rotating-frame correspondence — one crossing point, three names.

| \(M\) (\(M_\odot\)) | \(R_{\rm ta,max}\) |
|---|---|
| 10¹¹ | 0.50 Mpc |
| 10¹² | 1.08 Mpc |
| 5×10¹² (Local Group scale) | 1.85 Mpc |
| 10¹³ | 2.33 Mpc |
| 10¹⁵ (rich cluster) | 10.8 Mpc |

\(R_{\rm ta}\propto H_0^{-2/3}\), so the \(H_0\) tension shifts these by 5.5%.

This is a live observational test rather than a curiosity: candidate violations have been reported
at group scale (NGC 5353/4,
[ApJ 815, 43](https://iopscience.iop.org/article/10.1088/0004-637X/815/1/43)), and the bound is
used to constrain the dark-energy equation of state and modified gravity. Note the scale gap that
matters for this corpus: a galaxy's visible disk is ~30 kpc and its turnaround radius is ~1 Mpc —
a factor of ~30 in radius, ~10⁴ in the acceleration ratio.

## The solar-system bound

If bound orbits followed the Hubble flow at \(\dot r=H_0 r\):

| system | Hubble prediction | measured |
|---|---|---|
| Earth–Sun | **10.7 m/yr** (1071 m/century) | reported anomaly 15±4 m/century (Krasinsky & Brumberg 2004); 7±2 m/century (JPL/Standish) |
| Earth–Moon | **2.75 cm/yr** | ~3.8 cm/yr, tidal — see below |

The Hubble prediction for the AU exceeds even the largest *reported* anomaly by **71×**, and the
JPL value by **153×**. Those reported anomalies are themselves of debated significance and have
conventional candidate explanations; the point here is only that they bound any Hubble-following of
the Earth–Sun orbit at ≳70×. This complements
[solar-system-ephemeris-precision-floor](solar-system-ephemeris-precision-floor.md), which bounds
unmodeled *dynamics* over a decade; this row bounds a specific secular scale drift.

### Near-coincidence 1: the lunar recession

The Moon recedes at ~3.8 cm/yr and the naive Hubble prediction is 2.75 cm/yr. These are within 40%
of each other, which is close enough to have repeatedly tempted people into a cosmological reading.
It is wrong, and the discriminator is clean: the lunar recession is accompanied by a *matching*
transfer of Earth's rotational angular momentum — the day is lengthening, and the two effects
balance in a single angular-momentum budget confirmed independently by paleontological tidal
rhythmites. A cosmological stretching would produce the recession with no corresponding spin-down.
The mechanism is over-determined by an observable a cosmological account does not touch.

`conjecture — to verify`: the 3.8 cm/yr LLR figure and the rhythmite lineage are recalled here, not
checked against source in this pass. The angular-momentum argument does not depend on the exact
number.

## Do older galaxies look different? Yes — and it is not expansion

They do, dramatically. High-redshift massive quiescent galaxies ("red nuggets") have effective
radii **2–5× smaller at fixed stellar mass** than the local size–mass relation, some under 1 kpc,
and they are **completely absent** in the nearby universe
([arXiv:1108.0656](https://arxiv.org/pdf/1108.0656);
[EPOCHS VI, arXiv:2309.04377](https://arxiv.org/pdf/2309.04377)). High-\(z\) disks are also
clumpier, more turbulent, lower \(V/\sigma\), and more lopsided.

### Near-coincidence 2: size growth versus the scale factor

Galaxies have grown ~2–5× in effective radius since \(z\approx2\). The scale factor grew **3×**
over the same interval. If one were looking for evidence that expansion stretches bound systems,
this is exactly the number one would point at. Three independent reasons it is not that:

1. **It is type-dependent.** Quiescent galaxies grow substantially more than star-forming galaxies
   at the same stellar mass. Expansion cannot distinguish whether a galaxy is forming stars.
2. **The cores are preserved.** This is the decisive structural test. Expansion would dilute a
   galaxy uniformly, dense center included. What is observed is the opposite: the compact high-\(z\)
   core survives as the center of a local early-type galaxy, with material accreted *around* it.
   Growth is inside-out, not homologous stretching
   ([arXiv:1601.03920](https://arxiv.org/pdf/1601.03920)).
3. **The mechanism is over-determined.** Minor mergers give \(R\propto M^{2}\), which is why size
   outruns mass; current models additionally require supermassive-black-hole core scouring to
   recover the last factor of ~2 and to destroy the progenitors' rotational support
   ([MNRAS 535, 1202](https://academic.oup.com/mnras/article/535/1/1202/7833554)).

Also note the sign trap: "expansion weakens the potential, so galaxy edges shrink" is doubly wrong —
weaker binding moves orbits outward, and the observed evolution builds the outskirts up rather than
stripping them.

## What this bounds in the corpus

- **Any claim that expansion drives internal galactic dynamics** is excluded at \(10^{-4}\) of
  self-gravity at the visible disk edge. Rotation-curve phenomena are ~10⁴ too large to be sourced
  this way.
- **Any substrate/aether model must state its relationship to expansion.** If the substrate comoves
  with the Hubble flow, motion through it is peculiar velocity only. If it does not, distant
  galaxies move through it at a large fraction of \(c\), and the model owes an account of why the
  resulting signatures are absent. See
  [theory/moving-source-field-consistency](../theory/moving-source-field-consistency.md).
- **Structure larger than \(R_{\rm ta,max}\) cannot be bound**, which is a real constraint on any
  proposed large-scale bound configuration, and a live test of ΛCDM in its own right.
- **Two near-coincidences are traps** and should be named as such whenever they appear: lunar
  recession vs \(H_0 r\), and galaxy size growth vs the scale factor. Both are within a factor of
  ~1.5 of the naive cosmological prediction and both have over-determined conventional mechanisms.
- **Any model coupling gravitational strength to cosmic time** faces \(\dot G/G=(7.1\pm7.6)\times
  10^{-14}\,\mathrm{yr^{-1}}\), i.e. \(\lesssim10^{-3}H_0\). "Gravity and expansion are one
  phenomenon" is a measurable claim in that form, and it is excluded by three orders of magnitude.
- **Energy-based objections to any of the above are answered structurally, not numerically.** The
  local problem has a potential and no \(\dot r\) term, so nothing can dissipate; the global energy
  pathology is real but confined to the unbound sector. Any substrate model in this corpus that
  claims expansion transfers energy to or from bound systems owes a velocity-dependent term, and
  must then face the absence of orbital decay it would predict.

## Open items

- Verify the 3.8 cm/yr LLR lunar recession figure and the tidal-rhythmite angular-momentum lineage
  against source.
- Verify the Krasinsky & Brumberg 2004 and JPL/Standish AU-drift values against the primary papers
  rather than secondary summaries; record the current best upper limit rather than the historical
  reported anomalies.
- The turnaround-radius violation claims (NGC 5353/4 and the Corona Borealis supercluster) are
  cited here as existing rather than adjudicated; whether they survive is a separate question.
- The solar mass-loss rate in § What a real energy sink looks like is a calculation
  (\(L_\odot/c^{2}\approx4.3\times10^{9}\) kg/s plus an assumed \(\sim1.5\times10^{9}\) kg/s wind),
  not a sourced measurement. The wind term varies with the solar cycle and should be sourced before
  the 1.4 cm/yr figure is relied on — it is also one of the candidate explanations for the reported
  AU drift, which makes getting it right load-bearing for that row.
- \(\dot M/M\) also implies a slow secular change in \(GM_\odot\); check whether the ephemeris
  analyses cited for the AU drift already absorb it, to avoid double-counting.

## Related

- [solar-system-ephemeris-precision-floor](solar-system-ephemeris-precision-floor.md) — the
  decade-scale unmodeled-dynamics bound this note's AU row complements
- [lorentz-violation-bounds](lorentz-violation-bounds.md) — the preferred-frame wall, including the
  CMB dipole velocity that defines "peculiar" motion
- [theory/moving-source-field-consistency](../theory/moving-source-field-consistency.md) — the
  substrate branch whose \(\mathbf{w}\) is undefined until the comoving question here is answered
- [theory/retarded-scarcity-wake](../theory/retarded-scarcity-wake.md) — the parent branch
