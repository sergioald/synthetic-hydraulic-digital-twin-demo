"""Create example figures for the synthetic hydraulic digital-twin demo.

The figures are generated from fully synthetic data. They are intended for
portfolio documentation and are not operational diagnostics.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from hydraulic_twin.cli import run_pipeline

STATE_ORDER = [
    "normal",
    "investigate",
    "inefficient_operation",
    "pump_degradation_suspected",
    "transient_response",
    "load_response_anomaly",
    "pressure_loss_suspected",
    "sensor_issue",
]


def _normalise(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").interpolate(limit_direction="both")
    value_range = values.max() - values.min()
    if value_range == 0:
        return values * 0
    return (values - values.min()) / value_range


def create_anomaly_timeline(df: pd.DataFrame, output_dir: Path) -> Path:
    """Create a digital-twin state timeline figure."""

    state_to_code = {state: index for index, state in enumerate(STATE_ORDER)}
    state_codes = df["twin_state"].map(state_to_code).fillna(-1)

    path = output_dir / "anomaly_timeline.png"
    plt.figure(figsize=(11, 4.5))
    plt.plot(df["timestamp"], state_codes, marker=".", linewidth=0.7, markersize=2)
    plt.yticks(list(state_to_code.values()), STATE_ORDER)
    plt.xlabel("Synthetic timestamp")
    plt.ylabel("Digital-twin state")
    plt.title("Synthetic anomaly and digital-twin state timeline")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def create_energy_efficiency_summary(df: pd.DataFrame, output_dir: Path) -> Path:
    """Create a rolling efficiency summary figure."""

    path = output_dir / "energy_efficiency_summary.png"
    rolling_efficiency = df["efficiency_estimate"].rolling(48, min_periods=4).mean()
    summary_text = (
        "Total electrical energy: "
        f"{df['cumulative_electrical_energy_kwh'].iloc[-1]:.1f} kWh\n"
        "Total hydraulic energy: "
        f"{df['cumulative_hydraulic_energy_kwh'].iloc[-1]:.1f} kWh\n"
        f"Mean efficiency: {df['efficiency_estimate'].mean():.2f}"
    )

    plt.figure(figsize=(11, 4.5))
    plt.plot(df["timestamp"], rolling_efficiency)
    plt.xlabel("Synthetic timestamp")
    plt.ylabel("Rolling efficiency estimate")
    plt.title("Synthetic energy-efficiency estimate over time")
    plt.gcf().text(
        0.68,
        0.18,
        summary_text,
        fontsize=9,
        bbox={"boxstyle": "round", "alpha": 0.15},
    )
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def create_pressure_flow_overview(df: pd.DataFrame, output_dir: Path) -> Path:
    """Create a normalised pressure-flow operating overview figure."""

    path = output_dir / "pressure_flow_overview.png"
    pressure_norm = _normalise(df["high_pressure_bar"])
    flow_norm = _normalise(df["flow_lpm"])

    plt.figure(figsize=(11, 4.5))
    plt.plot(df["timestamp"], pressure_norm, label="High pressure, normalised")
    plt.plot(df["timestamp"], flow_norm, label="Flow, normalised")
    plt.xlabel("Synthetic timestamp")
    plt.ylabel("Normalised sensor value")
    plt.title("Synthetic pressure-flow operating overview")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def create_figures(
    *,
    config_path: str | Path = "configs/default.yaml",
    output_dir: str | Path = "reports/figures",
) -> list[Path]:
    """Run the synthetic workflow and create portfolio figures."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df = run_pipeline(
        config_path=config_path,
        output_path="reports/example_report.md",
        data_output_path=None,
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return [
        create_anomaly_timeline(df, output_path),
        create_energy_efficiency_summary(df, output_path),
        create_pressure_flow_overview(df, output_path),
    ]


def main() -> None:
    """CLI entry point for regenerating example figures."""

    parser = argparse.ArgumentParser(
        description="Create synthetic portfolio figures for the digital-twin demo."
    )
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--output-dir", default="reports/figures")
    args = parser.parse_args()

    paths = create_figures(config_path=args.config, output_dir=args.output_dir)
    for path in paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
