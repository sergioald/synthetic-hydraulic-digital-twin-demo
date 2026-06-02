"""Synthetic hydraulic digital-twin demo package."""

from hydraulic_twin.anomaly_detection import detect_anomalies, detect_rule_based_anomalies
from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy
from hydraulic_twin.features import make_features
from hydraulic_twin.reporting import generate_report, recommend_actions
from hydraulic_twin.twin_state import classify_twin_state
from hydraulic_twin.validation import ValidationResult, validate_sensor_data

__all__ = [
    "ValidationResult",
    "classify_twin_state",
    "detect_anomalies",
    "detect_rule_based_anomalies",
    "estimate_energy",
    "generate_report",
    "generate_synthetic_data",
    "make_features",
    "recommend_actions",
    "validate_sensor_data",
]

__version__ = "0.2.0"
