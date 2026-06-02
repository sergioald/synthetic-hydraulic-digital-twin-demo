"""Feature engineering for synthetic hydraulic time-series data."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _numeric(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(df[column], errors="coerce").interpolate(limit_direction="both")


def make_features(df: pd.DataFrame, *, rolling_window_samples: int = 24) -> pd.DataFrame:
    """Create simple rolling and physics-inspired features.

    The features are intentionally explainable. They provide baseline signals for
    anomaly detection and state classification without relying on real system data.
    """

    if rolling_window_samples <= 1:
        raise ValueError("rolling_window_samples must be greater than 1")

    result = df.copy()
    window = int(rolling_window_samples)

    command = _numeric(result, "command_signal_pct")
    high_pressure = _numeric(result, "high_pressure_bar")
    result["pressure_delta_bar"] = high_pressure - _numeric(result, "return_pressure_bar")
    result["pressure_command_residual_bar"] = high_pressure - (35 + 2.1 * command)
    result["load_command_error_kn"] = _numeric(result, "load_demand_kn") - 10 * command
    result["motor_power_per_flow_kw_per_lpm"] = _numeric(result, "motor_power_kw") / _numeric(
        result, "flow_lpm"
    ).clip(lower=1)

    for column in [
        "high_pressure_bar",
        "flow_lpm",
        "motor_power_kw",
        "motor_temperature_c",
        "vibration_proxy",
    ]:
        values = _numeric(result, column)
        result[f"{column}_rolling_mean"] = values.rolling(window, min_periods=2).mean()
        result[f"{column}_rolling_std"] = values.rolling(window, min_periods=2).std().fillna(0)
        result[f"{column}_zscore"] = (
            (values - result[f"{column}_rolling_mean"])
            / result[f"{column}_rolling_std"].replace(0, np.nan)
        ).replace([np.inf, -np.inf], np.nan).fillna(0)

    if "efficiency_estimate" in result.columns:
        efficiency = _numeric(result, "efficiency_estimate")
        result["efficiency_rolling_mean"] = efficiency.rolling(window, min_periods=2).mean()
        result["efficiency_drop"] = result["efficiency_rolling_mean"] - efficiency

    return result
