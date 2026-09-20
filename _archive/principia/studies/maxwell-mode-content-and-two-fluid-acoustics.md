---
title: "Maxwell plane-wave content versus two-fluid acoustics"
status: active
created: 2026-09-05
updated: 2026-09-05
---

# Maxwell plane-wave content versus two-fluid acoustics

The mode-and-constraint count that distinguishes a Maxwell photon sector from
ordinary two-component sound. This note is the established-physics comparator
for the packet-Hamiltonian linearization in
[theory/two-substance-vortex-vacuum](../theory/two-substance-vortex-vacuum/)
(ORB-11219). It does not adjudicate any two-substance model; it records what
Maxwell vacuum waves *are*, what two-fluid media *generically* carry, and why
equal characteristic speeds are not polarizations.

## Maxwell vacuum waves: two transverse polarizations, two constraints

Sourceless Maxwell equations in vacuum (Jackson, *Classical Electrodynamics*,
3rd ed., Wiley, 1998, Ch. 6 §6.1 and Ch. 7 §7.1):

\[
\nabla\cdot\mathbf{E}=0,\qquad
\nabla\cdot\mathbf{B}=0,\qquad
\nabla\times\mathbf{E}=-\partial_t\mathbf{B},\qquad
\nabla\times\mathbf{B}=c^{-2}\partial_t\mathbf{E}.
\]

Six first-order fields \((\mathbf{E},\mathbf{B})\). The two divergences are
**constraints**, not dynamical equations: they restrict the Cauchy data and are
preserved by Faraday and Ampère. Plane-wave substitution
\(\propto\exp[i(\mathbf{k}\cdot\mathbf{x}-\omega t)]\) with \(\mathbf{k}\ne0\)
turns them into \(\mathbf{k}\cdot\mathbf{E}=0\) and \(\mathbf{k}\cdot\mathbf{B}=0\).
The remaining Faraday–Ampère pair closes on the two components of \(\mathbf{E}\)
orthogonal to \(\mathbf{k}\), with \(\mathbf{B}=c^{-1}\hat{\mathbf{k}}\times\mathbf{E}\)
and \(\omega=\pm c|\mathbf{k}|\). Jackson §7.2: those two orthogonal directions
are two independent linear polarizations; general monochromatic data is a
complex combination of them (including circular polarization). Faraday’s law is
the restoring force for the transverse electric field — a **curl**, not a
gradient of a scalar potential.

Maxwell already identified the waves as *transverse* in the 1861–62 mechanical
model (“transverse undulations”; see
[vortex-atoms-and-quantized-circulation](vortex-atoms-and-quantized-circulation.md)
§ Maxwell’s vortex cells) and kept that content after removing the machinery
(Maxwell 1865, “A Dynamical Theory of the Electromagnetic Field”, *Phil. Trans.
R. Soc.* 155, 459–512, Part VI). The 1865 count is the one a substrate model
must match: two propagating transverse polarizations on one cone, Gauss
constraints killing longitudinal field, not two scalar sounds that happen to
share a speed.

**What this is not.** Two equal eigenvalues of a principal symbol are a
degenerate pair of whatever those eigenvectors already were. If both
eigenvectors are longitudinal density waves, degeneracy is one cone with two
scalar branches, not two photon polarizations. Polarization is an eigenvector
statement (the oscillating field is orthogonal to \(\mathbf{k}\)), not a
multiplicity statement.

## Two-fluid media: two longitudinal sounds

A medium with two independently moving components generically carries **two
scalar, longitudinal** branches — first sound (in-phase density/pressure) and
second sound (counterflow / entropy). Landau 1941, “The theory of
superfluidity of helium II”, *J. Phys. USSR* 5, 71; measured by Peshkov
1944, *J. Phys. USSR* 8, 381, with second-sound speed \(\sim 20\,\mathrm{m/s}\)
against first sound \(\sim 240\,\mathrm{m/s}\). The load-bearing statement and
the size of the splitting are recorded in
[superfluid-vacuum-and-emergent-gauge-fields](superfluid-vacuum-and-emergent-gauge-fields.md)
§ Two-fluid media carry two sounds. A single shared speed is the exception
that needs a mechanism (a locking symmetry, or Fermi-point-type protection),
not the default.

Those branches remain **longitudinal**: the oscillating current of each
component is parallel to \(\mathbf{k}\). Equalizing \(u_1\) and \(u_2\) by a
parameter choice would make the two cones coincide; it would not rotate the
eigenvectors into the transverse plane and would not manufacture Faraday’s
curl.

## Gradient-driven flux: transverse currents are frozen, not photons

In an ideal barotropic fluid the acceleration is minus the gradient of a
scalar (specific enthalpy). Helmholtz 1858 (“Über Integrale der
hydrodynamischen Gleichungen, welche den Wirbelbewegungen entsprechen”,
*J. reine angew. Math.* 55, 25–55) then implies that vortex lines are
permanent — circulation is conserved, vorticity is frozen into the flow. The
same identity holds for any continuum whose flux is kicked by
\(\partial_t\mathbf{j}=-\nabla\mu\) with \(\mu\) a local scalar: 
\(\partial_t(\nabla\times\mathbf{j})=-\nabla\times\nabla\mu=0\). Transverse
current is a **zero-frequency** mode of that force law, at finite amplitude,
not a propagating wave. It is the opposite of Maxwell’s transverse photon,
whose restoring force is the curl coupling of \(\mathbf{E}\) and \(\mathbf{B}\).

This is why a pair of conserved densities with gradient-driven fluxes is the
wrong kinematic type for a Maxwell sector, independently of how the two
scalar sound speeds are tuned. A theory that *does* deliver emergent photons
does it with additional structure — in Volovik’s program, the collective
coordinates of a topologically protected Fermi point acting as \(A_\mu\) and a
vierbein, a theorem about a universality class, not a speed-tuning
([superfluid-vacuum-and-emergent-gauge-fields](superfluid-vacuum-and-emergent-gauge-fields.md)).
That is a different object than two scalar densities.

## What this binds

For any claim that a two-density, gradient-driven apparatus is a Maxwell
sector: the Maxwell count is two propagating *transverse* polarizations plus
two Gauss constraints; the two-fluid default is two *longitudinal* sounds;
equal speeds are not polarizations; frozen transverse current is not a photon.
The packet-Hamiltonian algebra that applies this comparator lives in the
theory chapter, not here. Observational walls on birefringence, resonator
anisotropy, and \(\gamma=1\) remain
[lorentz-violation-bounds](lorentz-violation-bounds.md) and
[scalar-gravity-ppn-constraints](scalar-gravity-ppn-constraints.md).
