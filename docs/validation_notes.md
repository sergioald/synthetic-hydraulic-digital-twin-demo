# Validation notes

This document provides practical validation notes for the synthetic hydraulic digital-twin demo.

It complements [`validation_scope.md`](validation_scope.md) by explaining how the repository should be reviewed, what the automated checks cover, and where the validation boundary ends.

## Validation level

The repository is validated as a **synthetic research-software demonstration**.

That means the checks are intended to show that:

- the code runs reproducibly;
- expected columns and outputs are created;
- synthetic scenarios can be executed from configuration files;
- reports are generated consistently;
- the public examples do not depend on private or confidential data;
- the workflow is suitable for portfolio, teaching, and method-review use.

The repository is **not** validated as an operational hydraulic monitoring system.

## Automated checks

The current tests cover the public software workflow, including:

- synthetic data generation;
- required sensor columns and timestamps;
- missing-value and range validation;
- feature engineering;
- hydraulic and electrical energy estimates;
- rule-based and unsupervised anomaly flags;
- digital-twin state classification;
- Markdown report generation;
- optional HTML report generation;
- command-line execution;
- scenario-configuration execution.

These checks help ensure that future changes do not silently break the public demo.

## Scenario validation

The scenario configurations in `configs/scenarios/` are designed to exercise expected software paths under controlled synthetic conditions.

They are useful for checking whether the pipeline behaves coherently for illustrative cases such as:

- normal operation;
- pressure loss;
- sensor drift;
- missing data;
- pump degradation;
- abnormal energy use;
- load-response anomaly;
- transient response;
- mixed synthetic events.

The scenarios are not measured fault cases and should not be treated as operational benchmark data.

## Report validation

The generated reports are validated as presentation outputs.

The checks verify that reports can be written and that expected sections are present. They do not prove that the recommendations are operationally correct.

Report text should be interpreted as synthetic decision-support wording for demonstration only.

## What has not been validated

The repository has not been validated against:

- real hydraulic rigs;
- real FastBlade data;
- University of Edinburgh facility data;
- partner or industrial datasets;
- real sensor exports;
- real fault labels;
- measured efficiency curves;
- safety-critical control requirements;
- operational maintenance decisions.

No claim is made that thresholds, anomaly flags, or state labels generalise to real systems.

## Human review checklist

Before presenting or extending the repository, review that:

- all examples still use synthetic data only;
- no generated outputs contain private paths or private identifiers;
- no real facility names are used as hidden calibration references;
- no raw sensor exports are included;
- no internal reports or diagrams have been copied;
- README claims remain consistent with the synthetic validation boundary;
- tests and pre-commit checks pass.

Suggested commands:

```bash
pre-commit run --all-files
pytest
```

Optional search checks:

```bash
git grep -n "password"
git grep -n "token"
git grep -n "C:\\"
git grep -n "/Users/"
git grep -n "confidential"
```

Manual review is still required because automated checks cannot detect every confidentiality or interpretation issue.

## Reviewer interpretation

A reviewer may reasonably interpret this repository as evidence of:

- applied-AI workflow design;
- research-software engineering;
- synthetic data generation;
- sensor validation;
- anomaly-detection implementation;
- digital-twin-style state classification;
- automated report generation;
- careful publication-boundary management.

A reviewer should not interpret this repository as evidence of:

- operational hydraulic digital-twin validation;
- real equipment fault-diagnosis accuracy;
- measured energy-performance modelling;
- safety-critical decision support;
- access to confidential facility data.
