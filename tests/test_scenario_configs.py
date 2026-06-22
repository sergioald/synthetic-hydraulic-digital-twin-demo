from pathlib import Path

import pytest

from hydraulic_twin.cli import run_pipeline

SCENARIO_DIR = Path("configs/scenarios")


@pytest.mark.parametrize("config_path", sorted(SCENARIO_DIR.glob("*.yaml")))
def test_scenario_config_runs_end_to_end(config_path, tmp_path):
    report_path = tmp_path / f"{config_path.stem}_report.md"
    data_output_path = tmp_path / f"{config_path.stem}_synthetic_run.csv"

    result = run_pipeline(
        config_path=config_path,
        output_path=report_path,
        data_output_path=data_output_path,
    )

    assert len(result) > 0
    assert "event_label" in result.columns
    assert "combined_anomaly" in result.columns
    assert "twin_state" in result.columns
    assert "twin_state_reason" in result.columns
    assert report_path.exists()
    assert data_output_path.exists()


def test_scenario_directory_contains_expected_configs():
    scenario_names = {path.name for path in SCENARIO_DIR.glob("*.yaml")}

    expected = {
        "normal.yaml",
        "pressure_loss.yaml",
        "sensor_drift.yaml",
        "missing_data.yaml",
        "pump_degradation.yaml",
        "abnormal_energy.yaml",
        "load_anomaly.yaml",
        "transient_event.yaml",
        "mixed_faults.yaml",
    }

    assert expected.issubset(scenario_names)
