"""Synthetic data generation for a generic hydraulic monitoring workflow.

All values produced by this module are illustrative and synthetic. They are not
calibrated to any real facility, rig, component, controller or sensor export.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd

DEFAULT_EVENTS = (
    "normal",
    "inefficient_regime",
    "sensor_drift",
    "missing_data",
    "pressure_loss",
    "pump_degradation",
    "abnormal_energy",
    "load_anomaly",
    "transient_event",
)

RAW_SENSOR_COLUMNS = [
    "timestamp",
    "reservoir_level_pct",
    "low_pressure_bar",
    "low_pressure_temperature_c",
    "flow_lpm",
    "high_pressure_bar",
    "return_pressure_bar",
    "motor_power_kw",
    "motor_speed_rpm",
    "motor_temperature_c",
    "accumulator_pressure_bar",
    "accumulator_temperature_c",
    "command_signal_pct",
    "load_demand_kn",
    "actuator_displacement_mm",
    "vibration_proxy",
    "event_label",
]


def _read_config_value(
    config: Mapping[str, Any] | None, section: str, key: str, default: Any
) -> Any:
    if not config:
        return default
    return config.get(section, {}).get(key, default)


def _segment(n_samples: int, start_fraction: float, end_fraction: float) -> slice:
    start = max(0, min(n_samples, int(n_samples * start_fraction)))
    end = max(start + 1, min(n_samples, int(n_samples * end_fraction)))
    return slice(start, end)


def generate_synthetic_data(
    config: Mapping[str, Any] | None = None,
    *,
    duration_hours: float | None = None,
    sample_seconds: int | None = None,
    random_seed: int | None = None,
    start_time: str = "2026-01-01 08:00:00",
) -> pd.DataFrame:
    """Generate synthetic sensor data for a generic hydraulic system.

    Parameters are intentionally generic and should not be interpreted as real
    operating values. Event labels are included only as synthetic ground truth
    for examples and tests; the anomaly detector does not use them.
    """

    duration_hours = float(
        duration_hours
        if duration_hours is not None
        else _read_config_value(config, "simulation", "duration_hours", 6)
    )
    sample_seconds = int(
        sample_seconds
        if sample_seconds is not None
        else _read_config_value(config, "simulation", "sample_seconds", 5)
    )
    random_seed = int(
        random_seed
        if random_seed is not None
        else _read_config_value(config, "simulation", "random_seed", 42)
    )

    if duration_hours <= 0:
        raise ValueError("duration_hours must be positive")
    if sample_seconds <= 0:
        raise ValueError("sample_seconds must be positive")

    n_samples = max(20, int(duration_hours * 3600 / sample_seconds))
    rng = np.random.default_rng(random_seed)
    t = np.arange(n_samples)
    seconds = t * sample_seconds
    hours = seconds / 3600

    timestamps = pd.date_range(start=start_time, periods=n_samples, freq=f"{sample_seconds}s")

    demand_cycle = (
        0.60 * np.sin(2 * np.pi * hours / 0.80)
        + 0.25 * np.sin(2 * np.pi * hours / 0.23)
        + 0.15 * np.sin(2 * np.pi * hours / 1.75)
    )
    command_signal_pct = np.clip(52 + 34 * demand_cycle + rng.normal(0, 4, n_samples), 0, 100)
    demand_fraction = command_signal_pct / 100

    high_pressure_bar = np.clip(35 + 210 * demand_fraction + rng.normal(0, 6, n_samples), 15, 280)
    return_pressure_bar = np.clip(7 + 12 * demand_fraction + rng.normal(0, 1.2, n_samples), 2, 35)
    low_pressure_bar = np.clip(8 + 8 * demand_fraction + rng.normal(0, 0.8, n_samples), 4, 30)
    flow_lpm = np.clip(6 + 115 * np.sqrt(demand_fraction) + rng.normal(0, 3, n_samples), 2, 140)

    reservoir_level_pct = np.clip(
        88 - 3.0 * hours / max(duration_hours, 1) + rng.normal(0, 0.2, n_samples), 55, 95
    )
    motor_speed_rpm = np.clip(
        620 + 1180 * demand_fraction + rng.normal(0, 35, n_samples), 500, 1900
    )

    hydraulic_power_kw = high_pressure_bar * flow_lpm / 600
    efficiency = np.clip(
        0.72 - 0.08 * demand_fraction + rng.normal(0, 0.015, n_samples), 0.45, 0.86
    )
    standby_power_kw = float(_read_config_value(config, "energy_model", "standby_power_kw", 2.0))
    motor_power_kw = (
        hydraulic_power_kw / efficiency + standby_power_kw + rng.normal(0, 0.8, n_samples)
    )
    motor_power_kw = np.clip(motor_power_kw, 0.1, None)

    low_pressure_temperature_c = np.clip(
        24 + 0.6 * hours + 0.03 * flow_lpm + rng.normal(0, 0.5, n_samples), 18, 75
    )
    motor_temperature_c = np.clip(
        28 + 0.7 * hours + 0.18 * motor_power_kw + rng.normal(0, 0.7, n_samples), 20, 90
    )
    accumulator_pressure_bar = np.clip(
        pd.Series(high_pressure_bar).rolling(12, min_periods=1).mean().to_numpy()
        * rng.normal(0.92, 0.015, n_samples),
        10,
        260,
    )
    accumulator_temperature_c = np.clip(
        low_pressure_temperature_c + 0.06 * hydraulic_power_kw + rng.normal(0, 0.4, n_samples),
        18,
        85,
    )
    load_demand_kn = np.clip(35 + 930 * demand_fraction + rng.normal(0, 22, n_samples), 0, 1100)
    actuator_displacement_mm = np.clip(
        48 * np.sin(2 * np.pi * hours / 0.80) + rng.normal(0, 1.5, n_samples), -60, 60
    )
    vibration_proxy = np.clip(
        0.10
        + 0.0022 * motor_speed_rpm
        + 0.018 * hydraulic_power_kw
        + rng.normal(0, 0.08, n_samples),
        0,
        None,
    )

    event_label = np.full(n_samples, "normal", dtype=object)
    requested_events = tuple(_read_config_value(config, "events", "include", DEFAULT_EVENTS))

    if "inefficient_regime" in requested_events:
        idx = _segment(n_samples, 0.18, 0.28)
        motor_power_kw[idx] *= 1.22
        motor_temperature_c[idx] += 4
        event_label[idx] = "inefficient_regime"

    if "sensor_drift" in requested_events:
        idx = _segment(n_samples, 0.34, 0.43)
        drift = np.linspace(0, 24, idx.stop - idx.start)
        high_pressure_bar[idx] += drift
        accumulator_pressure_bar[idx] += 0.4 * drift
        event_label[idx] = "sensor_drift"

    if "missing_data" in requested_events:
        idx = _segment(n_samples, 0.48, 0.505)
        mask = rng.random(idx.stop - idx.start) < 0.70
        local = np.arange(idx.start, idx.stop)[mask]
        flow_lpm[local] = np.nan
        high_pressure_bar[local] = np.nan
        event_label[idx] = "missing_data"

    if "pressure_loss" in requested_events:
        idx = _segment(n_samples, 0.58, 0.66)
        high_pressure_bar[idx] *= 0.68
        flow_lpm[idx] *= 1.08
        return_pressure_bar[idx] += 8
        motor_power_kw[idx] *= 1.08
        event_label[idx] = "pressure_loss"

    if "pump_degradation" in requested_events:
        idx = _segment(n_samples, 0.70, 0.82)
        degradation = np.linspace(1.03, 1.32, idx.stop - idx.start)
        motor_power_kw[idx] *= degradation
        motor_temperature_c[idx] += np.linspace(2, 9, idx.stop - idx.start)
        vibration_proxy[idx] += np.linspace(0.2, 1.2, idx.stop - idx.start)
        event_label[idx] = "pump_degradation"

    if "abnormal_energy" in requested_events:
        idx = _segment(n_samples, 0.86, 0.895)
        motor_power_kw[idx] *= 1.45
        motor_temperature_c[idx] += 5
        event_label[idx] = "abnormal_energy"

    if "load_anomaly" in requested_events:
        idx = _segment(n_samples, 0.91, 0.94)
        load_demand_kn[idx] += 260
        actuator_displacement_mm[idx] -= 12
        vibration_proxy[idx] += 0.8
        event_label[idx] = "load_anomaly"

    if "transient_event" in requested_events:
        idx = _segment(n_samples, 0.955, 0.972)
        local_t = np.arange(idx.stop - idx.start)
        oscillation = np.sin(2 * np.pi * local_t / 5)
        high_pressure_bar[idx] += 18 * oscillation
        vibration_proxy[idx] += 1.4 * np.abs(oscillation)
        event_label[idx] = "transient_event"

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "reservoir_level_pct": reservoir_level_pct,
            "low_pressure_bar": low_pressure_bar,
            "low_pressure_temperature_c": low_pressure_temperature_c,
            "flow_lpm": flow_lpm,
            "high_pressure_bar": high_pressure_bar,
            "return_pressure_bar": return_pressure_bar,
            "motor_power_kw": motor_power_kw,
            "motor_speed_rpm": motor_speed_rpm,
            "motor_temperature_c": motor_temperature_c,
            "accumulator_pressure_bar": accumulator_pressure_bar,
            "accumulator_temperature_c": accumulator_temperature_c,
            "command_signal_pct": command_signal_pct,
            "load_demand_kn": load_demand_kn,
            "actuator_displacement_mm": actuator_displacement_mm,
            "vibration_proxy": vibration_proxy,
            "event_label": event_label,
        }
    )
    return df[RAW_SENSOR_COLUMNS]
