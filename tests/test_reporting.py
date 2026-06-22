import pandas as pd

from hydraulic_twin.anomaly_detection import detect_anomalies
from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy
from hydraulic_twin.features import make_features
from hydraulic_twin.reporting import generate_report, recommend_actions
from hydraulic_twin.twin_state import classify_twin_state
from hydraulic_twin.validation import validate_sensor_data


def _classified_synthetic_frame():
    raw = generate_synthetic_data(duration_hours=0.3, sample_seconds=10, random_seed=42)
    validation = validate_sensor_data(raw, max_missing_rate=0.10)
    data = estimate_energy(raw)
    data = make_features(data, rolling_window_samples=12)
    data = detect_anomalies(data, contamination=0.05, random_state=42)
    return classify_twin_state(data), validation


def test_generate_report_writes_markdown_file(tmp_path):
    data, validation = _classified_synthetic_frame()
    recommendations = recommend_actions(data)
    output_path = tmp_path / "synthetic_report.md"

    report = generate_report(
        data,
        validation,
        recommendations,
        output_path=output_path,
    )

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == report
    assert "# Synthetic Hydraulic Digital Twin Report" in report
    assert "## Publication boundary" in report
    assert "## Digital-twin state counts" in report
    assert "## Recommendations" in report


def test_recommend_actions_includes_synthetic_boundary_note():
    data = pd.DataFrame(
        {
            "twin_state": [
                "sensor_issue",
                "pressure_loss_suspected",
                "inefficient_operation",
                "pump_degradation_suspected",
                "load_response_anomaly",
                "transient_response",
            ]
        }
    )

    recommendations = recommend_actions(data)

    assert any("sensor" in item.lower() for item in recommendations)
    assert any("pressure-loss" in item.lower() for item in recommendations)
    assert any("energy-use" in item.lower() for item in recommendations)
    assert any("synthetic decision-support" in item for item in recommendations)
