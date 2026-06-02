import pandas as pd

from hydraulic_twin.data_generation import RAW_SENSOR_COLUMNS, generate_synthetic_data


def test_generate_synthetic_data_has_expected_columns_and_rows():
    data = generate_synthetic_data(duration_hours=0.1, sample_seconds=5, random_seed=7)

    assert list(data.columns) == RAW_SENSOR_COLUMNS
    assert len(data) >= 20
    assert pd.api.types.is_datetime64_any_dtype(data["timestamp"])


def test_generate_synthetic_data_is_reproducible_for_seed():
    first = generate_synthetic_data(duration_hours=0.1, sample_seconds=5, random_seed=123)
    second = generate_synthetic_data(duration_hours=0.1, sample_seconds=5, random_seed=123)

    pd.testing.assert_frame_equal(first, second)


def test_generate_synthetic_data_contains_synthetic_event_labels():
    data = generate_synthetic_data(duration_hours=1.0, sample_seconds=10, random_seed=42)

    assert "normal" in set(data["event_label"])
    assert data["event_label"].nunique() > 3
