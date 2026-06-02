from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy


def test_estimate_energy_adds_expected_columns():
    data = generate_synthetic_data(duration_hours=0.2, sample_seconds=5, random_seed=42)
    result = estimate_energy(data)

    for column in [
        "hydraulic_power_kw",
        "efficiency_estimate",
        "cumulative_electrical_energy_kwh",
        "cumulative_hydraulic_energy_kwh",
    ]:
        assert column in result.columns

    assert result["cumulative_electrical_energy_kwh"].iloc[-1] > 0
    assert 0 < result["efficiency_estimate"].median() < 1.2
