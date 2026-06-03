# Portfolio Summary

This repository is a compact public demonstration of applied AI and research-software practice for sensor-heavy engineering systems.

It is designed to show how a private or confidential digital-twin workflow can be communicated safely using fully synthetic data, clear documentation, automated tests and continuous integration.

## What the project demonstrates

The workflow starts from generated synthetic sensor data and runs through a complete monitoring pipeline:

```text
synthetic sensor data
→ validation
→ feature engineering
→ energy and efficiency estimation
→ anomaly detection
→ digital-twin state classification
→ recommendations and markdown reporting
```

The emphasis is not hydraulic realism. The emphasis is reproducible structure, explainable baselines, data-quality awareness and safe public communication of applied-AI methods.

## Example visual outputs

The following figures are generated from the synthetic pipeline and stored in `reports/figures/`.

### Digital-twin state timeline

![Synthetic anomaly and digital-twin state timeline](../reports/figures/anomaly_timeline.png)

This figure shows how the baseline digital-twin classifier translates synthetic sensor behaviour into operating states such as `normal`, `investigate`, `pressure_loss_suspected`, `sensor_issue` and `inefficient_operation`.

### Energy-efficiency summary

![Synthetic energy-efficiency summary](../reports/figures/energy_efficiency_summary.png)

This figure summarises the rolling synthetic efficiency estimate and reports cumulative synthetic electrical and hydraulic energy estimates.

### Pressure-flow overview

![Synthetic pressure-flow overview](../reports/figures/pressure_flow_overview.png)

This figure compares normalised high-pressure and flow-rate signals to give a quick view of the synthetic operating envelope.

## Why this is relevant for applied-AI roles

The project provides evidence of capability in several areas that are difficult to show publicly when real industrial or research data is confidential:

- synthetic data generation for safe publication
- time-series sensor validation
- explainable feature engineering
- baseline energy and efficiency modelling
- rule-based and machine-learning anomaly detection
- interpretable digital-twin state classification
- automated markdown reporting
- Python packaging, tests, pre-commit and GitHub Actions

## Confidentiality boundary

This is a public synthetic demonstration. It does not include real FastBlade data, University of Edinburgh code, partner data, proprietary control logic, facility diagrams, component parameters, database schemas or confidential reports.

All values, events, figures and recommendations are generated synthetically and should not be interpreted as operational advice.

## How to regenerate the figures

From the repository root, run:

```bash
python examples/create_example_figures.py
```

The script runs the synthetic pipeline and writes updated figures to:

```text
reports/figures/
```
