# Branch C: the explicit boost-violating equation, and why it closes

**Purpose (ORB-11175, 2026-09-04).** The `retarded-wake-branch-c` gate owed one object: an
explicit boost-violating substrate equation with a map from its breaking parameters to
observables — or the closure of Branch C. This chapter delivers the equation, derives its
uniformly-moving-source solution against the boost-invariant control, writes the amplitude map
\(A_1=F(\ldots)\), confronts each breaking parameter with the sourced walls, and records the
outcome: **Branch C closes.** Not because the four walls named on the card crush the dissipative
parameter directly — they do not, and that is itself a result worth recording — but because the
same coefficient that makes a galactic \(m=1\) dipole makes a first-order self-acceleration of
every gravitationally bound body along its substrate-relative velocity, and the solar system's
own ephemeris floor bounds that self-acceleration far below any observable galactic amplitude.

The chapter lives in this document rather than the parent because the gate card, the
`moving-source-branch-c-not-adjudicated` claim, and the Stage 2′ program it executes all live
here. Every established-physics fact below cites a `studies/` note; arithmetic that is ours is
marked as ours; anything not yet sourced is marked `conjecture — to verify`. No orrery sim was
built: the numeric follow-on is named at the end with its gates predeclared.

## The minimal equation

Branch C's premise, inherited from the parent, is that matter and light are excitations of the
substrate and therefore blind to uniform motion through it at leading order — the reading that
lets the resonator wall ([lorentz-violation-bounds](../../studies/lorentz-violation-bounds.md),
anisotropy of \(c\) below \(10^{-17}\)) be survived at all. What the wake needs is that the
*gravitational field itself* is not blind: its dynamics must single out the substrate rest frame.
So the equation carries one preferred unit timelike vector \(U^\mu\) — the Standard-Model
Extension's way of writing a preferred frame, and the object whose weak-field gravitational
content the parametrized post-Newtonian preferred-frame parameters \(\alpha_1,\alpha_2,\alpha_3\)
classify ([moving-source-gravity-bounds](../../studies/moving-source-gravity-bounds.md)
§ preferred-frame PPN). We do not invent a new framework; we ask the narrowest question the
framework allows.

The scarcity scalar \(S\) of the parent is, in the weak field, a potential \(\Phi\) with
\(\mathbf a=-\nabla\Phi\) — that is all of the parent's mechanics this chapter uses. Take the
most general **linear, local** field equation for \(\Phi\) with at most two derivatives, built
from \(\partial_\mu\), the flat metric, and \(U^\mu\), sourced by the matter density. In the
substrate rest frame (\(U^\mu\partial_\mu=\partial_t\)) it reads

\[
\boxed{\;
\nabla^{2}\Phi-\frac{1}{c_g^{2}}\,\partial_t^{2}\Phi-\frac{\Gamma}{c_g^{2}}\,\partial_t\Phi
=4\pi G\left[\rho+\tau_s\,\partial_t\rho\right]
\;}
\tag{1}
\]

with three **named breaking parameters** and nothing else:

| Parameter | Structure | What it breaks | Time parity |
|---|---|---|---|
| \(c_g\) (speed) | \((U\!\cdot\!\partial)^2\Phi\) with a coefficient \(\ne 1/c^2\) | the gravity sector's limiting speed differs from light's; \(U\) is the frame in which \(c_g\) is isotropic | even |
| \(\Gamma\) (aether-frame dissipation), \(\ell_\Gamma\equiv c_g/\Gamma\) | \((U\!\cdot\!\partial)\Phi\) | a first-order time derivative in the substrate frame: the field relaxes toward its static solution at rate \(\Gamma\) *in that frame* | odd |
| \(\tau_s\) (source delay) | \((U\!\cdot\!\partial)\rho\) | the field responds to the substrate-frame time-extrapolated density | odd |

A mass term \(\mu^2\Phi\) is allowed by the same counting but breaks nothing (it is a Yukawa
range, already the parent family's business) and is dropped. The count is complete at this order:
with one vector there are no other scalars of dimension \(\le 2\) acting on \(\Phi\) or on
\(\rho\). Static limit: (1) reduces to \(\nabla^2\Phi=4\pi G\rho\) for every value of the three
parameters, so **no static test sees them**. That is why this is the minimal Branch C: it is
invisible to everything the parent family has already lost on, and it can only show itself
through motion relative to \(U\).

The parent's open questions — is \(S\) a scalar, a flow history, or an effective metric; what is
its evolution equation and its conserved quantities; what defines \(U\) — are answered *for this
class* by (1): \(S\) is a scalar potential, (1) is its evolution equation, \(\Gamma\) and
\(\tau_s\) are its only conserved-quantity-breaking terms (energy and momentum leak to the
substrate at rate \(\propto\Gamma\), § the drag lemma), and \(U\) is whatever frame (1) holds in
— the chapter never assumes it is the CMB frame; it only needs the ratio of the Sun's and a
galaxy's speed relative to it to be of order one, which fails only if \(U\) is tuned to comove
with the Sun.

## The control: Heaviside form and the Carlip cancellation inside the model

Set \(\Gamma=\tau_s=0\). A point source \(\rho=M\delta^3(\mathbf x-\mathbf w t)\) moving
uniformly at \(\mathbf w\) relative to the substrate, \(\beta_g=|\mathbf w|/c_g\). In comoving
coordinates \(\boldsymbol\xi=\mathbf x-\mathbf w t\) the steady state has
\(\partial_t\to-\mathbf w\!\cdot\!\nabla\), so with \(\partial_\parallel=\hat{\mathbf w}\cdot\nabla\):

\[
(1-\beta_g^{2})\,\partial_\parallel^{2}\Phi+\nabla_\perp^{2}\Phi=4\pi GM\,\delta^{3}(\boldsymbol\xi)
\quad\Longrightarrow\quad
\Phi_0=-\frac{\gamma_g\,GM}{\sqrt{\gamma_g^{2}\xi_\parallel^{2}+\xi_\perp^{2}}},
\qquad \gamma_g=(1-\beta_g^{2})^{-1/2}.
\tag{2}
\]

This is the Heaviside field of a uniformly moving charge with \(c\to c_g\)
([moving-source-gravity-bounds](../../studies/moving-source-gravity-bounds.md) § aberration
cancellation: the Liénard–Wiechert velocity term extrapolates the retarded direction so the field
points at the instantaneous position). Equation (2) is **even in \(\xi_\parallel\)**: every odd
multipole vanishes identically, at every order in \(\beta_g\), for every \(c_g\). The first
deformation is the fore–aft-symmetric \(O(\beta_g^2)\) flattening. So the Carlip cancellation is
not an assumption imported from electromagnetism; it is a theorem of (1) with the odd sector off,
and it is exactly the Stage 1′ calibration equation this document demanded: no \(O(\beta_g)\)
dipole, a symmetric \(O(\beta_g^2)\) deformation, and a solver that shows a first-order dipole
here is defective. (Symbolic residual of (2) in the comoving operator: zero — ours, uncataloged.)

Corollary for the parent's Branch B: a "causal steady field" with any propagation speed is (2).
Retardation alone never makes a wake. The speed parameter \(c_g\) is a breaking parameter with no
dipole attached.

## The first-order moving-source solution with the odd sector on

**Dissipation.** Keep \(\Gamma\), drop \(\tau_s\) and the \(O(\beta_g^2)\) term (it only
reinstates the symmetric Heaviside flattening). The comoving equation becomes

\[
\nabla^{2}\Phi+k\,\partial_\parallel\Phi=4\pi GM\,\delta^{3}(\boldsymbol\xi),
\qquad
k\equiv\frac{\Gamma\beta_g}{c_g}=\frac{\beta_g}{\ell_\Gamma},
\tag{3}
\]

which the substitution \(\Phi=e^{-k\xi_\parallel/2}\psi\) turns into a screened Poisson
equation \(\nabla^2\psi-(k/2)^2\psi=4\pi GM\delta^3\). Hence, with \(\theta\) measured from the
leading direction \(+\hat{\mathbf w}\),

\[
\boxed{\;
\Phi_\Gamma(r,\theta)=-\frac{GM}{r}\exp\!\left[-\frac{k}{2}\,(r+\xi_\parallel)\right]
=-\frac{GM}{r}\exp\!\left[-A_1(r)\,(1+\cos\theta)\right],
\qquad
A_1(r)=\frac{k r}{2}=\frac{\beta_g\,r}{2\,\ell_\Gamma}
\;}
\tag{4}
\]

— the same closed form as a moving heat source in a conducting medium, which is what a moving
source in a relaxing medium is. Read off what the parent wanted and what it did not expect:

- **The \(m=1\) potential dipole exists and is first order.** Expanding (4),
  \(\Phi_\Gamma=-\frac{GM}{r}\left[1-A_1-A_1\cos\theta\right]+O(A_1^2)\): dipole-to-monopole ratio
  \(A_1(r)\), leading edge at higher (less negative) potential, trailing edge exactly Newtonian —
  the parent's sign. The potential contrast is \(\Phi_{\rm lead}-\Phi_{\rm trail}=2A_1\,GM/r\),
  the parent's formula with \(\beta_g\to A_1\).
- **The amplitude is not \(\beta_g\); it is \(\beta_g\) times \(r/2\ell_\Gamma\).** The wake is a
  free parameter bounded by experiment, exactly as § Stage 2′ predicted, and it grows linearly
  with radius: unlike the refuted delayed-center shortcut this is a legitimate exterior profile,
  because the operator in (3) is not Laplace's — the "effective source" \(-k\partial_\parallel\Phi_0\)
  is the dissipation term itself, filling space by construction, and the linearly divergent
  dipole moment of § The delayed-center potential is not a Poisson-vacuum field never arises
  because the exponential closes the profile at \(r\sim\ell_\Gamma/\beta_g\).
- **No first-order leading/trailing acceleration contrast.** From (4) the inward radial
  acceleration is \(g=\frac{GM}{r^2}e^{-x}(1+x)\) with \(x=A_1(1+\cos\theta)\), so
  \(g=g_0\,[1-\tfrac12A_1^2(1+\cos\theta)^2+\ldots]\): the parent's "stronger attraction on the
  trailing edge" is second order. The first-order force is purely **tangential**,
  \(a_\theta=g_0A_1\sin\theta\), pushing from the leading toward the trailing side and vanishing
  on the axis. (Both expansions symbolically checked — ours, uncataloged.)
- **Extended sources.** At first order \(\nabla^2\Phi_1=-k\,\partial_\parallel\Phi_0\) everywhere;
  outside a source of size \(a\) the far field of \(\Phi_1\) is set by the far field of
  \(\Phi_0\), i.e. by \(M\) alone, so \(A_1(r)\to\beta_g r/2\ell_\Gamma\) with corrections
  \(O(a/r)\) **independent of central concentration**. The parent's concentration law
  \(C[\rho;R]\) is not merely moot for this class — it is absent.

**Source delay.** Keep \(\tau_s\), drop \(\Gamma\). The right-hand side of the comoving equation
is \(4\pi G[\rho-\tau_s w\,\partial_\parallel\rho]\), so
\(\Phi_{\tau}=\Phi_0-\tau_s w\,\partial_\parallel\Phi_0=\Phi_0(\boldsymbol\xi-\tau_s\mathbf w)+O(\tau_s^2)\):
the *entire* potential of any source is rigidly displaced by \(\tau_s\mathbf w\) (ahead for
\(\tau_s>0\), behind for \(\tau_s<0\)). This is the delayed-center picture done legitimately — a
fixed displacement, not one growing with the evaluation radius — and its dipole ratio is a
physical offset's, \(A_1(r)=|\tau_s|\,w/r\to0\), as this document's first section already said a
real offset must be.

**The amplitude map.** For the minimal class,

\[
\boxed{\;
A_1(r)=\underbrace{\frac{\beta_g\,r}{2\ell_\Gamma}}_{\Gamma}
+\underbrace{\frac{|\tau_s|\,\beta_g\,c_g}{r}}_{\tau_s}
+\underbrace{0}_{c_g}\;+\;O(\beta_g^2)
\;}
\tag{5}
\]

with the \(\Gamma\) term concentration-independent, the \(\tau_s\) term a rigid shift, and the
tracer coupling entering only through the potential (the equation has no velocity-dependent
force; § The gravitomagnetic gap is a debt of the completion, not of the breaking terms).

## The drag lemma: the dipole and the drag are one coefficient

A time-odd term is a dissipation. Its first consequence is not the dipole but the force the
dipole exerts back on its own source. At first order in \(k\), for any source density
\(\rho\) with Newtonian potential \(\Phi_0\), the self-force along \(\hat{\mathbf w}\) is
\(F_\parallel=-\int\rho\,\partial_\parallel\Phi_1\), and with \(\rho=\nabla^2\Phi_0/4\pi G\) and
\(\nabla^2\Phi_1=-k\,\partial_\parallel\Phi_0\), two integrations by parts give

\[
F_\parallel=-\frac{k}{4\pi G}\int(\partial_\parallel\Phi_0)^2\,d^3x
=-\frac{2k}{3}\,|W|,
\qquad
|W|=\frac{1}{8\pi G}\int|\nabla\Phi_0|^2\,d^3x,
\tag{6}
\]

for a spherical source, \(|W|\) being its gravitational binding energy. (Verified on a periodic
grid for a uniform sphere: the integration-by-parts identity holds to \(10^{-12}\); the
normalisation matches \(2|W|/3\) up to the box's truncated exterior field — ours, uncataloged.)
The sign is drag: the well is shallower ahead and full behind, so the body is pulled back. With
\(k=\Gamma w/c_g^2\) and \(c_g=c\) (§ walls, Cherenkov row):

\[
\boxed{\;
\mathbf a_{\rm self}=-\frac{2\Gamma}{3}\,\frac{|W|}{Mc^{2}}\;\mathbf w
=-\frac{2c}{3\ell_\Gamma}\,\frac{|W|}{Mc^{2}}\;\mathbf w
\;}
\tag{7}
\]

Every gravitationally bound body decelerates relative to the substrate frame at a rate set by
\(\Gamma\) times its binding-energy fraction — the same structure as the self-gravity-dependent
preferred-frame effects the PPN \(\alpha\)-parameters describe, except first order in
\(\mathbf w\) and independent of spin. The energy-balance reading agrees: the dissipated power of
the uniformly moving Newtonian field, \(\frac{\Gamma}{4\pi Gc^2}\int(\partial_t\Phi_0)^2d^3x\)
with \(\partial_t\Phi_0=-\mathbf w\cdot\nabla\Phi_0\), equals \(F_\parallel w\). The parent's
rejection gate 3 (conservation) is therefore not violated by this class — the momentum has an
explicit sink — but the sink is the falsifier. The τ\(_s\) term, being a rigid shift of a
conservative field, produces no self-force.

Eliminating \(\Gamma\) between (5) and (7) gives the relation that closes the branch. A galaxy
with substrate speed \(\beta_{\rm gal}\) showing a dipole \(A_1\) at radius \(R\) has
\(c/\ell_\Gamma=2cA_1/\beta_{\rm gal}R\), so every other bound body, moving at \(\beta_{\rm b}\),
must self-accelerate at

\[
\boxed{\;
a_{\rm self}=\frac{4A_1}{3R}\,\frac{|W|}{M}\,\frac{\beta_{\rm b}}{\beta_{\rm gal}}
\;}
\tag{8}
\]

— independent of \(\Gamma\) and of \(c\), and depending on \(U\) only through the ratio
\(\beta_{\rm b}/\beta_{\rm gal}\).

## Walls

Sourced velocity scales: the solar system moves at \(369.82\pm0.11\) km/s relative to the CMB,
\(\beta_\odot=1.23\times10^{-3}\) ([lorentz-violation-bounds](../../studies/lorentz-violation-bounds.md)
§ velocity scales); the Sun's Galactic circular speed is \(229\) km/s
([milky-way-rotation-curve](../../studies/milky-way-rotation-curve.md)), so \(\beta_\odot\) is
\(\sim10^{-3}\) for any \(U\) not comoving with the Sun. For the galaxy, this document's generous
\(600\) km/s gives \(\beta_{\rm gal}=2\times10^{-3}\). The Sun's binding fraction is bounded
below by the uniform-sphere value, \(|W_\odot|/M_\odot c^2\ge\frac35\,GM_\odot/R_\odot c^2=1.27\times10^{-6}\)
(ours, from standard constants; uniform density minimises \(|W|\) at fixed \(M\) and \(R\); the
real Sun's central concentration raises it by roughly \(3\times\) — `conjecture — to verify`).
The same equation must govern the Sun's field as governs a galaxy's:
[source-side-universality-of-g](../../studies/source-side-universality-of-g.md).

**The solar-system self-acceleration wall.** By (7)–(8) the Sun self-accelerates along
\(-\hat{\mathbf w}_\odot\), a direction fixed in inertial space, at
\(a_\odot\ge\frac23\,\Gamma\,(1.27\times10^{-6})(3.7\times10^{5}\ {\rm m/s})=0.31\,\Gamma\)
m s\(^{-2}\) per s\(^{-1}\). In the heliocentric frame every planet therefore feels a uniform
anomalous acceleration of that size — the Earth's own self-acceleration is \(10^{-4}\) of the
Sun's. The corpus's sourced bound on unmodeled solar-system dynamics is the Newtonian-omission
residual floor ([solar-system-ephemeris-precision-floor](../../studies/solar-system-ephemeris-precision-floor.md)):
a modification predicting a larger deviation from the Newtonian baseline over 2016–2025 than a
planet's floor is excluded at that amplitude. Converting a uniform acceleration \(\delta\) into a
10-year position deviation with the calibrated estimator (rms \(|\Delta r|\approx2.2\,\delta t/n\)
for spans of at least an orbit, \(\approx0.23\,\delta t^2\) for a third of one — ours, from a
Kepler integration, uncataloged):

| Planet | floor, rms \(|\Delta r|\) | mean motion \(n\) | bound on uniform \(\delta\) |
|---|---|---|---|
| Earth | \(2.49\times10^{-6}\) AU | \(2.0\times10^{-7}\) s\(^{-1}\) | \(1\times10^{-10}\) m/s² |
| Mars | \(8.40\times10^{-7}\) AU | \(1.06\times10^{-7}\) s\(^{-1}\) | \(2\times10^{-11}\) m/s² |
| Jupiter | \(1.84\times10^{-7}\) AU | \(1.68\times10^{-8}\) s\(^{-1}\) | \(6\times10^{-13}\) m/s² |
| Saturn | \(4.25\times10^{-8}\) AU | \(6.8\times10^{-9}\) s\(^{-1}\) | \(3\times10^{-13}\) m/s² |
| Uranus | \(4.08\times10^{-9}\) AU | \(2.4\times10^{-9}\) s\(^{-1}\) | \(3\times10^{-14}\) m/s² |

The floors note flags the outer rows as upper bounds on allowed unmodeled dynamics, which is
exactly the use made of them. Take Saturn as the conservative row and Uranus as the tight one:

\[
\Gamma<1\times10^{-12}\ {\rm s^{-1}},\quad \ell_\Gamma>3\times10^{20}\ {\rm m}\approx10\ {\rm kpc}
\quad\text{(Saturn)};\qquad
\Gamma<1\times10^{-13}\ {\rm s^{-1}},\quad \ell_\Gamma>3\times10^{21}\ {\rm m}\approx100\ {\rm kpc}
\quad\text{(Uranus)}.
\]

**The parameter-by-parameter table.** "Survives" means the wall does not bound the parameter;
it never means the parameter is free to produce a galactic dipole — that verdict is the last row.

| Breaking parameter | Cherenkov ([moving-source-gravity-bounds](../../studies/moving-source-gravity-bounds.md)) | Resonator / clock anisotropy ([lorentz-violation-bounds](../../studies/lorentz-violation-bounds.md)) | Cassini \(\gamma\) ([scalar-gravity-ppn-constraints](../../studies/scalar-gravity-ppn-constraints.md)) | \(\alpha_1/\alpha_2\) ([moving-source-gravity-bounds](../../studies/moving-source-gravity-bounds.md)) | Solar-system self-acceleration ([ephemeris floor](../../studies/solar-system-ephemeris-precision-floor.md)) |
|---|---|---|---|---|---|
| \(c_g\) (speed) | **Bounds it**: \(\Phi\) is the conventionally coupled potential, so Moore & Nelson apply, \(c-c_g<2\times10^{-15}c\) (Galactic origin). Extension of their graviton scaling to a scalar mode: `conjecture — to verify`. \(c_g>c\) unbounded here. | Survives: \(U\) is invisible to the photon sector by the Branch C premise. | Survives: statics untouched. | Survives: the \(O(\beta_g^2)\) Heaviside flattening is not a PPN preferred-frame term. | Survives: (2) has no odd sector, no drag. **Produces no dipole at any value.** |
| \(\Gamma\) (dissipation) | Survives: \(\Gamma\) does not change the mode speed. | Survives: \(\Gamma\) lives in the gravity sector only; the wall binds the *completion* — light and lab matter must stay \(U\)-blind at \(10^{-17}\) while \(\Phi\) sees \(U\) at \(\Gamma\). | Survives: the moving-Sun dipole along the Cassini ray is \(A_1(\le1\,{\rm AU})=\beta_\odot r/2\ell_\Gamma<3\times10^{-13}\) for \(\ell_\Gamma>10\) kpc, against a \(2\times10^{-5}\) sensitivity; the photon coupling of \(\Phi\) itself is the parent's refuted sector, not a Branch C parameter. | **Not applicable by parametrization**: the dipole (4) is first order in \(w\) in \(g_{00}\) with a new scale \(\ell_\Gamma\) — a half-order term outside the PPN potentials, the same hazard [ppn-reduction-of-the-settled-flow](../ppn-reduction-of-the-settled-flow/) found. The \(\alpha\)'s classify the \(O(w^2)\) and \(g_{0i}\) sectors, which (1) does not have (order counting from PPN bookkeeping: `conjecture — to verify` against Will's metric). | **Excluded**: \(\ell_\Gamma>10\)–\(100\) kpc, hence at \(R=10\) kpc, \(\beta_{\rm gal}=2\times10^{-3}\): \(A_1\le1\times10^{-3}\) (Saturn, uniform-sphere Sun) down to \(\sim3\times10^{-5}\) (Uranus, real Sun). |
| \(\tau_s\) (source delay) | Survives. | Survives (gravity sector). | Survives at any \(\tau_s\) the next column allows. | Not applicable: a rigid shift of a static potential is not a PPN term. | **Excluded**: the Sun's dynamical centre coincides with its disk to far better than \(R_\odot\) (the km-level statement: `conjecture — to verify`; the \(R_\odot\)-level one is not in doubt), so \(|\tau_s|\,w_\odot<7\times10^{8}\) m, \(|\tau_s|<2\times10^{3}\) s, and \(A_1(10\,{\rm kpc})=|\tau_s|w_{\rm gal}/R<4\times10^{-12}\). |
| any *metric* aether-type completion (scalar + vector \(U\) dynamics) | as \(c_g\) | as \(\Gamma\) | must give \(\gamma=1\) to \(2\times10^{-5}\) | **Bounds it**: its preferred-frame content is \(\alpha_1\le10^{-4}\), \(\alpha_2\le10^{-7}\) (sourced), entering at \(O(w^2)\) or through \(g_{0i}\) on moving tracers, so \(A_1\lesssim\alpha_1\beta^2\le10^{-10}\). | — |

Comparison scales (this document, § The delayed-center toy supplies a scale, not a ceiling):
observed disk lopsidedness \(\sim0.1\); the delayed-center toy \(2\times10^{-3}\). The maximal
surviving Branch C dipole is **\(10^{2}\)–\(3\times10^{3}\) times below the observed scale on
every reading of the wall**, and at or below the toy scale that this document's own
detectability table already put at \(10^{4}\)–\(10^{5}\) galaxies for \(3\sigma\); at the Uranus
reading the requirement scales to \(\sim10^{7}\).

Two further channels sharpen the same coefficient and are recorded as debts, not used:

- **Pulsar self-acceleration** — `conjecture — to verify`. A neutron star's binding fraction
  is of order \(10^{-1}\) (not in `studies/`), \(10^{5}\) times the Sun's, so (7) makes its
  self-acceleration \(\sim0.1\,\Gamma w\); a line-of-sight component enters the observed period
  derivative through the Doppler term, which is the channel behind the sourced \(\alpha_3\) bound
  of \(4\times10^{-20}\) ([moving-source-gravity-bounds](../../studies/moving-source-gravity-bounds.md)).
  If that channel bounds anomalous accelerations near \(10^{-10}\) m/s², \(\Gamma\) falls by a
  further four orders and \(A_1\) with it.
- **Dissipation of orbital fields** — `conjecture — to verify`. The same \(\Gamma\) damps the
  time-varying near-zone field of a binary at \(\dot E/E\sim\Gamma\,v^2/c^2\), which for a
  relativistic binary pulsar is of the same order as the general-relativistic decay rate at
  \(\Gamma\sim10^{-10}\) s\(^{-1}\); the measured agreement with general relativity would bound
  \(\Gamma\) independently once the decay data are sourced.

## The falsifier, stated once

- **Dimensionless amplitude:** \(A_1(R)=\beta_{\rm gal}R/2\ell_\Gamma\), the \(m=1\) potential
  dipole along the substrate velocity, growing linearly with radius, concentration-independent.
- **Observable:** in a galaxy, the dipole and its first-order tangential force
  \(g_0A_1\sin\theta\) (no first-order rotation-speed contrast on the leading/trailing axis); in
  the solar system, the twin the dipole cannot be separated from — a uniform anomalous
  acceleration of the planets of \(a_\odot=\frac{4A_1}{3R}\frac{|W_\odot|}{M_\odot}\frac{\beta_\odot}{\beta_{\rm gal}}\),
  fixed in the direction opposite the Sun's substrate-relative velocity.
- **Bound:** the house ephemeris floors, \(3\times10^{-13}\) m/s² (Saturn) to
  \(3\times10^{-14}\) m/s² (Uranus), which cap \(A_1(10\,{\rm kpc})\) at \(10^{-3}\) to
  \(3\times10^{-5}\).

## Closure

Branch C, as the parent defined it — matter as excitations of a medium whose rest frame the
gravitational field can nonetheless see — has, at linear, local, two-derivative order, exactly
three breaking parameters. One (\(c_g\)) produces no dipole and is pinned by Cherenkov. One
(\(\tau_s\)) produces a rigid offset the solar system excludes by ten orders. One (\(\Gamma\))
produces the parent's dipole with the parent's sign and a legitimate exterior profile — and
carries, inseparably, a first-order self-acceleration of every bound body that the solar
system's ephemeris floor bounds far below any galactic amplitude that could be seen. The four
walls the card named do not do the killing; the equation's own conservation structure does. No
parameter value producing an observable galactic \(m=1\) dipole survives. The gate's kill —
"the equation is already bounded once couplings are specified" — fired on the self-acceleration
wall.

What this closure does **not** cover, and what would reopen it (with `daniel_reopen`, since the
central claim goes on the wall): a **non-local** or **scale-dependent** \(\Gamma\) that couples to
kiloparsec structures but not to stars (which surrenders locality, the premise of the card); a
**non-linear** sector in which the odd term switches on only above some field scale (which must
then explain why the Sun's field, deeper than a galaxy's outskirts by orders of magnitude, is
exempt); or a \(U\) tuned to comove with the Sun. None of these is the retarded-scarcity wake as
proposed. The forbidden reopens on the card (`retarded-wake-rescues-parent`,
`scarcity-fixed-beta-universality`) are untouched.

## Follow-on fixture (named, not built)

`branch-c-first-order-solution` — an orrery fixture, to be filed as an orbit task in that
workspace if the algebra above is ever to move from `untested` to `supported`:

1. A comoving-frame solver for \((1-\beta_g^2)\partial_\parallel^2\Phi+\nabla_\perp^2\Phi+k\,\partial_\parallel\Phi=4\pi G\rho\)
   on a point source, a uniform sphere, and a Plummer sphere of equal mass.
2. **Predeclared gates.** (i) Control, \(k=0\): all odd ring multipoles zero to solver precision at
   \(\beta_g\in\{10^{-3},10^{-2},10^{-1}\}\) — the Carlip calibration. (ii) \(k\ne0\), point source:
   \(A_1(r)/(kr/2)\to1\), radial leading/trailing contrast \(\propto k^2\), tangential force
   \(\to g_0A_1\sin\theta\). (iii) Extended sources: exterior \(A_1(r)\) agrees between the
   uniform and Plummer spheres to \(O(a/r)\) — concentration independence. (iv) Self-force on the
   uniform sphere \(=-\frac{2k}{3}\cdot\frac35\frac{GM^2}{a}\) within grid error; on the Plummer
   sphere, \(-\frac{2k}{3}|W_{\rm Plummer}|\).
3. **Kill.** Any gate failing by more than the resolution ladder's convergence band refutes the
   corresponding row here; a first-order dipole in gate (i) is a solver defect, by construction.

It is a demonstration fixture, not a physics arm: nothing in the closure waits on it.
