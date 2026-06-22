from hydraulic_twin.cli import run_pipeline


def test_run_pipeline_creates_report_and_data_outputs(tmp_path):
    config_path = tmp_path / "small_config.yaml"
    report_path = tmp_path / "reports" / "example_report.md"
    data_output_path = tmp_path / "data" / "synthetic_run.csv"

    config_path.write_text(
        """
simulation:
  duration_hours: 0.3
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

    result = run_pipeline(
        config_path=config_path,
        output_path=report_path,
        data_output_path=data_output_path,
    )

    assert len(result) > 0
    assert "combined_anomaly" in result.columns
    assert "twin_state" in result.columns
    assert "twin_state_reason" in result.columns

    assert report_path.exists()
    assert data_output_path.exists()
    assert "Synthetic Hydraulic Digital Twin Report" in report_path.read_text(encoding="utf-8")
