"""Hydraulic and electrical energy estimates for synthetic time-series data."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _infer_sample_period_seconds(df: pd.DataFrame, default: float = 5.0) -> float:
    if "timestamp" not in df.columns or len(df) < 2:
        return default
    timestamps = pd.to_datetime(df["timestamp"], errors="coerce")
    deltas = timestamps.diff().dt.total_seconds().dropna()
    if deltas.empty:
        return default
    return float(deltas.median())


def _interpolate_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").interpolate(limit_direction="both")


def estimate_energy(
    df: pd.DataFrame,
    *,
    sample_period_seconds: float | None = None,
    standby_power_kw: float = 2.0,
) -> pd.DataFrame:
    """Add hydraulic power, efficiency and cumulative energy estimates.

    Hydraulic power is estimated with the common engineering approximation:

    ``hydraulic_power_kw = pressure_bar * flow_lpm / 600``

    This is an illustrative synthetic calculation, not a calibrated facility model.
    """

    result = df.copy()
    sample_period_seconds = sample_period_seconds or _infer_sample_period_seconds(result)
    dt_hours = sample_period_seconds / 3600

    high_pressure = _interpolate_numeric(result["high_pressure_bar"])
    flow = _interpolate_numeric(result["flow_lpm"])
    motor_power = _interpolate_numeric(result["motor_power_kw"]).clip(lower=0)

    result["hydraulic_power_kw"] = (high_pressure * flow / 600).clip(lower=0)
    result["net_motor_power_kw"] = (motor_power - standby_power_kw).clip(lower=0.001)
    result["efficiency_estimate"] = (
        result["hydraulic_power_kw"] / result["net_motor_power_kw"]
    ).replace([np.inf, -np.inf], np.nan)
    result["efficiency_estimate"] = result["efficiency_estimate"].clip(lower=0, upper=1.2)

    result["electrical_energy_kwh"] = motor_power * dt_hours
    result["hydraulic_energy_kwh"] = result["hydraulic_power_kw"] * dt_hours
    result["cumulative_electrical_energy_kwh"] = result["electrical_energy_kwh"].cumsum()
    result["cumulative_hydraulic_energy_kwh"] = result["hydraulic_energy_kwh"].cumsum()

    load = _interpolate_numeric(result["load_demand_kn"]).clip(lower=1)
    result["energy_intensity_kw_per_kn"] = motor_power / load
    return result
