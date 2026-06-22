"""Run all synthetic scenario configurations.

This script is intended for portfolio demonstrations and regression checks.
It generates one Markdown report and one CSV file per scenario configuration.

Outputs are written to:

- reports/scenarios/
- data/scenarios/

The generated CSV files are reproducible synthetic outputs and can remain ignored
by Git if the repository ignores generated data.
"""

from __future__ import annotations

from pathlib import Path

from hydraulic_twin.cli import run_pipeline


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    scenario_dir = repo_root / "configs" / "scenarios"
    report_dir = repo_root / "reports" / "scenarios"
    data_dir = repo_root / "data" / "scenarios"

    scenario_paths = sorted(scenario_dir.glob("*.yaml"))
    if not scenario_paths:
        raise FileNotFoundError(f"No scenario YAML files found in {scenario_dir}")

    report_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(scenario_paths)} synthetic scenarios.")

    for scenario_path in scenario_paths:
        scenario_name = scenario_path.stem
        report_path = report_dir / f"{scenario_name}_report.md"
        data_output_path = data_dir / f"{scenario_name}_synthetic_run.csv"

        result = run_pipeline(
            config_path=scenario_path,
            output_path=report_path,
            data_output_path=data_output_path,
        )

        anomaly_count = int(result["combined_anomaly"].sum())
        state_count = int(result["twin_state"].nunique())

        print(
            f"- {scenario_name}: {len(result)} samples, "
            f"{anomaly_count} anomaly samples, {state_count} twin states"
        )

    print(f"\nReports written to: {report_dir}")
    print(f"CSV outputs written to: {data_dir}")


if __name__ == "__main__":
    main()
