from hydraulic_twin.anomaly_detection import detect_anomalies
from hydraulic_twin.cli import main, run_pipeline
from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy
from hydraulic_twin.features import make_features
from hydraulic_twin.reporting import generate_html_report, recommend_actions
from hydraulic_twin.twin_state import classify_twin_state
from hydraulic_twin.validation import validate_sensor_data


def _classified_synthetic_frame():
    raw = generate_synthetic_data(duration_hours=0.3, sample_seconds=10, random_seed=42)
    validation = validate_sensor_data(raw, max_missing_rate=0.10)
    data = estimate_energy(raw)
    data = make_features(data, rolling_window_samples=12)
    data = detect_anomalies(data, contamination=0.05, random_state=42)
    return classify_twin_state(data), validation


def _write_small_config(config_path):
    config_path.write_text(
        """
simulation:
  duration_hours: 0.2
  sample_seconds: 10
  random_seed: 42

energy_model:
  standby_power_kw: 2.0

anomaly_detection:
  rolling_window_samples: 12
  isolation_forest_contamination: 0.05
  maximum_missing_rate: 0.10
""".strip(),
        encoding="utf-8",
    )


def test_generate_html_report_writes_html_file(tmp_path):
    data, validation = _classified_synthetic_frame()
    recommendations = recommend_actions(data)
    output_path = tmp_path / "synthetic_report.html"

    html = generate_html_report(
        data,
        validation,
        recommendations,
        output_path=output_path,
    )

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == html
    assert "<!doctype html>" in html
    assert "Synthetic Hydraulic Digital Twin Report" in html
    assert "Publication boundary" in html
    assert "<table>" in html
    assert "Recommendations" in html


def test_run_pipeline_can_create_html_report(tmp_path):
    config_path = tmp_path / "small_config.yaml"
    report_path = tmp_path / "reports" / "example_report.md"
    html_output_path = tmp_path / "reports" / "example_report.html"
    data_output_path = tmp_path / "data" / "synthetic_run.csv"
    _write_small_config(config_path)

    result = run_pipeline(
        config_path=config_path,
        output_path=report_path,
        html_output_path=html_output_path,
        data_output_path=data_output_path,
    )

    assert len(result) > 0
    assert report_path.exists()
    assert html_output_path.exists()
    assert data_output_path.exists()
    assert "Synthetic Hydraulic Digital Twin Report" in html_output_path.read_text(encoding="utf-8")


def test_cli_can_write_html_report(tmp_path, capsys):
    config_path = tmp_path / "small_config.yaml"
    report_path = tmp_path / "reports" / "example_report.md"
    html_output_path = tmp_path / "reports" / "example_report.html"
    _write_small_config(config_path)

    main(
        [
            "run",
            "--config",
            str(config_path),
            "--output",
            str(report_path),
            "--html-output",
            str(html_output_path),
        ]
    )

    captured = capsys.readouterr()

    assert "Generated" in captured.out
    assert "HTML report" in captured.out
    assert report_path.exists()
    assert html_output_path.exists()
