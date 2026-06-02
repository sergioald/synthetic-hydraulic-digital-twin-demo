from hydraulic_twin.anomaly_detection import detect_anomalies
from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy
from hydraulic_twin.features import make_features
from hydraulic_twin.reporting import generate_report, recommend_actions
from hydraulic_twin.twin_state import classify_twin_state
from hydraulic_twin.validation import validate_sensor_data


def test_classify_twin_state_produces_normal_and_non_normal_states():
    data = generate_synthetic_data(duration_hours=1.0, sample_seconds=10, random_seed=42)
    validation = validate_sensor_data(data, max_missing_rate=0.10)
    data = estimate_energy(data)
    data = make_features(data)
    data = detect_anomalies(data, contamination=0.05, random_state=42)
    result = classify_twin_state(data)

    assert "twin_state" in result.columns
    assert "normal" in set(result["twin_state"])
    assert result["twin_state"].nunique() > 1

    recommendations = recommend_actions(result)
    report = generate_report(result, validation, recommendations)
    assert "Synthetic Hydraulic Digital Twin Report" in report
    assert recommendations
