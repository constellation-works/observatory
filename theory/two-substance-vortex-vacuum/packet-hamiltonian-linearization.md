## Packet Hamiltonian linearization — mode count, equal speeds, and why this is not Maxwell

**Purpose (ORB-11219, 2026-09-05).** The live gate
`two-substance-photon-sector` owes one Maxwell sector. A standing conjecture
was that the existing Orrery packet apparatus
([two-substance-dynamical-packet](../../../orrery/lab/sims/two-substance-dynamical-packet/))
could become that sector by setting its two declared speeds equal. This
chapter freezes that apparatus’s continuum equations, counts modes against
constraints, and computes the linearized principal symbol — including the
coupling-off control, equal-speed degeneracy, and small admissible
backgrounds. **Analytical failure of this scalar-density apparatus is the
result.** It is not a no-go for every two-component emergent-gauge theory, and
it does not reopen the gravity wall.

Established-physics facts cite
[studies/maxwell-mode-content-and-two-fluid-acoustics](../../studies/maxwell-mode-content-and-two-fluid-acoustics.md).
Algebra that is ours is marked as ours. Model-property rows stay `untested`
until the named orrery fixture is cataloged (policy: analytic rows wait on a
sim or a sourced study; the study backs the Maxwell/two-fluid comparator, not
this Hamiltonian). No new interaction is introduced.

## Frozen equations (the actual apparatus)

The packet fixture evolves two conserved densities \(n_1,n_2\) and their
fluxes \(\mathbf{j}_1,\mathbf{j}_2\) under

\[
H=\frac{|\mathbf{j}_1|^2+|\mathbf{j}_2|^2}{2}
+\frac{c_+^2 n_+^2}{4}+\frac{c_-^2 n_-^2}{4}
+\frac{\lambda}{4}\,n_+ n_-^2,
\tag{1}
\]

with \(n_+=n_1+n_2-2n_0\), \(n_-=n_1-n_2\), and \(n_0=1\) the declared
background density. The continuum limit of the kick–drift–kick step is

\[
\partial_t n_i+\nabla\cdot\mathbf{j}_i=0,
\qquad
\partial_t\mathbf{j}_i+\nabla\mu_i=0,
\qquad i=1,2,
\tag{2}
\]

where \(\mu_i=\delta H/\delta n_i\):

\[
\begin{aligned}
\mu_1&=\tfrac12 c_+^2 n_++\tfrac12 c_-^2 n_-+\tfrac14\lambda n_-^2+\tfrac12\lambda n_+ n_-,\\
\mu_2&=\tfrac12 c_+^2 n_+-\tfrac12 c_-^2 n_-+\tfrac14\lambda n_-^2-\tfrac12\lambda n_+ n_-.
\end{aligned}
\tag{3}
\]

These are the chemical potentials in `main.py`. The kinetic term is
\(|\mathbf{j}|^2/2\), not \(|\mathbf{j}|^2/(2n)\); there is no convective
derivative. Neither omission is repaired here. The cubic \(\lambda\) term is
the named postulate `postulate-lambda-coupling`.

**Finite assumptions.** Continuum (lattice dispersion is a fixture
correction, not a new mode); uniform rest background, or a small uniform
shift of \((n_+,n_-)\); \(c_\pm>0\) real; no capacity constraint in (1)
(the packet Hamiltonian does not implement \(\varnothing\ge0\)); linearization
except for the curl identity below, which is exact.

## Variable count, constraints, and the exact curl identity

In \(d\) spatial dimensions the state is \((n_1,n_2,\mathbf{j}_1,\mathbf{j}_2)\):
**\(2+2d\)** real fields, and (2) supplies **\(2+2d\)** first-order evolution
equations. There is no algebraic constraint. In particular there is no Gauss
law: nothing forces \(\mathbf{k}\cdot\delta\mathbf{j}=0\) or kills a
longitudinal density.

Because each \(\mu_i\) is a local scalar, (2) implies the exact identity

\[
\partial_t(\nabla\times\mathbf{j}_i)=-\nabla\times\nabla\mu_i=0.
\tag{4}
\]

Transverse flux is frozen at finite amplitude, not restored. This is the
gradient-driven Helmholtz fact
([studies/maxwell-mode-content-and-two-fluid-acoustics](../../studies/maxwell-mode-content-and-two-fluid-acoustics.md)
§ Gradient-driven flux), applied to (2). Faraday’s curl is absent.

## Principal symbol on the vacuum background

Linearize (2)–(3) about \(n_1=n_2=n_0\), \(\mathbf{j}_i=0\)
(\(n_+=n_-=0\)). The cubic terms in (3) are quadratic in the perturbation and
drop from the linear symbol, **whether or not \(\lambda=0\)**. Common and
relative combinations \(\delta n_\pm=\delta n_1\pm\delta n_2\),
\(\delta\mathbf{j}_\pm=\delta\mathbf{j}_1\pm\delta\mathbf{j}_2\) decouple:

\[
\partial_t\delta n_\pm+\nabla\cdot\delta\mathbf{j}_\pm=0,
\qquad
\partial_t\delta\mathbf{j}_\pm+c_\pm^2\nabla\delta n_\pm=0.
\tag{5}
\]

Plane waves \(\propto\exp[i(\mathbf{k}\cdot\mathbf{x}-\omega t)]\),
\(\mathbf{k}\ne0\):

| Branch | Dispersion | Eigenvector | Count |
|---|---|---|---|
| Common longitudinal | \(\omega=\pm c_+|\mathbf{k}|\) | \(\delta n_+\ne0\), \(\delta n_-=0\), \(\delta\mathbf{j}_+\parallel\mathbf{k}\), \(\delta\mathbf{j}_-=0\) | 2 |
| Relative longitudinal | \(\omega=\pm c_-|\mathbf{k}|\) | \(\delta n_-\ne0\), \(\delta n_+=0\), \(\delta\mathbf{j}_-\parallel\mathbf{k}\), \(\delta\mathbf{j}_+=0\) | 2 |
| Transverse currents | \(\omega=0\) | \(\delta n_\pm=0\), \(\mathbf{k}\cdot\delta\mathbf{j}_\pm=0\) | \(2(d-1)\) |

Total \(4+2(d-1)=2+2d\), matching the field count. **Nothing is left over for
a photon.** The four propagating roots are scalar density waves with flux
parallel to \(\mathbf{k}\). The \(2(d-1)\) transverse directions are
zero-frequency currents, not polarizations.

Maxwell vacuum, by contrast (same studies note § Maxwell vacuum waves): six
fields \((\mathbf{E},\mathbf{B})\), two Gauss constraints
\(\mathbf{k}\cdot\mathbf{E}=\mathbf{k}\cdot\mathbf{B}=0\), two propagating
*transverse* polarizations at \(\omega=\pm c|\mathbf{k}|\). Equating two
eigenvalues of (5) with those two polarizations is a type error: multiplicity
is not polarization.

In the packet fixture’s native \(d=2\): six fields, four longitudinal
propagating roots, two frozen transverse currents. In \(d=3\): eight fields,
four longitudinal roots, four frozen transverse currents. Neither is Maxwell.

## Unequal speeds, equal speeds, and the \(\lambda=0\) control

**Unequal speeds** (\(c_+=0.65\), \(c_-=1.0\), the packet fixture’s
`COMMON_SPEED` and `RELATIVE_SPEED`). Two distinct longitudinal cones. This is
already a standing witness against one cone; it is also the generic two-fluid
default (Landau/Peshkov).

**Equal speeds** (\(c_+=c_-=c\)). The two longitudinal cones coincide:
\(\omega=\pm c|\mathbf{k}|\) with a two-dimensional *longitudinal* eigenspace
spanned by \((\delta n_+,0)\) and \((0,\delta n_-)\). Both eigenvectors still
have \(\delta\mathbf{j}\parallel\mathbf{k}\). Transverse currents remain
\(\omega=0\). Cone degeneracy is two scalar sounds sharing a speed, not two
photon polarizations.

**Coupling-off, vacuum background.** \(\lambda\) is absent from (5). The
linear spectrum at \(\lambda=0\) and at the fixture’s \(\lambda=0.8\) *agree
exactly* about \(n_\pm=0\). The cubic term cannot manufacture a transverse
restoring force that the linear force law does not contain.

## Small admissible backgrounds (local only)

On a uniform rest background \((\bar n_+,\bar n_-)\) the linearized chemical
potentials mix. The acoustic tensor on \((\delta n_+,\delta n_-)\) is the
Hessian of the potential in (1) (ours):

\[
M=\begin{pmatrix}c_+^2 & \lambda\bar n_-\\ \lambda\bar n_- & c_-^2+\lambda\bar n_+\end{pmatrix}.
\tag{6}
\]

Squared speeds are the eigenvalues of \(M\). For \(\bar n_-=0\) the matrix
stays diagonal: speeds \(c_+\) and \(\sqrt{c_-^2+\lambda\bar n_+}\). For
small \(\bar n_-\ne0\) the two scalar branches mix but remain scalar; the
force is still \(-\nabla\mu\), so (4) still freezes transverse current.
Positive-definiteness of \(M\) (local acoustic stability) holds for
\(|\bar n|\ll c^2/|\lambda|\).

Those conclusions are **local**. Completing the square in \(n_+\) (ours):

\[
\frac{c_+^2}{4}n_+^2+\frac{\lambda}{4}n_+ n_-^2
=\frac{c_+^2}{4}\left(n_++\frac{\lambda}{2c_+^2}n_-^2\right)^2
-\frac{\lambda^2}{16c_+^2}n_-^4.
\tag{7}
\]

The remainder \(-\lambda^2 n_-^4/(16 c_+^2)\) is a negative quartic for every
\(\lambda\ne0\). Global Hamiltonian unboundedness is uncured; the packet
fixture already recorded this and sampled only a locally positive weak-field
patch. A locally stable Hessian is not a globally bounded energy.

## What fails, and what this does not kill

**Fails:** the conjecture that tuning \(c_+=c_-\) in (1)–(2) yields a Maxwell
sector. The apparatus is two conserved scalar densities with gradient-driven
fluxes. Its linear content is two longitudinal sounds plus frozen transverse
currents. Equal speeds degenerate the sounds; they do not invent Faraday, Gauss
constraints, or transverse restoring force.

**Does not fail:** every possible two-component emergent-gauge theory. Volovik’s
Fermi-point theorem delivers one cone and an emergent \(A_\mu\) from the
collective coordinates of a topologically protected vacuum, not from two scalar
densities
([studies/superfluid-vacuum-and-emergent-gauge-fields](../../studies/superfluid-vacuum-and-emergent-gauge-fields.md)).
A recast to one substance with a two-component order parameter remains the
gate’s other owed object. A different interaction whose force is not a pure
gradient is a new postulate, out of scope here.

**Does not reopen:** `two-substance-void-volume-ep`,
`two-substance-conserving-far-field`,
`two-substance-s2-fifth-force-charge`,
`two-substance-fixed-length-universality`. No gravity-source law is proposed.
No nature-level photon sector is claimed. Kill condition B stays the theorem
the family owes.

## Cataloged verification fixture (ORB-11220)

`two-substance-packet-linear-symbol` — Orrery ORB-11220, merged remote commit
`73c9bd53e963e44bb365992c1df87a1077cc996f` — verified (5)–(6) on the existing
packet discretization (periodic 2-D, centered derivatives), not a new
interaction and not an observational fit. Dimensionless. Result-neutral: a
failed gate is reported as a classification, never as a nonzero process exit.

**Operator.** Discrete linearized evolution of
\((n_1,n_2,j_{1x},j_{1y},j_{2x},j_{2y})\) about a declared uniform background,
read in Fourier space at wavevectors
\(\mathbf{k}=(2\pi n_x/L, 2\pi n_y/L)\) with \(n_x\in\{1,2,4\}\), \(n_y=0\)
and one diagonal probe \((n_x,n_y)=(2,2)\). Longitudinal projector
\(\hat{\mathbf{k}}\otimes\hat{\mathbf{k}}\); transverse projector
\(I-\hat{\mathbf{k}}\otimes\hat{\mathbf{k}}\).

**Predeclared cases.**

| Id | Background | \(\lambda\) | \((c_+,c_-)\) | Seed |
|---|---|---|---|---|
| U0 | vacuum \(\bar n_\pm=0\) | 0 | \((0.65,1.0)\) | longitudinal common / relative |
| U1 | vacuum | 0 | \((1.0,1.0)\) | same |
| U2 | vacuum | 0.8 | \((0.65,1.0)\) and \((1.0,1.0)\) | same (must match U0/U1) |
| B0 | \(\bar n_+=0\), \(\bar n_-=0.05\) | 0.8 | \((0.65,1.0)\) and \((1.0,1.0)\) | longitudinal mixed |
| T0 | vacuum | 0 and 0.8 | both speed pairs | transverse \(j_y\) only |

**Predeclared gates** (result-neutral tolerances; discrete Laplacian
dispersion is expected).

1. Longitudinal frequencies: \(|\omega/(c_{\mathrm{branch}}|\mathbf{k}|)-1|\le 0.02\)
   on U0/U1, using the analytic branch speed; at equal speed, both longitudinal
   eigenvalues share that cone to \(0.02\).
2. Eigenvector type: longitudinal seeds have
   \(|\widehat{\delta\mathbf{j}}\cdot\hat{\mathbf{k}}|\ge 0.98\); they are not
   classified as polarizations.
3. Transverse T0: \(|\omega|/(c_{\max}|\mathbf{k}|)\le 0.02\) (numerical floor)
   and discrete curl of each \(\mathbf{j}_i\) conserved to \(10^{-10}\) relative
   to the seed.
4. Vacuum coupling-off: U2 vs U0/U1 eigenvalue relative difference
   \(\le 10^{-8}\).
5. Small-background mixing: B0 Hessian eigenvalues of (6) match measured
   \(\omega^2/|\mathbf{k}|^2\) within \(0.02\); both branches remain
   longitudinal by gate 2.
6. Classification vocabulary is frozen before the run:
   `longitudinal-acoustic`, `transverse-frozen`,
   `unexpected-propagating-transverse`. The Maxwell-kill of this sub-object is
   any T0 or equal-speed arm classified `unexpected-propagating-transverse`.

**Not in scope.** Gravity, defect emission, observational \(\gamma\) or
birefringence, any new coupling, any globally bounding modification of (1).
The original cubic remains unbounded; the fixture must record sampled energy
sign without treating a positive patch as a cure.

It is a demonstration fixture: the gate stays open on a Maxwell sector from a
*different* object (order-parameter recast or a non-gradient interaction), not
on this Hamiltonian.

**Outcome.** All frozen U0/U1/U2/B0/T0, stability, and refinement controls passed.
The independent symbol and actual time-evolution lanes agree to a maximum frequency relative
error of 6.58×10⁻⁵; the B0 squared-speed comparison is 0.00319 against its 0.02 bound.
The fixture found four longitudinal propagating roots, frozen transverse currents, and no
Gauss constraint. Its `refuted` result is therefore scoped to the proposition that this packet
Hamiltonian supplies a Maxwell sector; it supports the two corresponding model-property rows
without moving Kill condition B's nature-level status.
