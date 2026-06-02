"""Baseline anomaly detection for synthetic hydraulic time-series data."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

CRITICAL_SENSOR_COLUMNS = ["high_pressure_bar", "flow_lpm", "motor_power_kw"]


def detect_rule_based_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Apply transparent baseline rules for hydraulic monitoring anomalies."""

    result = df.copy()
    reasons: list[list[str]] = [[] for _ in range(len(result))]

    critical_missing = result[CRITICAL_SENSOR_COLUMNS].isna().any(axis=1)
    low_pressure_delta = (
        (result.get("pressure_delta_bar", np.inf) < 60) & (result["command_signal_pct"] > 50)
    ) | (result.get("pressure_command_residual_bar", 0) < -45)
    inefficient = result.get("efficiency_estimate", 1.0) < 0.48
    high_temperature = result["motor_temperature_c"] > 80
    high_energy = (
        result["motor_power_kw"]
        > result["motor_power_kw"].rolling(48, min_periods=4).median() * 1.35
    )
    load_mismatch = result.get("load_command_error_kn", 0).abs() > 220
    vibration_spike = result["vibration_proxy"] > result["vibration_proxy"].quantile(0.98)

    rule_map = {
        "critical_sensor_missing": critical_missing.fillna(False),
        "low_pressure_delta": low_pressure_delta.fillna(False),
        "low_efficiency": inefficient.fillna(False),
        "high_temperature": high_temperature.fillna(False),
        "abnormal_energy_use": high_energy.fillna(False),
        "load_response_mismatch": load_mismatch.fillna(False),
        "vibration_spike": vibration_spike.fillna(False),
    }

    for reason, mask in rule_map.items():
        for position in np.flatnonzero(mask.to_numpy()):
            reasons[position].append(reason)

    result["rule_anomaly"] = [bool(row_reasons) for row_reasons in reasons]
    result["anomaly_reason"] = [
        ";".join(row_reasons) if row_reasons else "" for row_reasons in reasons
    ]
    return result


def detect_anomalies(
    df: pd.DataFrame,
    *,
    contamination: float = 0.04,
    random_state: int = 42,
) -> pd.DataFrame:
    """Add rule-based and Isolation Forest anomaly indicators."""

    if not 0 < contamination < 0.5:
        raise ValueError("contamination must be between 0 and 0.5")

    result = detect_rule_based_anomalies(df)
    numeric_columns = [
        column
        for column in result.select_dtypes(include=["number", "bool"]).columns
        if column not in {"rule_anomaly", "ml_anomaly"}
    ]

    if len(result) < 20 or not numeric_columns:
        result["ml_anomaly"] = False
        result["ml_anomaly_score"] = 0.0
        result["combined_anomaly"] = result["rule_anomaly"]
        return result

    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        IsolationForest(contamination=contamination, random_state=random_state),
    )
    predictions = model.fit_predict(result[numeric_columns])
    scores = model.named_steps["isolationforest"].decision_function(
        model[:-1].transform(result[numeric_columns])
    )

    result["ml_anomaly"] = predictions == -1
    result["ml_anomaly_score"] = -scores
    result["combined_anomaly"] = result["rule_anomaly"] | result["ml_anomaly"]
    return result
