"""Command-line interface for the synthetic hydraulic digital-twin workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from hydraulic_twin.anomaly_detection import detect_anomalies
from hydraulic_twin.data_generation import generate_synthetic_data
from hydraulic_twin.energy_model import estimate_energy
from hydraulic_twin.features import make_features
from hydraulic_twin.reporting import generate_html_report, generate_report, recommend_actions
from hydraulic_twin.twin_state import classify_twin_state
from hydraulic_twin.validation import validate_sensor_data


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file."""

    with Path(path).open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    if not isinstance(config, dict):
        raise ValueError("configuration file must contain a YAML mapping")
    return config


def run_pipeline(
    *,
    config_path: str | Path = "configs/default.yaml",
    output_path: str | Path = "reports/example_report.md",
    data_output_path: str | Path | None = None,
    html_output_path: str | Path | None = None,
) -> pd.DataFrame:
    """Run the complete synthetic digital-twin workflow."""

    config = load_config(config_path)
    anomaly_config = config.get("anomaly_detection", {})
    energy_config = config.get("energy_model", {})

    raw = generate_synthetic_data(config)
    validation_result = validate_sensor_data(
        raw,
        max_missing_rate=float(anomaly_config.get("maximum_missing_rate", 0.05)),
    )

    with_energy = estimate_energy(
        raw,
        standby_power_kw=float(energy_config.get("standby_power_kw", 2.0)),
    )
    with_features = make_features(
        with_energy,
        rolling_window_samples=int(anomaly_config.get("rolling_window_samples", 24)),
    )
    with_anomalies = detect_anomalies(
        with_features,
        contamination=float(anomaly_config.get("isolation_forest_contamination", 0.04)),
        random_state=int(config.get("simulation", {}).get("random_seed", 42)),
    )
    classified = classify_twin_state(with_anomalies)
    recommendations = recommend_actions(classified)
    generate_report(classified, validation_result, recommendations, output_path=output_path)

    if html_output_path is not None:
        generate_html_report(
            classified,
            validation_result,
            recommendations,
            output_path=html_output_path,
        )

    if data_output_path is not None:
        path = Path(data_output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        classified.to_csv(path, index=False)

    return classified


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description="Run a synthetic hydraulic digital-twin monitoring workflow."
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="run the synthetic pipeline")
    run_parser.add_argument("--config", default="configs/default.yaml", help="path to YAML config")
    run_parser.add_argument(
        "--output", default="reports/example_report.md", help="path for markdown report"
    )
    run_parser.add_argument(
        "--html-output", default=None, help="optional path for generated HTML report"
    )
    run_parser.add_argument(
        "--data-output", default=None, help="optional path for generated synthetic CSV output"
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {None, "run"}:
        data = run_pipeline(
            config_path=args.config,
            output_path=args.output,
            data_output_path=args.data_output,
            html_output_path=args.html_output,
        )
        anomaly_count = int(data["combined_anomaly"].sum())
        report_targets = f"report to {args.output}"
        if args.html_output is not None:
            report_targets += f" and HTML report to {args.html_output}"
        print(
            f"Generated {len(data)} synthetic samples, flagged {anomaly_count} anomalies, "
            f"and wrote {report_targets}."
        )
        return

    parser.error(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
