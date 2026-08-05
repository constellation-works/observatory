---
title: "Common Research Protocol"
summary: "The domain-neutral evidence contract shared by every numbered Parallax research program."
tags: [parallax, research, preregistration, reproducibility]
related: ["docs/ARCHITECTURE.md", "docs/research/README.md"]
created_on: 2026-07-31
updated_on: 2026-08-03
status: active
---

# Common research protocol

Every durable study freezes its question, hypothesis, baseline, method, primary metric, information
cutoff, and invalidation criterion before final evaluation. Outcomes are appended as reject,
revise, or advance; they never replace the original claim.

The domain-neutral contract is implemented by `parallax research`. A numbered research protocol
may add stricter requirements but cannot weaken this common contract.

## Durable record sequence

1. Form one falsifiable claim in `hypothesis/H<NN>-<title>.md` using the generic hypothesis
   template. Freeze its baseline, alternatives, and rejection criteria.
2. Create `experiments/E<NN>-<title>.md` for one test of that primary hypothesis. Link the hypothesis
   in `related` and in `hypothesis_id`.
3. Freeze the methodology before opening final evaluation data.
4. Append results, protocol deviations, and an outcome without editing the frozen question or plan.
5. Update both registries. A revision or unexpected finding receives a new hypothesis identity.

Hypothesis and experiment counters are independent, zero-padded, scoped to an `RNN` program, and
never recycled. One hypothesis can motivate many experiments; one experiment has exactly one
primary hypothesis.

The local journal and datasets live under the same `data/RNN-title/` identity. An experiment links
every cross-program input to its owning data contract and immutable snapshot.

## Common experiment record

Every durable experiment records:

- research id, domain, and the decision the research could inform;
- question, hypothesis, and plausible alternative explanations;
- exact point-in-time dataset, provenance, observation window, and information cutoff;
- train, validation, and untouched test partitions appropriate to the data-generating process;
- simplest credible baseline and primary metric;
- parameter-search space and number of trials;
- uncertainty, robustness checks, and known failure modes;
- code revision, environment, reproducible command, and artifact locations; and
- decision: reject, revise, advance, or inconclusive.

Exploration may generate a new hypothesis, but it does not retroactively become confirmatory
evidence. Register the new claim as a new hypothesis and test it in a new experiment.

## The preregistration declaration

Every experiment record declares `preregistered: true` or `preregistered: false` in its
frontmatter. Without it the `ENN` record type means two incompatible things — a plan frozen before
the data was opened, and a write-up of work already done — and a reader cannot tell them apart
because both carry the same headings.

- `preregistered: true` — the methodology was frozen before the final evaluation data was opened.
- `preregistered: false` — the data were viewed or the method evolved first. The record is still
  worth keeping: an honest exploratory write-up, including a negative one, is how a claim earns a
  real test later. State in `## Study status` what was seen before the design was written.

A `preregistered: false` record may reach `reject`, `revise`, or `inconclusive`, and may report
findings interesting enough to justify further work. It may **never** reach `advance`. Promotion
requires a new preregistered experiment run on data the exploration has not seen. Repository tests
enforce this; it is not left to the author's judgment, because the moment it matters is exactly the
moment the author is most invested in the result.

An exploratory record that survives a calibration or a placebo control is stronger than one that
does not, and should say so. It is still exploratory.
