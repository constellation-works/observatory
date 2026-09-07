---
title: "Hypothesis Template"
summary: "Template for a durable, falsifiable hypothesis within a numbered research program."
tags: [parallax, hypothesis, template]
related: ["docs/research/README.md", "docs/RESEARCH_PROTOCOL.md", "docs/_templates/EXPERIMENT.md"]
created_on: 2026-08-03
updated_on: 2026-08-19
status: draft
research_id: RNN
domain: domain-title
hypothesis_id: HNN
outcome: untested
---

# HNN: Hypothesis title

## Claim

State one falsifiable claim. Name the population, treatment or signal, response, direction, and
time horizon precisely enough that two researchers would test the same proposition.

## Motivation and mechanism

Why might the claim be true? Separate the proposed mechanism from the observable prediction; an
experiment may support the prediction without establishing the mechanism.

## Predicted observables

- **Primary prediction:**
- **Secondary predictions:**
- **Information cutoff:**

## Plausible alternatives

List competing explanations that could produce the same observation and the controls needed to
distinguish them.

## Baseline

Name the simplest credible alternative the hypothesis must beat.

## Rejection criteria

Define the evidence that would reject or materially weaken the claim before creating an experiment.

## Experiment queue

Link each `E<NN>-<title>.md` record created to test this hypothesis, and the matching
`notebooks/RNN-title/ENN-<title>` methodology. A hypothesis may have multiple experiments, but each
experiment names exactly one primary hypothesis.

## Decision history

Append dated decisions here. Use `untested`, `rejected`, `revised`, or `advanced`; never rewrite the
original claim after seeing a result.
