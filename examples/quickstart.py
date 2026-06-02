"""Quickstart example for the synthetic hydraulic digital-twin workflow."""

from pathlib import Path

from hydraulic_twin.cli import run_pipeline


if __name__ == "__main__":
    output_path = Path("reports/example_report.md")
    data = run_pipeline(
        config_path="configs/default.yaml",
        output_path=output_path,
        data_output_path=None,
    )
    print(data[["timestamp", "event_label", "combined_anomaly", "twin_state"]].head())
    print(f"\nWrote synthetic report to {output_path}")
