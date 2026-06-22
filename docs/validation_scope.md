# Validation scope

This document explains what the repository tests are intended to prove, and what they are not intended to prove.

The project uses fully synthetic data to demonstrate an applied-AI workflow for hydraulic-style sensor systems. The tests therefore focus on software behaviour, reproducibility, data-shape expectations, and safe report generation. They do not validate the model against a real hydraulic rig or any confidential facility data.

## What the tests prove

The automated tests check that:

- synthetic data generation returns the expected columns and row structure;
- synthetic data generation is reproducible when a fixed random seed is used;
- generated timestamps and required sensor columns are valid enough for the demo workflow;
- validation catches missing required columns and basic data-quality problems;
- feature engineering adds the expected derived and rolling features;
- energy estimation adds hydraulic/electrical energy and efficiency columns;
- anomaly detection adds rule-based, machine-learning, and combined anomaly flags;
- twin-state classification adds interpretable state labels and reasons;
- report generation creates Markdown output with the expected sections;
- the full pipeline can run from a configuration file and write report/data outputs;
- the command-line interface can run a small smoke example without crashing.

These tests are useful for research-software quality because they check that the public workflow remains runnable, reproducible, and understandable as the repository evolves.

## What the tests do not prove

The tests do not prove that:

- the synthetic signals match any real hydraulic facility;
- the energy model is physically calibrated;
- the anomaly detector is operationally reliable on real equipment;
- the digital-twin state labels are valid diagnostic truth;
- the workflow is suitable for safety-critical decisions;
- the outputs generalise to real sensor exports;
- the thresholds are optimal for real monitoring;
- the software has been validated against FastBlade, University of Edinburgh, partner, or industrial datasets.

The tests should therefore be interpreted as software and demonstration checks, not as physical validation of a hydraulic system.

## Why this distinction matters

Terms such as *digital twin*, *anomaly detection*, *energy modelling*, and *state classification* can imply a high level of operational maturity. In this repository, those terms describe the structure of a safe, synthetic demonstration workflow.

The validation boundary is intentionally conservative:

- the repository demonstrates method structure;
- the data are synthetic;
- the logic is explainable and reproducible;
- the tests verify behaviour of the public code;
- no real facility, partner, or proprietary data are used.

## Suggested reviewer interpretation

A reviewer should treat this repository as evidence of:

- applied-AI workflow design;
- sensor-data processing;
- anomaly-detection implementation;
- digital-twin-style state classification;
- automated report generation;
- research-software engineering practice;
- safe publication of confidential-domain methods.

A reviewer should not treat this repository as evidence of a calibrated or operational hydraulic digital twin.

## Recommended future validation improvements

Possible future additions include:

- scenario-specific synthetic test cases with known injected faults;
- benchmark tests comparing expected and detected synthetic events;
- uncertainty ranges for synthetic sensor noise and energy estimates;
- regression tests for generated reports and figures;
- documented assumptions for each synthetic scenario;
- a model-card-style summary for the anomaly-detection layer.
