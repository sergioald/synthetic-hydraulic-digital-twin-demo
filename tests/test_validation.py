from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.validation import validate_sensor_data


def test_validate_generated_data_has_no_errors():
    data = generate_synthetic_data(duration_hours=0.2, sample_seconds=5, random_seed=42)
    result = validate_sensor_data(data, max_missing_rate=0.10)

    assert result.ok
    assert result.summary["rows"] == len(data)


def test_validate_missing_required_column_is_error():
    data = generate_synthetic_data(duration_hours=0.1, sample_seconds=5, random_seed=42)
    data = data.drop(columns=["flow_lpm"])

    result = validate_sensor_data(data)

    assert not result.ok
    assert any("missing required columns" in error for error in result.errors)
