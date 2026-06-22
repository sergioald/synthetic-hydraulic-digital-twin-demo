# Reviewer guide

This guide is intended for recruiters, collaborators, technical reviewers and
research-software reviewers who want to understand the repository quickly.

## Five-minute review path

For a fast review, read these files in order:

1. [`README.md`](../README.md)
2. [`docs/portfolio_summary.md`](portfolio_summary.md)
3. [`docs/case_study.md`](case_study.md)
4. [`docs/validation_scope.md`](validation_scope.md)

This gives the main purpose, workflow, confidentiality boundary and validation
interpretation.

## Fifteen-minute review path

For a deeper review, inspect:

1. `configs/default.yaml`
2. `configs/scenarios/`
3. `examples/run_scenarios.py`
4. `src/hydraulic_twin/data_generation.py`
5. `src/hydraulic_twin/validation.py`
6. `src/hydraulic_twin/features.py`
7. `src/hydraulic_twin/anomaly_detection.py`
8. `src/hydraulic_twin/twin_state.py`
9. `src/hydraulic_twin/reporting.py`
10. `tests/`

This shows how configuration, synthetic data, validation, features, anomaly
detection, state classification and reporting connect.

## What to look for

### Software structure

The repository is organised as a Python package rather than a collection of
loose scripts. This supports:

- importable modules;
- command-line use;
- tests;
- documentation;
- reproducible examples;
- continuous integration.

### Reproducibility

The synthetic data generator uses fixed seeds through the configuration files.
This makes example runs and scenario tests reproducible.

### Configuration clarity

The scenario files in `configs/scenarios/` make the synthetic assumptions
visible. A reviewer can see which illustrative events are included without
reading the generator internals first.

### Explainability

The workflow favours interpretable features, rules, state labels and reports.
This is appropriate for an engineering-facing digital-twin demonstration where
users need to understand why a period was flagged.

### Testing practice

The test suite includes unit tests, integration tests, smoke tests and
scenario-configuration tests. This supports confidence in software behaviour,
while the validation-scope documentation avoids overstating scientific or
operational claims.

## What not to infer

Do not interpret this repository as:

- a calibrated hydraulic simulator;
- a validated condition-monitoring product;
- a real FastBlade dataset;
- a real facility digital twin;
- a safety-critical diagnostic tool;
- evidence of real fault-detection accuracy.

The repository is intentionally synthetic and public-safe.

## Suggested reviewer questions

Good questions to ask about this project include:

- How would the synthetic scenarios be replaced by real sensor exports?
- Which parts of the pipeline would need calibration before operational use?
- Which anomaly thresholds are purely illustrative?
- How would uncertainty be propagated into the report?
- How would domain experts review false positives and false negatives?
- How would this workflow scale to a live sensor database?
- Which parts would become MLOps components in an operational deployment?

## What this project says about the author

This repository is intended to demonstrate capability in:

- applied AI for engineering systems;
- digital-twin workflow design;
- time-series data processing;
- anomaly-detection baselines;
- engineering feature design;
- reproducible Python software;
- documentation and validation boundaries;
- safe public communication of confidential research-adjacent work.

## Suggested review commands

Install:

```bash
python -m pip install -e ".[dev]"
```

Run all tests:

```bash
pytest
```

Run checks:

```bash
pre-commit run --all-files
```

Run one scenario:

```bash
hydraulic-twin run \
  --config configs/scenarios/pressure_loss.yaml \
  --output reports/scenarios/pressure_loss_report.md \
  --data-output data/scenarios/pressure_loss_synthetic_run.csv
```

Run all scenarios:

```bash
python examples/run_scenarios.py
```
