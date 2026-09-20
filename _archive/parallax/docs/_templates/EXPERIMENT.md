---
title: "Experiment Template"
summary: "Template for preregistering methodology and preserving results and outcomes."
tags: [parallax, experiment, template]
related: ["docs/research/README.md", "docs/RESEARCH_PROTOCOL.md", "docs/_templates/HYPOTHESIS.md"]
created_on: 2026-08-03
updated_on: 2026-08-19
status: draft
research_id: RNN
domain: domain-title
experiment_id: ENN
hypothesis_id: HNN
preregistered: true
outcome: pending
---

# ENN: Experiment title

Replace the generic `related` links with the exact hypothesis, protocol, data contract, and artifact
records used by this experiment. Freeze the methodology before opening the final evaluation data.

Set `preregistered: false` when the data were viewed or the method evolved before the evaluation
contract was frozen. Such a record can never carry the `advance` outcome — an exploratory finding
becomes confirmatory only through a new preregistered experiment on data it has not seen.

## Question

What narrow question does this experiment answer, and what decision could the answer change?

## Methodology

### Design

- **Experimental or observational unit:**
- **Population and sampling frame:**
- **Treatment, signal, or intervention:**
- **Response and horizon:**
- **Known confounders and controls:**

### Data contract

- **Sources and provenance:**
- **Immutable dataset or snapshot identifier:**
- **Observation window:**
- **Information cutoff:**
- **Exclusions and missing-data policy:**

### Evaluation contract

- **Train, validation, and untouched test split:**
- **Baseline:**
- **Primary metric:**
- **Secondary metrics:**
- **Uncertainty method:**
- **Robustness checks:**
- **Parameter search and trial count:**
- **Costs or resource budget:**
- **Rejection criterion:**

### Protocol deviations

Record deviations after preregistration without erasing the frozen plan. A material deviation makes
the affected analysis exploratory and requires a new experiment for confirmation.

## Reproducibility

- **Code revision:**
- **Environment or lockfile:**
- **Random seeds:**
- **Command or notebook:** `notebooks/RNN-title/ENN-title.ipynb` or `.py` (required; run it and
  quote its labeled outputs)
- **Artifacts:**

## Results

Complete only after the frozen evaluation. Report the primary metric first, the baseline comparison,
uncertainty, robustness results, failures, and any deviations. Preserve null and negative results.

## Outcome

- **Decision:** `reject`, `revise`, `advance`, or `inconclusive` — `advance` requires
  `preregistered: true`
- **Rationale:**
- **Limitations:**
- **Next step:**

Unexpected findings generate a new `H<NN>-<title>.md`; they do not retroactively change this
experiment or its primary hypothesis.
