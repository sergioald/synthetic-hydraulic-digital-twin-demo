# Roadmap

This roadmap describes possible future improvements for the synthetic hydraulic
digital-twin demo. The project will remain confidentiality-safe: no real facility
data, partner data, proprietary parameters, control logic or private diagrams
will be added.

## Current status: v0.1.0

The current version provides a complete minimal research-software workflow:

- synthetic sensor data generation
- data validation
- feature engineering
- baseline energy modelling
- rule-based anomaly detection
- unsupervised anomaly detection baseline
- digital-twin state classification
- automated reporting
- example visual outputs
- tests and GitHub Actions CI
- documentation of assumptions and limitations

This version is suitable as a portfolio demonstration of applied AI, digital-twin
engineering, time-series monitoring and reproducible research-software practice.

## Planned improvements

### v0.2.0 — Stronger evaluation workflow

Potential additions:

- richer synthetic fault scenarios
- confusion-matrix style evaluation using synthetic ground-truth labels
- precision, recall and false-positive-rate summaries
- sensitivity analysis for anomaly thresholds
- comparison of rule-based and unsupervised anomaly-detection outputs
- improved tests for edge cases such as missing timestamps and sensor dropout

### v0.3.0 — Improved modelling layer

Potential additions:

- additional unsupervised anomaly-detection baselines
- simple forecasting baseline for expected pressure, flow or power behaviour
- residual-based anomaly detection
- model-card style documentation
- clearer separation between feature generation, model fitting and inference

### v0.4.0 — Better reporting and usability

Potential additions:

- richer automated report template
- command-line options for output folders and configuration files
- more example visualisations
- architecture diagram
- lightweight documentation site
- release archive with DOI

### v0.5.0 — Packaging and reproducibility polish

Potential additions:

- improved package metadata
- example configuration variants
- reproducible release workflow
- expanded CI checks
- optional Dockerfile or devcontainer
- Zenodo DOI for a stable release snapshot

## Out of scope

The following are intentionally out of scope for this public repository:

- real FastBlade data
- real acoustic, hydraulic or structural sensor exports
- confidential facility diagrams
- proprietary controller logic
- partner data
- internal reports
- calibrated operational thresholds
- production deployment instructions
- claims of operational safety certification

## Long-term direction

The long-term aim is to keep this repository as a clean public demonstration of
how applied AI and research-software practices can support industrial digital
twins:

- clear synthetic-data boundary
- reproducible workflows
- explainable baseline models
- automated validation and reporting
- CI-tested Python package structure
- documentation suitable for technical reviewers

Future extensions should preserve clarity and confidentiality rather than adding
complexity for its own sake.
