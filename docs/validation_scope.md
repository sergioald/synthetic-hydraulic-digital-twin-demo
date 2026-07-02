# Validation scope

This document summarises what is currently validated in the `synthetic-hydraulic-digital-twin-demo` repository, what is intentionally outside the validation scope, and what should be checked before using the workflows as examples for new research, teaching or portfolio outputs.

## Validation focus

This repository is public research software built around a fully synthetic applied-AI workflow for hydraulic-style sensor systems. The validation focus is on:

- reproducible execution of the main command-line workflow;
- correct handling of expected synthetic sensor columns and timestamps;
- lightweight checks of sensor validation, feature engineering, energy estimation, anomaly detection and state classification;
- smoke testing of the command-line interface;
- end-to-end checks of YAML scenario configurations;
- safe generation of Markdown and optional HTML reports;
- separation between reusable source code, synthetic data generation, generated outputs and confidential real-world material;
- clear documentation of what the public tests do and do not prove.

The tests are designed to support maintainable research software. They are not a substitute for physical validation against a real hydraulic facility.

## What is tested

The automated tests and development checks are intended to verify that:

- the Python package can be imported and run in an editable development environment;
- synthetic data generation returns the expected row structure and sensor columns;
- synthetic data generation is reproducible when fixed random seeds are used;
- timestamp and required-column checks behave as expected;
- validation catches missing required columns and basic data-quality issues;
- feature engineering creates derived pressure, flow, load, power, rolling-statistic and efficiency-related features;
- the energy model creates hydraulic/electrical energy and cumulative-energy fields;
- anomaly detection creates rule-based, machine-learning and combined anomaly flags;
- state classification adds interpretable digital-twin state labels and reasons;
- recommendations can be generated from synthetic state labels;
- Markdown reports contain the expected sections;
- optional HTML reports can be generated from the same synthetic workflow;
- the full pipeline can run from a YAML configuration file and write report/data outputs;
- scenario configuration files run end to end;
- generated outputs are reproducible and can be ignored by Git.

## What is not fully tested

The repository does not provide scientific or operational validation of a real hydraulic digital twin. In particular, the following are outside the lightweight public test scope:

- calibration against a real hydraulic rig or industrial test facility;
- validation against FastBlade, University of Edinburgh, partner or industrial datasets;
- verification of real sensor export formats;
- confirmation of real fault-diagnosis accuracy;
- operational false-positive or false-negative assessment;
- safety-critical suitability;
- hydraulic-system design validation;
- control-system validation;
- uncertainty propagation for real measurements;
- benchmarking against production monitoring systems;
- reproduction of confidential internal reports, figures or analyses.

The tests should therefore be interpreted as software and demonstration checks, not as evidence of real-world diagnostic performance.

## Synthetic model and data boundaries

All data, operating behaviours, labels, figures and reports in this repository are synthetic.

The repository separates:

- public reusable Python code;
- YAML configurations for synthetic scenarios;
- small generated examples and documentation assets;
- automated tests for public software behaviour;
- generated reports and CSV outputs;
- real, confidential or partner-specific materials, which must remain outside the repository.

Generated CSV and report outputs are reproducible. They should normally not be committed unless they are intentionally added as lightweight documentation or release assets.

## Expected behaviour

For a correctly formatted configuration file, the workflow should:

- generate a synthetic hydraulic-style sensor dataset;
- validate expected columns, timestamps, missing values and plausible ranges;
- compute derived features for pressure, flow, power, load, vibration proxy and efficiency;
- estimate hydraulic and electrical energy summaries;
- flag illustrative anomaly periods using rules and a baseline unsupervised method;
- classify rows into interpretable digital-twin state labels;
- generate recommendations that are clearly framed as synthetic decision-support text;
- write Markdown and, when requested, HTML reports;
- optionally write the classified synthetic dataset to CSV.

## Known limitations

- The synthetic data generator is illustrative and not physically calibrated.
- Scenario labels are injected by the synthetic workflow and are not operational truth.
- Thresholds are demonstration settings, not validated monitoring limits.
- The energy model is a simplified estimate and not a validated hydraulic power model.
- The anomaly-detection baseline is intended for workflow demonstration, not real deployment.
- State labels are review categories, not diagnostic conclusions.
- HTML and Markdown reports are presentation formats and do not change the validation status.
- Recommendations should not be interpreted as operational instructions.

## Recommended checks before reuse

Before adapting the repository for a new public example, users should:

- inspect the YAML configuration used for the run;
- confirm that all data remain synthetic;
- run the workflow on a small configuration first;
- inspect state counts, event counts and validation messages;
- review generated plots and reports before sharing outputs;
- document any changes to thresholds, scenario definitions or feature logic;
- avoid mixing private facility data with public example outputs;
- rerun tests and pre-commit checks before committing changes.

## Recommended checks before any real-data adaptation

If the workflow is ever adapted privately for real sensor exports, additional validation would be required before any operational interpretation. At minimum, this would include:

- documented data provenance and access permissions;
- sensor-unit and timestamp validation;
- calibration of pressure, flow, power and load channels;
- comparison with known operating events;
- domain-expert review of false positives and false negatives;
- uncertainty assessment;
- review of safety and operational implications;
- separation of private data and public repository materials.

Those checks are outside the current public repository scope.

## Development checks

Recommended local checks are:

```bash
python -m pip install -e ".[dev]"
pre-commit run --all-files
pytest
```

Optional report-generation check:

```bash
hydraulic-twin run \
  --config configs/default.yaml \
  --output reports/example_report.md \
  --html-output reports/example_report.html \
  --data-output data/synthetic_run.csv
```

On Windows PowerShell:

```powershell
hydraulic-twin run `
  --config configs/default.yaml `
  --output reports/example_report.md `
  --html-output reports/example_report.html `
  --data-output data/synthetic_run.csv
```

## Reviewer interpretation

A reviewer should treat this repository as evidence of:

- applied-AI workflow design;
- synthetic sensor-data generation;
- validation and feature-engineering structure;
- anomaly-detection implementation;
- digital-twin-style state classification;
- automated Markdown/HTML reporting;
- reproducible research-software practice;
- careful handling of confidentiality boundaries.

A reviewer should not treat this repository as evidence of a calibrated or operational hydraulic digital twin.
