"""Validation utilities for synthetic hydraulic sensor data."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from hydraulic_twin.data_generation import RAW_SENSOR_COLUMNS

REQUIRED_COLUMNS = tuple(RAW_SENSOR_COLUMNS)
NUMERIC_RANGE_CHECKS = {
    "reservoir_level_pct": (0, 100),
    "low_pressure_bar": (0, 60),
    "low_pressure_temperature_c": (-10, 120),
    "flow_lpm": (0, 250),
    "high_pressure_bar": (0, 350),
    "return_pressure_bar": (0, 80),
    "motor_power_kw": (0, 250),
    "motor_speed_rpm": (0, 2500),
    "motor_temperature_c": (-10, 130),
    "accumulator_pressure_bar": (0, 350),
    "accumulator_temperature_c": (-10, 130),
    "command_signal_pct": (0, 100),
    "load_demand_kn": (-50, 1500),
    "actuator_displacement_mm": (-150, 150),
    "vibration_proxy": (0, 20),
}


@dataclass(frozen=True)
class ValidationResult:
    """Container for validation errors, warnings and summary metrics."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summary: dict[str, float | int | str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """Return True when no blocking validation errors were found."""

        return not self.errors

    def raise_for_errors(self) -> None:
        """Raise ValueError if blocking validation errors are present."""

        if self.errors:
            raise ValueError("; ".join(self.errors))


def validate_sensor_data(df: pd.DataFrame, *, max_missing_rate: float = 0.05) -> ValidationResult:
    """Validate required columns, timestamps, missingness and simple physical ranges."""

    errors: list[str] = []
    warnings: list[str] = []

    if df.empty:
        errors.append("dataframe is empty")
        return ValidationResult(errors=errors, warnings=warnings, summary={"rows": 0})

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        errors.append(f"missing required columns: {missing_columns}")

    summary: dict[str, float | int | str] = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
    }

    if "timestamp" in df.columns:
        timestamps = pd.to_datetime(df["timestamp"], errors="coerce")
        invalid_timestamps = int(timestamps.isna().sum())
        summary["invalid_timestamps"] = invalid_timestamps
        if invalid_timestamps:
            errors.append(f"invalid timestamps found: {invalid_timestamps}")
        if timestamps.duplicated().any():
            errors.append("duplicate timestamps found")
        if not timestamps.is_monotonic_increasing:
            errors.append("timestamps are not monotonic increasing")

    available_required = [column for column in REQUIRED_COLUMNS if column in df.columns]
    if available_required:
        missing_rate = float(df[available_required].isna().mean().max())
        summary["max_column_missing_rate"] = missing_rate
        if missing_rate > max_missing_rate:
            warnings.append(
                f"maximum column missing rate {missing_rate:.3f} exceeds configured "
                f"threshold {max_missing_rate:.3f}"
            )

    for column, (low, high) in NUMERIC_RANGE_CHECKS.items():
        if column not in df.columns:
            continue
        values = pd.to_numeric(df[column], errors="coerce")
        below = int((values < low).sum())
        above = int((values > high).sum())
        if below or above:
            warnings.append(
                f"{column} has {below} values below {low} and {above} values above {high}"
            )

    return ValidationResult(errors=errors, warnings=warnings, summary=summary)
