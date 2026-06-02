# Anomaly Detection Method

This document describes the baseline anomaly-detection method used in the synthetic hydraulic digital-twin demo.

The current method combines transparent engineering-style rules with an unsupervised machine-learning detector. The goal is not to claim state-of-the-art anomaly detection. The goal is to demonstrate a reproducible and explainable monitoring workflow that can be reviewed, tested and extended.

## Pipeline position

Anomaly detection is applied after:

```text
synthetic data generation
→ data validation
→ feature engineering
→ hydraulic/electrical energy estimation
```

The detector uses measured and derived signals. It should not use `event_label` as an input feature because that label represents synthetic ground truth for evaluation and demonstration.

## Inputs

The anomaly-detection stage expects a dataframe containing synthetic sensor signals and engineered variables such as:

- `high_pressure_bar`;
- `return_pressure_bar`;
- `flow_lpm`;
- `motor_power_kw`;
- `motor_temperature_c`;
- `vibration_proxy`;
- `command_signal_pct`;
- `load_demand_kn`;
- `pressure_delta_bar`;
- `efficiency_estimate`;
- `load_command_error_kn`.

The exact set of available features can grow over time as the project develops.

## Rule-based anomaly detection

The rule-based detector creates transparent flags based on simple monitoring logic.

The current rules include:

| Rule | Example interpretation |
|---|---|
| `critical_sensor_missing` | A critical pressure, flow or power measurement is missing |
| `low_pressure_delta` | Pressure difference is unexpectedly low under demand |
| `low_efficiency` | Estimated efficiency falls below a synthetic threshold |
| `high_temperature` | Motor temperature exceeds a synthetic threshold |
| `abnormal_energy_use` | Motor power is high relative to recent rolling behaviour |
| `load_response_mismatch` | Load demand and command response are inconsistent |
| `vibration_spike` | Vibration proxy exceeds a high synthetic quantile |

The output columns are:

| Output | Meaning |
|---|---|
| `rule_anomaly` | `True` if one or more rules fired |
| `anomaly_reason` | Semicolon-separated list of rule names |

### Why use rules?

Rules are useful because they are:

- easy to explain to engineers and reviewers;
- easy to test;
- useful as a baseline;
- helpful when labelled training data is unavailable;
- transparent enough for early-stage decision support.

They also help separate the monitoring logic from a purely black-box model.

## Machine-learning anomaly detection

The ML component uses an unsupervised Isolation Forest.

Isolation Forest is useful here because:

- it can work without labelled failures;
- it handles multivariate patterns;
- it provides a simple anomaly score;
- it is widely available in scikit-learn;
- it is appropriate as a baseline for tabular engineered features.

Before fitting the model, the pipeline:

1. selects numeric and boolean features;
2. imputes missing values using the median;
3. standardises numeric variables;
4. fits the Isolation Forest;
5. converts model outputs into anomaly flags and scores.

The output columns are:

| Output | Meaning |
|---|---|
| `ml_anomaly` | `True` if the Isolation Forest identifies the sample as anomalous |
| `ml_anomaly_score` | Higher values indicate stronger model-based abnormality |

## Combined anomaly flag

The combined anomaly flag is:

```text
combined_anomaly = rule_anomaly OR ml_anomaly
```

This means a sample is flagged if either the transparent rules or the ML model detects abnormal behaviour.

This approach is useful for a first public demo because it combines interpretability and multivariate detection.

## Configuration

The main parameter is the Isolation Forest contamination rate:

```yaml
anomaly_detection:
  isolation_forest_contamination: 0.04
```

This tells the model the approximate fraction of samples expected to be anomalous. The value is synthetic and illustrative. It is not a calibrated operational threshold.

Other thresholds, such as temperature limits and efficiency cut-offs, are also synthetic demonstration values.

## Relationship to digital-twin state classification

The anomaly detector answers:

```text
Is this sample unusual?
```

The digital-twin state classifier answers:

```text
What kind of operating condition does this sample most resemble?
```

For example, an anomaly might later be classified as:

- `sensor_issue`;
- `pressure_loss_suspected`;
- `inefficient_operation`;
- `pump_degradation_suspected`;
- `load_response_anomaly`;
- `transient_response`;
- `investigate`.

This separation keeps the workflow easier to reason about.

## Evaluation approach

Because the data is synthetic, the `event_label` column can be used for sanity checks. For example, a reviewer can check whether known synthetic event periods are more likely to be flagged than normal periods.

However, the current repository does not claim that `event_label` represents real labelled failure data. It should be treated as a simulation aid.

Recommended evaluation checks include:

- anomaly rate during normal vs injected event periods;
- number of missing-data points flagged as sensor issues;
- whether abnormal-energy periods increase `ml_anomaly_score`;
- whether pressure-loss periods are reflected in pressure-related rules;
- whether pump-degradation periods show lower efficiency and higher temperature/vibration indicators.

## Known limitations

The current method has important limitations:

- thresholds are synthetic and not calibrated;
- the Isolation Forest is fitted on the same run it scores;
- no independent validation set is currently used;
- no uncertainty intervals are provided;
- no real failure labels are available;
- false positives and false negatives are not yet formally quantified;
- event types may overlap in derived feature space;
- the method is not suitable for operational use.

These limitations are documented deliberately. The purpose of the project is to show a responsible baseline workflow, not to overclaim model performance.

## Future improvements

Possible future improvements include:

- scenario-level train/test splits;
- explicit precision/recall metrics against synthetic event labels;
- threshold sensitivity analysis;
- rolling or online anomaly scoring;
- alternative models such as robust covariance, one-class SVM or autoencoders;
- uncertainty-aware anomaly scoring;
- model cards for each detector;
- richer visual diagnostics in the report.

Any future improvement should preserve explainability and the synthetic-data publication boundary.
