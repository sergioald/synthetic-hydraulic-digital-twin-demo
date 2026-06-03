# Changelog

All notable changes to this project will be documented in this file.

This project follows a simple versioned release structure. The first public
release is intended as a confidentiality-safe portfolio and research-software
demonstration.

## [0.1.0] - 2026-06-03

### Added

- Initial public synthetic hydraulic digital-twin demo.
- Synthetic sensor data generation for a generic hydraulic test system.
- Configuration-driven data-generation workflow.
- Data validation checks for schema, timestamps, missing values and plausible ranges.
- Feature engineering for pressure, flow, load, power, rolling statistics and efficiency indicators.
- Baseline energy model for hydraulic power, electrical power and cumulative energy estimates.
- Rule-based anomaly detection for pressure loss, inefficient operation, high temperature, load mismatch, vibration spikes and missing sensor values.
- Isolation Forest baseline for unsupervised anomaly detection.
- Digital-twin state classification layer.
- Automated Markdown reporting.
- Example portfolio figures:
  - anomaly timeline
  - energy-efficiency summary
  - pressure-flow overview
- Technical documentation covering:
  - confidentiality boundary
  - synthetic data design
  - system abstraction
  - anomaly-detection method
  - model-validation approach
  - development workflow
- Continuous integration with GitHub Actions.
- Pre-commit checks with Ruff and standard file-quality hooks.
- Unit tests for the core synthetic data and digital-twin workflow.

### Notes

- This repository uses fully synthetic data.
- It does not include real FastBlade data, partner data, facility-specific parameters,
  control logic, raw sensor exports, diagrams, reports or confidential operational details.
- The project is intended as a public, reproducible analogue of industrial
  sensor-monitoring and digital-twin workflows.
