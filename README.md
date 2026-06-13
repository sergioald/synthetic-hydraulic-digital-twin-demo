# Synthetic Hydraulic Digital Twin Demo

[![Tests](https://github.com/sergioald/synthetic-hydraulic-digital-twin-demo/actions/workflows/tests.yml/badge.svg)](https://github.com/sergioald/synthetic-hydraulic-digital-twin-demo/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **synthetic applied-AI / research-software demo** for sensor-heavy hydraulic systems.

This repository shows how a digital-twin-style workflow can generate synthetic time-series data, validate sensor signals, estimate energy use, detect anomalies, classify operating states, and produce engineering-style reports — without exposing real facility data or proprietary control logic.

<p align="center">
  <img src="docs/assets/readme_workflow.png" alt="Synthetic hydraulic digital-twin workflow" width="900">
</p>

<p align="center">
  <em>A safe, reproducible public workflow for demonstrating applied AI on hydraulic sensor data.</em>
</p>

---

## Why this project exists

Real industrial and research facilities often produce valuable sensor data, but the raw data, controls, infrastructure details, and operating conditions cannot always be shared publicly.

This project demonstrates the same kind of applied-AI workflow using **fully synthetic data**. It is designed for portfolio review, research-software demonstration, teaching, and method discussion.

The project is intentionally explainable rather than physically exhaustive. It focuses on:

- clean software structure;
- reproducible examples;
- safe publication boundaries;
- sensor-data validation;
- energy and efficiency summaries;
- anomaly detection and state classification;
- report generation for engineering review.

For a more detailed reviewer-facing explanation, see [`docs/portfolio_summary.md`](docs/portfolio_summary.md).

---

## What this repository demonstrates

| Area | What is included |
|---|---|
| Synthetic data | Hydraulic-style time-series variables generated without real facility data |
| Validation | Range, missing-value, and consistency checks for sensor data |
| Feature engineering | Rolling statistics and derived engineering signals |
| Energy modelling | Electrical and hydraulic energy estimates plus efficiency summaries |
| Anomaly detection | Rule-based checks and an Isolation Forest baseline |
| Digital-twin states | Explainable state labels for review and reporting |
| Reporting | Markdown report generation with recommendations and summary metrics |
| Research software | CLI, config file, tests, docs, citation metadata, and reproducible examples |

---

## Example outputs

The figures below are generated from the repository's synthetic example run. They are included so the project can be understood before running the code.

### Digital-twin state counts

<p align="center">
  <img src="docs/assets/readme_state_counts.png" alt="Example digital-twin state counts" width="850">
</p>

<p align="center">
  <em>Example operating-state counts generated from synthetic data.</em>
</p>

### Energy-efficiency summary

<p align="center">
  <img src="docs/assets/readme_energy_summary.png" alt="Example energy-efficiency summary" width="760">
</p>

<p align="center">
  <em>Example electrical/hydraulic energy estimates and mean efficiency from the synthetic report.</em>
</p>

---

## Quick start

### 1. Create an environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 2. Run the example workflow

```bash
python examples/quickstart.py
```

Or run the CLI directly:

```bash
hydraulic-twin run \
  --config configs/default.yaml \
  --output reports/example_report.md \
  --data-output data/synthetic_run.csv
```

On Windows PowerShell:

```powershell
hydraulic-twin run `
  --config configs/default.yaml `
  --output reports/example_report.md `
  --data-output data/synthetic_run.csv
```

The generated CSV is ignored by Git because it is a reproducible output.

### 3. Regenerate example figures

```bash
python examples/create_example_figures.py
```

---

## Main outputs

| Output | Purpose |
|---|---|
| `data/synthetic_run.csv` | Generated synthetic sensor dataset |
| `reports/example_report.md` | Markdown engineering-style summary report |
| `reports/figures/` | Example portfolio figures generated from synthetic data |
| `docs/portfolio_summary.md` | Reviewer-facing explanation of the project value |

---

## Synthetic data boundary

This repository does **not** contain:

- real FastBlade data;
- real University of Edinburgh code;
- partner or industrial datasets;
- proprietary control logic;
- real facility diagrams;
- real hydraulic parameters;
- real sensor exports;
- confidential reports or database schemas.

All datasets, parameters, operating behaviours, labels, figures, and reports in this repository are synthetic.

See:

- [`docs/confidentiality_statement.md`](docs/confidentiality_statement.md)
- [`docs/system_abstraction.md`](docs/system_abstraction.md)
- [`docs/synthetic_data_design.md`](docs/synthetic_data_design.md)

---

## Method overview

The workflow is organised as a small but complete research-software pipeline:

```text
synthetic data generation
→ sensor validation
→ feature engineering
→ hydraulic/electrical energy estimation
→ anomaly detection
→ digital-twin state classification
→ markdown report generation
```

The anomaly-detection layer combines transparent rule-based checks with a simple Isolation Forest baseline. The digital-twin state classifier converts validation, anomaly, and energy-efficiency signals into interpretable state labels such as `normal`, `sensor_issue`, `pressure_loss_suspected`, and `inefficient_operation`.

---

## Development

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=hydraulic_twin --cov-report=term-missing
```

Run formatting/lint checks:

```bash
pre-commit run --all-files
```

---

## Repository structure

```text
synthetic-hydraulic-digital-twin-demo/
  README.md
  pyproject.toml
  LICENSE
  CITATION.cff
  CHANGELOG.md
  configs/
    default.yaml
  docs/
    portfolio_summary.md
    anomaly_detection_method.md
    confidentiality_statement.md
    development.md
    model_validation.md
    synthetic_data_design.md
    system_abstraction.md
    roadmap.md
    assets/
      readme_workflow.png
      readme_state_counts.png
      readme_energy_summary.png
  examples/
    quickstart.py
    create_example_figures.py
  reports/
    example_report.md
    figures/
  src/hydraulic_twin/
    anomaly_detection.py
    cli.py
    data_generation.py
    energy_model.py
    features.py
    reporting.py
    twin_state.py
    validation.py
  tests/
```

---

## Documentation

Useful supporting documents:

- [`docs/portfolio_summary.md`](docs/portfolio_summary.md) — reviewer-facing project explanation
- [`docs/synthetic_data_design.md`](docs/synthetic_data_design.md) — synthetic data design notes
- [`docs/anomaly_detection_method.md`](docs/anomaly_detection_method.md) — anomaly-detection approach
- [`docs/model_validation.md`](docs/model_validation.md) — validation and limitations
- [`docs/system_abstraction.md`](docs/system_abstraction.md) — abstraction boundary
- [`docs/confidentiality_statement.md`](docs/confidentiality_statement.md) — publication boundary
- [`docs/development.md`](docs/development.md) — development workflow
- [`docs/roadmap.md`](docs/roadmap.md) — possible next steps

---

## Status and limitations

This is a **synthetic portfolio and research-software demonstration**, not a calibrated hydraulic model and not an operational digital twin.

The current implementation prioritises:

- explainability;
- reproducibility;
- safe public communication;
- clean project structure;
- testable applied-AI workflow design.

Any engineering conclusions from the example report should be interpreted as synthetic decision-support outputs only.

---

## Citation / acknowledgement

This project was developed as a public portfolio and research-software example for applied AI, sensor data, anomaly detection, and digital-twin-style engineering workflows.

See [`CITATION.cff`](CITATION.cff) for citation metadata.

---

## License

MIT License. See [`LICENSE`](LICENSE).
