# Synthetic System Abstraction

This project uses a simplified synthetic representation of a hydraulic structural test rig.

The abstraction is inspired by general sensor-heavy hydraulic monitoring workflows, but it is not a representation of any real facility, hydraulic architecture, control system or proprietary setup.

## Public synthetic system

The synthetic system contains:

- hydraulic reservoir
- auxiliary or low-pressure pump
- conditioning stage for filtering and cooling
- variable hydraulic pump or motor unit
- electric motor
- pressure storage element
- structural load interface
- return path
- sensor monitoring layer

The model is intentionally simplified. It is designed to demonstrate data validation, energy modelling, anomaly detection, digital-twin state classification and automated reporting.

## Simplified public architecture

```text
reservoir
→ auxiliary pump
→ conditioning stage
→ hydraulic pump/motor unit
→ pressure storage element
→ structural load interface
→ return path
```

This is a public abstraction only. It must not be interpreted as a real hydraulic diagram or real facility design.

## Synthetic measured variables

The planned synthetic dataset will include variables such as:

| Variable | Description |
|---|---|
| `timestamp` | Simulated measurement time |
| `reservoir_level_pct` | Synthetic reservoir level |
| `low_pressure_bar` | Synthetic low-pressure line pressure |
| `low_pressure_temperature_c` | Synthetic low-pressure oil temperature |
| `flow_lpm` | Synthetic hydraulic flow rate |
| `high_pressure_bar` | Synthetic high-pressure output |
| `return_pressure_bar` | Synthetic return-side pressure |
| `motor_power_kw` | Synthetic electric power drawn |
| `motor_speed_rpm` | Synthetic motor speed |
| `motor_temperature_c` | Synthetic motor temperature |
| `accumulator_pressure_bar` | Synthetic pressure-storage measurement |
| `accumulator_temperature_c` | Synthetic oil temperature near pressure storage |
| `command_signal_pct` | Synthetic control demand signal |
| `load_demand_kn` | Synthetic structural load demand |
| `actuator_displacement_mm` | Synthetic actuator displacement |
| `vibration_proxy` | Synthetic vibration or audio-like proxy |
| `hydraulic_power_kw` | Derived synthetic hydraulic power |
| `efficiency_estimate` | Derived synthetic efficiency estimate |
| `event_label` | Synthetic injected operating condition |

## Synthetic operating states

The initial synthetic events are:

- normal operation
- inefficient operating regime
- sensor drift
- missing data
- pressure loss
- pump degradation
- abnormal energy use
- load anomaly
- transient event

These are generic labels for demonstration. They are not mapped to real events, real failure modes or real operating logs.

## Explicit exclusions

This repository does not include:

- real FastBlade data
- real FastBlade diagrams
- real University of Edinburgh code
- real partner data
- real control logic
- real component parameters
- facility-specific hydraulic layouts
- real nominal operating values
- confidential industrial measurements

All parameters, signals and operating behaviours are illustrative and generated synthetically.
