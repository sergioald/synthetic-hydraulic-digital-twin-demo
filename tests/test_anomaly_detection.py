from hydraulic_twin.anomaly_detection import detect_anomalies
from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy
from hydraulic_twin.features import make_features


def test_detect_anomalies_adds_rule_and_ml_columns():
    data = generate_synthetic_data(duration_hours=1.0, sample_seconds=10, random_seed=42)
    data = estimate_energy(data)
    data = make_features(data)
    result = detect_anomalies(data, contamination=0.05, random_state=42)

    assert "rule_anomaly" in result.columns
    assert "ml_anomaly" in result.columns
    assert "combined_anomaly" in result.columns
    assert result["combined_anomaly"].sum() > 0
