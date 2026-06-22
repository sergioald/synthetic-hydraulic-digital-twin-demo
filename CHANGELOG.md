# Changelog

All notable changes to this project will be documented in this file.

This project follows a simple versioned release structure. The first public
release is intended as a confidentiality-safe portfolio and research-software
demonstration.

## [0.2.0] - Unreleased

### Added

- Synthetic scenario configurations for normal operation and illustrative
  fault-like conditions:
  - pressure loss
  - sensor drift
  - missing critical data
  - pump degradation
  - abnormal energy use
  - load-response anomaly
  - transient response
  - mixed synthetic faults
- Scenario runner for generating one report and one synthetic CSV output per
  scenario.
- Scenario-configuration documentation explaining purpose, usage and
  interpretation boundaries.
- Validation-scope documentation clarifying what the tests do and do not prove.
- Unit tests for feature engineering, reporting and recommendations.
- Integration tests for configured full-pipeline execution.
- CLI smoke test.
- Scenario-configuration tests.
- README scenario overview section and scenario workflow figure.
- Repository `.gitignore` rules for Python caches, build artifacts and
  reproducible generated outputs.
- Reviewer-facing case-study documentation.
- Reviewer guide for quick portfolio and research-software assessment.
- Release checklist for preparing a public `v0.2.0` GitHub release.
- GitHub repository description and topic recommendations.

### Changed

- Improved README structure to make the scenario-based workflow, validation
  boundaries and generated-output policy easier to understand.
- Strengthened the repository's position as a public, synthetic analogue of
  applied-AI and digital-twin workflows for sensor-heavy hydraulic systems.
- Made testing and validation claims more explicit to avoid implying operational
  calibration or safety-critical readiness.

### Notes

- The scenario configurations are synthetic demonstrations only.
- Generated scenario CSV files and scenario reports are reproducible outputs and
  should normally not be committed.
- The repository still does not include real FastBlade data, partner data,
  facility-specific parameters, raw sensor exports, proprietary control logic or
  confidential operational documentation.

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
