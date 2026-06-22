from hydraulic_twin.cli import main


def test_cli_smoke_run_creates_outputs(tmp_path, capsys):
    config_path = tmp_path / "smoke_config.yaml"
    report_path = tmp_path / "smoke_report.md"
    data_output_path = tmp_path / "smoke_data.csv"

    config_path.write_text(
        """
simulation:
  duration_hours: 0.2
  sample_seconds: 10
  random_seed: 7

energy_model:
  standby_power_kw: 2.0

anomaly_detection:
  rolling_window_samples: 12
  isolation_forest_contamination: 0.05
  maximum_missing_rate: 0.10
""".strip(),
        encoding="utf-8",
    )

    main(
        [
            "run",
            "--config",
            str(config_path),
            "--output",
            str(report_path),
            "--data-output",
            str(data_output_path),
        ]
    )

    captured = capsys.readouterr()

    assert "Generated" in captured.out
    assert "flagged" in captured.out
    assert report_path.exists()
    assert data_output_path.exists()
