import pytest

from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy
from hydraulic_twin.features import make_features


def test_make_features_adds_expected_columns_and_preserves_rows():
    raw = generate_synthetic_data(duration_hours=0.2, sample_seconds=10, random_seed=42)
    data = estimate_energy(raw)

    result = make_features(data, rolling_window_samples=12)

    expected_columns = [
        "pressure_delta_bar",
        "pressure_command_residual_bar",
        "load_command_error_kn",
        "motor_power_per_flow_kw_per_lpm",
        "high_pressure_bar_rolling_mean",
        "high_pressure_bar_rolling_std",
        "high_pressure_bar_zscore",
        "flow_lpm_rolling_mean",
        "flow_lpm_rolling_std",
        "flow_lpm_zscore",
        "motor_power_kw_rolling_mean",
        "motor_power_kw_rolling_std",
        "motor_power_kw_zscore",
        "motor_temperature_c_rolling_mean",
        "motor_temperature_c_rolling_std",
        "motor_temperature_c_zscore",
        "vibration_proxy_rolling_mean",
        "vibration_proxy_rolling_std",
        "vibration_proxy_zscore",
        "efficiency_rolling_mean",
        "efficiency_drop",
    ]

    assert len(result) == len(data)
    for column in expected_columns:
        assert column in result.columns

    assert result["pressure_delta_bar"].notna().any()
    assert result["motor_power_per_flow_kw_per_lpm"].notna().any()


def test_make_features_rejects_invalid_rolling_window():
    data = generate_synthetic_data(duration_hours=0.1, sample_seconds=10, random_seed=42)

    with pytest.raises(ValueError, match="rolling_window_samples"):
        make_features(data, rolling_window_samples=1)
