# Model Validation Notes

This document describes how to interpret and validate the baseline synthetic hydraulic digital-twin workflow.

The repository is a public demonstration of applied-AI research software. It is not a calibrated operational digital twin. The validation approach therefore focuses on reproducibility, internal consistency, data-quality checks, sanity checks and clear limitations.

## Scope

The current workflow demonstrates:

```text
synthetic data generation
→ validation
→ feature engineering
→ energy estimation
→ anomaly detection
→ digital-twin state classification
→ recommendation/report generation
```

The workflow should be evaluated as a safe, synthetic and reproducible software artifact rather than as a real hydraulic model.

## Validation objectives

The validation objectives are:

1. **Data integrity**: required columns exist, timestamps are valid and missingness is visible.
2. **Feature consistency**: derived variables behave consistently with their definitions.
3. **Energy-model sanity**: energy and efficiency estimates are numerically plausible for the synthetic dataset.
4. **Anomaly-detection sanity**: injected synthetic events should be more likely to trigger anomalies than normal periods.
5. **State-classification explainability**: each digital-twin state should have a simple and understandable reason.
6. **Reproducibility**: running the same configuration should produce the same outputs.
7. **Publication safety**: no confidential data, real parameters or facility-specific information should enter the workflow.

## Data-validation checks

The validation layer checks the structure and basic plausibility of the input data.

Typical checks include:

- required columns are present;
- timestamps can be parsed;
- timestamps are monotonic increasing;
- duplicate timestamps are flagged;
- missing data rates are summarised;
- critical variables stay inside broad synthetic ranges;
- warnings and errors are reported explicitly.

Validation results are summarised in the markdown report. A validation failure should be interpreted as a warning that downstream metrics may not be meaningful.

## Feature-validation checks

Feature engineering creates derived variables such as:

- pressure difference;
- pressure-command residual;
- load-command error;
- power per unit flow;
- rolling averages;
- rolling standard deviations;
- z-score-like indicators;
- efficiency-change indicators.

Useful checks include:

- derived columns exist after feature generation;
- rolling features do not produce unexpected all-null columns;
- pressure-difference features respond to pressure-loss events;
- energy-intensity features increase during inefficient or abnormal-energy events;
- load-command error increases during injected load anomalies.

These checks can be expanded into additional tests as the project grows.

## Energy-model validation

The baseline energy model estimates hydraulic power using the common illustrative relation:

```text
hydraulic_power_kw = pressure_bar × flow_lpm / 600
```

It then compares hydraulic power with motor electrical power to estimate efficiency and cumulative energy.

Important outputs include:

- `hydraulic_power_kw`;
- `net_motor_power_kw`;
- `efficiency_estimate`;
- `electrical_energy_kwh`;
- `hydraulic_energy_kwh`;
- `cumulative_electrical_energy_kwh`;
- `cumulative_hydraulic_energy_kwh`.

Validation should check that:

- cumulative energy is non-decreasing;
- efficiency is finite where pressure, flow and power are available;
- abnormal-energy events increase electrical energy use;
- pressure-loss and degradation events affect efficiency-related features;
- energy metrics are not interpreted when critical sensors are missing.

The energy model is intentionally simple. It is a monitoring feature generator, not a calibrated hydraulic efficiency model.

## Anomaly-detection validation

The anomaly-detection layer combines rule-based checks and Isolation Forest scoring.

Recommended checks include:

- `rule_anomaly` is true when critical sensors are missing;
- `anomaly_reason` explains rule-based flags;
- `ml_anomaly` is generated for a reasonable fraction of samples;
- `combined_anomaly` is true whenever either the rule-based or ML detector fires;
- known synthetic event windows have higher anomaly rates than normal windows.

The synthetic `event_label` column can be used for these checks, but it should not be used as a model input.

## Digital-twin state validation

The digital-twin state classifier translates sensor and anomaly information into explainable operating states.

Current states include:

| State | Interpretation |
|---|---|
| `normal` | Synthetic baseline operation |
| `sensor_issue` | Critical pressure, flow or power value is missing |
| `pressure_loss_suspected` | Pressure delta is low under moderate/high demand |
| `inefficient_operation` | Estimated efficiency is below the synthetic threshold |
| `pump_degradation_suspected` | Temperature, vibration and efficiency indicators align |
| `load_response_anomaly` | Load demand and command signal are inconsistent |
| `transient_response` | Short-duration vibration or pressure transient detected |
| `investigate` | Rule-based or ML anomaly detector flagged the sample |

Validation should check that:

- every row receives a `twin_state`;
- every row receives a `twin_state_reason`;
- missing critical sensors are classified as `sensor_issue`;
- pressure-loss periods are classified as pressure-related states;
- abnormal energy or degradation periods are reflected in efficiency or degradation states;
- state counts are reported in the markdown report.

## Report validation

The markdown report should provide a concise engineering-style summary.

It should include:

- publication boundary;
- number of samples;
- validation status;
- anomaly count;
- energy estimates;
- mean efficiency;
- digital-twin state counts;
- synthetic event-label counts;
- validation messages;
- recommendations;
- limitations.

A useful report should be understandable without reading the full source code.

## Reproducibility checks

A minimal reproducibility check is:

```bash
python examples/quickstart.py
pytest
```

The generated results should be stable when using the same configuration and random seed.

GitHub Actions also checks the repository automatically through:

```text
pre-commit run --all-files
pytest
```

This supports a research-software workflow where formatting, basic repository hygiene and tests are checked on every commit.

## What is not validated yet

The current project does not yet validate:

- real-world hydraulic accuracy;
- calibrated component behaviour;
- controller performance;
- real fault detection performance;
- real sensor drift distributions;
- uncertainty intervals;
- long-term deployment behaviour;
- operator decision quality;
- safety-critical recommendations.

These are intentionally out of scope for the current public demo.

## Acceptance criteria for the current baseline

The current baseline is acceptable if:

1. all tests pass;
2. pre-commit checks pass;
3. the quickstart script runs successfully;
4. the generated report is readable;
5. validation warnings are explicit;
6. anomaly and state columns are produced;
7. no confidential or real facility-specific information is included.

## Future validation improvements

Possible future validation improvements include:

- synthetic scenario benchmark table;
- confusion matrix against synthetic event labels;
- anomaly-rate comparison by event type;
- threshold sensitivity analysis;
- stress tests for missing data;
- multiple random-seed robustness checks;
- model card for the anomaly detector;
- richer report plots;
- documented limitations for each derived metric.

The validation strategy should remain honest: the project demonstrates workflow competence and research-software discipline, not a production-certified hydraulic digital twin.
