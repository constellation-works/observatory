---
title: "Research Program Template"
summary: "Template for the charter and evidence contract of a numbered research program."
tags: [parallax, research, template]
related: ["docs/research/README.md", "docs/_templates/HYPOTHESIS.md", "docs/_templates/EXPERIMENT.md"]
created_on: 2026-08-03
updated_on: 2026-08-19
status: active
---

# Research program: TITLE

## Purpose

What class of questions belongs here, and which decisions could the evidence inform?

## Boundary

- **In scope:**
- **Out of scope:**
- **Consequential actions disabled by default:**

## Evidence contract

- **Observational unit:**
- **Data sources and provenance:**
- **Information cutoff:**
- **Baseline family:**
- **Primary metric family:**
- **Required evaluation split:**
- **Uncertainty and robustness requirements:**

## Safety and ethics

What privacy, consent, security, financial, medical, legal, or social risks apply?

## First question

Write it as `hypothesis/H<NN>-<title>.md`, implement the methodology under
`notebooks/RNN-title/ENN-<title>.ipynb` or `.py`, then write
`experiments/E<NN>-<title>.md` from that run before treating the result as
preregistered.
