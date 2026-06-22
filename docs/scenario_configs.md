# Synthetic scenario configurations

This document explains the scenario-based configuration files in `configs/scenarios/`.

The scenarios provide small, reproducible synthetic examples for exercising the digital-twin workflow under different illustrative operating conditions. They are intended for demonstrations, tests, documentation, and portfolio review.

They do not represent real hydraulic operating conditions, real facility parameters, real control logic, or real fault data.

## Available scenarios

| Scenario | File | Purpose |
|---|---|---|
| Normal baseline | `configs/scenarios/normal.yaml` | Synthetic run with no injected fault event beyond normal operation |
| Pressure loss | `configs/scenarios/pressure_loss.yaml` | Illustrative pressure-loss event |
| Sensor drift | `configs/scenarios/sensor_drift.yaml` | Illustrative pressure-sensor drift |
| Missing data | `configs/scenarios/missing_data.yaml` | Illustrative missing critical sensor values |
| Pump degradation | `configs/scenarios/pump_degradation.yaml` | Illustrative temperature, vibration, and efficiency degradation |
| Abnormal energy | `configs/scenarios/abnormal_energy.yaml` | Illustrative high energy-use period |
| Load anomaly | `configs/scenarios/load_anomaly.yaml` | Illustrative command/load mismatch |
| Transient event | `configs/scenarios/transient_event.yaml` | Illustrative short transient response |
| Mixed faults | `configs/scenarios/mixed_faults.yaml` | Combined synthetic scenario containing multiple illustrative events |

## Run one scenario

From the repository root:

```bash
hydraulic-twin run \
  --config configs/scenarios/pressure_loss.yaml \
  --output reports/scenarios/pressure_loss_report.md \
  --data-output data/scenarios/pressure_loss_synthetic_run.csv
```

On Windows PowerShell:

```powershell
hydraulic-twin run `
  --config configs/scenarios/pressure_loss.yaml `
  --output reports/scenarios/pressure_loss_report.md `
  --data-output data/scenarios/pressure_loss_synthetic_run.csv
```

## Run all scenarios

```bash
python examples/run_scenarios.py
```

This creates one report and one CSV file per scenario:

```text
reports/scenarios/
data/scenarios/
```

The generated CSV files are reproducible synthetic outputs. They do not need to be committed unless you intentionally want to publish small example outputs.

## Test all scenario configs

```bash
pytest tests/test_scenario_configs.py
```

Or run the full suite:

```bash
pytest
```

## Configuration design

Each scenario changes only the `events.include` list, the random seed, and a few lightweight execution parameters. This keeps the scenarios easy to understand and avoids implying that they are calibrated physical models.

Example:

```yaml
events:
  include:
    - normal
    - pressure_loss
```

The synthetic data generator begins with normal operation and injects only the requested illustrative events.

## Interpretation boundary

These scenarios demonstrate software behaviour:

- configuration-driven execution;
- repeatable synthetic data generation;
- pipeline execution from YAML files;
- report and CSV generation;
- state-classification behaviour under known synthetic event labels.

They do not validate:

- real hydraulic physics;
- real sensor fault behaviour;
- operational diagnostic reliability;
- safety-critical monitoring decisions;
- calibration against FastBlade, University of Edinburgh, partner, or industrial data.

For the broader validation boundary, see `docs/validation_scope.md`.
