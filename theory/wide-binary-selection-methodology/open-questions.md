## Open questions

- Who builds the Orrery fixture, and under what task? This doc and its gate freeze the
  protocol; the sim itself is explicitly out of scope here (principia judges theory and
  literature, Orrery runs the apparatus) and is not yet filed.
- If R1 fires (a populated bin exceeds the predeclared threshold), does the follow-up isolate
  *which* cut (theta/s window, PM-escape gate, magnitude truncation, or the photometric
  mass-luminosity scatter) is responsible, or only that the pipeline as a whole is miscalibrated
  under the tested footprint? The current protocol's run matrix (cap ladder, wrap/polar
  placements) gives partial isolation but does not ablate each cut independently — a natural v2
  if R1 fires.
- Is the predeclared effect-size threshold (0.04 in median v-tilde) the right operating point,
  or should it track a specific literature number (e.g. Banik et al. 2024's quoted anomaly
  upper bound) more tightly once that bound is sourced with a verified citation to a specific
  number rather than the qualitative "null at high significance" framing used in this protocol's
  references?
- Does a real (not synthetic) nonuniform footprint — e.g. a Gaia cone straddling the Galactic
  plane, where dust and crowding actually vary the completeness gradient this protocol only
  approximates — change the verdict? Out of scope for the offline, CPU-bounded pilot; a
  candidate v2 if the synthetic pilot is inconclusive.
