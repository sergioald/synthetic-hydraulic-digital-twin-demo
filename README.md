# Synthetic Hydraulic Digital Twin Demo

A synthetic applied-AI research software demo for sensor-heavy hydraulic systems.

This repository demonstrates a reproducible Python workflow for generating synthetic hydraulic-system time series, validating sensor data, estimating energy use, detecting anomalies, classifying digital-twin operating states and producing engineering-style reports.

The project is designed as a public portfolio/research-software example. It is inspired by general experience with structural testing, monitoring systems and digital-twin workflows, but it does **not** reproduce any real facility, dataset, control system or proprietary architecture.

## Why this project exists

Many industrial and research systems generate large volumes of sensor data but cannot share the real data, controls or infrastructure publicly. This project shows how to communicate applied-AI capability safely using fully synthetic data and a transparent, testable software structure.

The intended audience includes research software teams, applied-AI groups, industrial digital-twin teams and organisations working on sensor monitoring, energy efficiency, anomaly detection or decision support.

## Planned workflow

```text
synthetic data generation
→ data validation
→ feature engineering
→ hydraulic/electrical energy estimation
→ anomaly detection
→ digital-twin state classification
→ recommendation/report generation
```

## Repository status

This first commit defines the project structure, confidentiality boundary and development standards. Source code, tests, examples and generated reports will be added in subsequent commits.

## Confidentiality boundary

This repository does not contain:

- real FastBlade data
- real University of Edinburgh code
- partner or industrial data
- proprietary control logic
- real facility diagrams
- real hydraulic parameters
- real sensor exports
- confidential reports or database schemas

All future datasets, parameters and operating behaviours in this repository will be generated synthetically.

See [`docs/confidentiality_statement.md`](docs/confidentiality_statement.md) and [`docs/system_abstraction.md`](docs/system_abstraction.md) for the publication boundary.

## Planned project structure

```text
synthetic-hydraulic-digital-twin-demo/
  README.md
  pyproject.toml
  LICENSE
  .gitignore
  .pre-commit-config.yaml
  configs/
    default.yaml
  docs/
    confidentiality_statement.md
    system_abstraction.md
    development.md
  .github/
    workflows/
      tests.yml
```

Later commits will add:

```text
src/hydraulic_twin/
  data_generation.py
  validation.py
  features.py
  energy_model.py
  anomaly_detection.py
  twin_state.py
  reporting.py
  cli.py

tests/
examples/
reports/
```

## Development

Install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Install the pre-commit hooks:

```bash
pre-commit install
```

Run repository checks manually:

```bash
pre-commit run --all-files
```

Once source code and tests are added, run the test suite with:

```bash
pytest
```

See [`docs/development.md`](docs/development.md) for more details.

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE).
