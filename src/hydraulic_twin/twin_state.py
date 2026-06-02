"""Digital-twin state classification for synthetic hydraulic monitoring data."""

from __future__ import annotations

import numpy as np
import pandas as pd

CRITICAL_SENSOR_COLUMNS = ["high_pressure_bar", "flow_lpm", "motor_power_kw"]


def classify_twin_state(df: pd.DataFrame) -> pd.DataFrame:
    """Classify each row into an explainable synthetic digital-twin state."""

    result = df.copy()
    state = np.full(len(result), "normal", dtype=object)
    reason = np.full(len(result), "within baseline synthetic envelope", dtype=object)

    critical_missing = result[CRITICAL_SENSOR_COLUMNS].isna().any(axis=1).to_numpy()
    pressure_loss = (
        (
            (
                (result.get("pressure_delta_bar", pd.Series(np.inf, index=result.index)) < 60)
                & (result["command_signal_pct"] > 50)
            )
            | (result.get("pressure_command_residual_bar", pd.Series(0, index=result.index)) < -45)
        )
        .fillna(False)
        .to_numpy()
    )
    inefficient = (
        (result.get("efficiency_estimate", pd.Series(1.0, index=result.index)) < 0.48)
        .fillna(False)
        .to_numpy()
    )
    load_mismatch = (
        (result.get("load_command_error_kn", pd.Series(0, index=result.index)).abs() > 220)
        .fillna(False)
        .to_numpy()
    )
    pump_degradation = (
        (
            (result["motor_temperature_c"] > result["motor_temperature_c"].quantile(0.90))
            & (result["vibration_proxy"] > result["vibration_proxy"].quantile(0.90))
            & (result.get("efficiency_estimate", pd.Series(1.0, index=result.index)) < 0.60)
        )
        .fillna(False)
        .to_numpy()
    )
    transient = (
        (result["vibration_proxy"] > result["vibration_proxy"].quantile(0.985))
        .fillna(False)
        .to_numpy()
    )
    investigate = (
        result.get("combined_anomaly", pd.Series(False, index=result.index))
        .fillna(False)
        .to_numpy()
    )

    def assign(mask: np.ndarray, label: str, label_reason: str) -> None:
        state[mask] = label
        reason[mask] = label_reason

    assign(investigate, "investigate", "rule-based or ML anomaly detector flagged the sample")
    assign(inefficient, "inefficient_operation", "estimated efficiency below synthetic threshold")
    assign(
        pump_degradation,
        "pump_degradation_suspected",
        "temperature, vibration and efficiency indicators align",
    )
    assign(
        transient, "transient_response", "short-duration vibration or pressure transient detected"
    )
    assign(
        load_mismatch, "load_response_anomaly", "load demand and command signal are inconsistent"
    )
    assign(
        pressure_loss, "pressure_loss_suspected", "pressure delta is low under moderate/high demand"
    )
    assign(critical_missing, "sensor_issue", "critical sensor value is missing")

    result["twin_state"] = state
    result["twin_state_reason"] = reason
    return result
