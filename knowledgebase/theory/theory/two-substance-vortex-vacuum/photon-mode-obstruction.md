# Photon gate: phase modes and the cost of locking

Analytic attempt, 2026-09-04, under the existing
`two-substance-photon-sector` existence gate. **Conditional result, not a family-wide
refutation:** a regular, isotropic two-phase superfluid cannot identify its linear
phase waves with Maxwell photons. Equalizing their speeds does not supply transverse
polarizations. Josephson locking removes a gapless phase but puts the proposed charged
windings on domain walls. Renaming two substances as two components alone fixes neither.

The registered nature claim `two-substance-kill-condition-b` remains **untested**.
This chapter specifies an obstruction within an explicit effective theory, not an
adjudication of every microscopic completion. No new experiment or nature claim is added.

## Assumptions and the quadratic action

Take the [mechanics](mechanics.md) at its ordinary two-superfluid reading: two nonzero
condensates with phases \(\theta=(\theta_1,\theta_2)^T\), separately conserved substance
numbers, a homogeneous isotropic rest background, and no independent gauge or orientational
field. Work away from vortex cores, at long wavelengths, with nonsingular positive
compressibility and stiffness matrices. Density fluctuations are auxiliary at leading
derivative order; eliminating them gives

\[
\mathcal L_2=\tfrac12\dot\theta^T K\dot\theta
-\tfrac12\sum_i(\partial_i\theta)^T R(\partial_i\theta),
\qquad K=K^T>0,\quad R=R^T>0.
\]

Off-diagonal entries allow density coupling and entrainment. Independent constant phase
shifts forbid a phase mass term. This is a specified hydrodynamic class, not a deduction
that the corpus has already supplied a microscopic action. Singular incompressible limits,
vortex condensates, additional gapless fields, and anisotropic backgrounds are outside it.
The binary-condensate precedent and its limitations are sourced in
[two-component phase locking](../../studies/two-component-phase-locking.md).

For a plane wave,

\[
(\omega^2K-k^2R)a=0,\qquad
c_{1,2}^2=\operatorname{eig}(K^{-1/2}RK^{-1/2}).
\]

There are two positive acoustic eigenvalues. Requiring both to equal \(c^2\) makes the
real symmetric matrix \(K^{-1/2}RK^{-1/2}=c^2I\), hence **\(R=c^2K\)**. This can be
imposed or protected by additional structure; it is not automatic from two components.
Even when it holds, there are still two scalar modes.

At linear order each superfluid velocity is proportional to \(\nabla\theta_a\), and
entrained currents are linear combinations of these gradients. Thus all these currents
are parallel to \(\mathbf k\). Rotating about \(\mathbf k\) leaves the phase amplitudes
unchanged. The two internal labels do not become the two spatial transverse polarizations
of a Maxwell field. A local rotation-covariant vector constructed linearly from these
scalars and derivatives is likewise longitudinal; taking its curl gives zero. Nonlinear
composites or a new phase with emergent gauge structure require a separate derivation.

Consequently **two different sound speeds are not, by themselves, optical birefringence**:
one must first identify the photon and how it couples to matter. Equal sound speeds are
also insufficient to pass this gate. Counting two amplitudes is insufficient to identify
their transformation under spatial rotations.

## The tempting repair changes the charge sector

As a diagnostic alternative, explicitly relax separate substance-number conservation and
add a Josephson energy \(J[1-\cos(\theta_1-\theta_2)]\), with \(J>0\). This is a new
interaction being examined, **not adopted as a derived law**. Set \(v=(1,-1)^T\).
At \(k=0\), its quadratic mass matrix is \(Jvv^T\), giving

\[
\omega^2=0,\qquad \omega_J^2=Jv^TK^{-1}v.
\]

One phase becomes gapped; the surviving common-phase excitation is still scalar.
The full potential also exposes a topological cost hidden by that linear calculation.
Minimizing over the common-phase gradient leaves the static relative phase
\(\phi=\theta_1-\theta_2\) with

\[
E_\phi=\int d^3x\left[\tfrac12\rho_{\rm rel}|\nabla\phi|^2
+J(1-\cos\phi)\right],\qquad
\rho_{\rm rel}=(v^TR^{-1}v)^{-1}.
\]

A planar \(2\pi\) sine-Gordon wall has width
\(\ell_J=\sqrt{\rho_{\rm rel}/J}\) and tension
\(T=8\sqrt{\rho_{\rm rel}J}\). These follow by the first integral
\(\rho_{\rm rel}(\phi')^2/2=J(1-\cos\phi)\) and integration from 0 to \(2\pi\).

Now apply the family's own charge assignment:

\[
\oint d\phi=2\pi(w_1-w_2)=-2\pi q/e.
\]

A defect with nonzero proposed charge therefore winds the **locked** relative phase.
It must carry a wall, meet another defect that cancels the relative winding, or terminate
the wall on a boundary. For long parallel vortex lines the wall energy per unit length
grows linearly with their separation once that separation exceeds \(\ell_J\). In this
regime the electron assignment \((1,0)\) and proton assignment \((0,1)\) both acquire
this cost; a combined \((1,1)\) winding is neutral and avoids the relative-phase wall.
It does not selectively explain why only proton constituents confine.

This is an obstruction for the stated vortex-line charge realization, not a proof about
all localized three-dimensional particles. Closed loops, wall decay, finite boundaries,
and core dynamics require their own analysis. The result also does **not** mean that an
existing winding can simply disappear while both order parameters stay nonzero on its
contour: explicit symmetry breaking, number conservation, and winding conservation are
different statements.

The control is \(J=0\): the relative gap and wall tension vanish, independent phase
symmetry returns, and both scalar acoustic branches remain. Increasing entrainment
without breaking that symmetry changes \(K,R\); it does not generate this gap.

## What would move the existing gate

This closes the two easy algebraic shortcuts within the assumptions above: matching
speeds, and gapping the relative phase. The broader gate remains open. Its next owed
object should be an explicit action and constraint structure that produce a transverse
gauge sector, with a declared regime in which the phase-only assumptions cease to apply.
The proposal must show both its linear polarization content and its defect couplings;
inserting a Maxwell field would be a postulate, not its emergence.

Merely calling \((\psi_1,\psi_2)\) one order parameter leaves the calculation unchanged.
A useful recast must change the symmetry, constraints, or phase of matter. It must also
explain whether the charge assignment survives. A single shared propagation cone for
defects and gauge excitations, absence of observable frame effects, and the gravitational
light sector remain further obligations. No inference about those follows from this
flat-background mode calculation, and no universal-cone theorem is borrowed from the
corpus's Volovik analogy.
