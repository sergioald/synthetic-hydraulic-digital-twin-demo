"""Recommendation and report generation for the synthetic digital-twin workflow."""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd

from hydraulic_twin.validation import ValidationResult


def recommend_actions(df: pd.DataFrame) -> list[str]:
    """Generate simple engineering-style recommendations from synthetic states."""

    recommendations: list[str] = []
    state_counts = df.get("twin_state", pd.Series(dtype=str)).value_counts()

    if state_counts.get("sensor_issue", 0) > 0:
        recommendations.append(
            "Review critical pressure and flow sensor channels before interpreting downstream metrics."
        )
    if state_counts.get("pressure_loss_suspected", 0) > 0:
        recommendations.append(
            "Inspect synthetic pressure-loss periods and compare pressure delta against command demand."
        )
    if state_counts.get("inefficient_operation", 0) > 0:
        recommendations.append(
            "Investigate high energy-use periods and check whether operating demand could be redistributed."
        )
    if state_counts.get("pump_degradation_suspected", 0) > 0:
        recommendations.append(
            "Prioritise maintenance-style review where temperature, vibration and efficiency degrade together."
        )
    if state_counts.get("load_response_anomaly", 0) > 0:
        recommendations.append(
            "Review command/load response consistency during high mismatch periods."
        )
    if state_counts.get("transient_response", 0) > 0:
        recommendations.append(
            "Inspect short transient events and compare them with operating demand changes."
        )

    if not recommendations:
        recommendations.append(
            "No major synthetic operating-state concerns were detected in this run."
        )

    recommendations.append(
        "Treat all recommendations as synthetic decision-support outputs, not operational instructions."
    )
    return recommendations


def _last_numeric_value(df: pd.DataFrame, column: str, *, default: float = 0.0) -> float:
    if column not in df or df[column].empty:
        return default
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if values.empty:
        return default
    return float(values.iloc[-1])


def _mean_numeric_value(df: pd.DataFrame, column: str) -> float:
    if column not in df or df[column].empty:
        return float("nan")
    return float(pd.to_numeric(df[column], errors="coerce").mean())


def _count_true(df: pd.DataFrame, column: str) -> int:
    if column not in df:
        return 0
    return int(df[column].fillna(False).astype(bool).sum())


def _format_float(value: float, *, digits: int) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value:.{digits}f}"


def _summary_rows(df: pd.DataFrame, validation_result: ValidationResult) -> list[tuple[str, str]]:
    validation_status = "PASS" if validation_result.ok else "FAIL"
    total_energy = _last_numeric_value(df, "cumulative_electrical_energy_kwh")
    hydraulic_energy = _last_numeric_value(df, "cumulative_hydraulic_energy_kwh")
    mean_efficiency = _mean_numeric_value(df, "efficiency_estimate")
    anomaly_count = _count_true(df, "combined_anomaly")

    return [
        ("Samples", str(len(df))),
        ("Validation status", validation_status),
        ("Combined anomaly samples", str(anomaly_count)),
        ("Total electrical energy estimate [kWh]", _format_float(total_energy, digits=2)),
        ("Total hydraulic energy estimate [kWh]", _format_float(hydraulic_energy, digits=2)),
        ("Mean efficiency estimate", _format_float(mean_efficiency, digits=3)),
    ]


def _markdown_table(series: pd.Series, *, empty_message: str = "No entries") -> str:
    if series.empty:
        return empty_message
    lines = ["| Item | Count |", "|---|---:|"]
    for item, count in series.items():
        lines.append(f"| {item} | {int(count)} |")
    return "\n".join(lines)


def _html_table_from_rows(rows: list[tuple[str, str]]) -> str:
    lines = ["<table>", "<thead><tr><th>Metric</th><th>Value</th></tr></thead>", "<tbody>"]
    for metric, value in rows:
        lines.append(f'<tr><th scope="row">{escape(metric)}</th><td>{escape(value)}</td></tr>')
    lines.append("</tbody></table>")
    return "\n".join(lines)


def _html_table_from_series(series: pd.Series, *, empty_message: str = "No entries") -> str:
    if series.empty:
        return f"<p>{escape(empty_message)}</p>"

    lines = ["<table>", "<thead><tr><th>Item</th><th>Count</th></tr></thead>", "<tbody>"]
    for item, count in series.items():
        lines.append(f'<tr><th scope="row">{escape(str(item))}</th><td>{int(count)}</td></tr>')
    lines.append("</tbody></table>")
    return "\n".join(lines)


def _html_list(items: list[str]) -> str:
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


def generate_report(
    df: pd.DataFrame,
    validation_result: ValidationResult,
    recommendations: list[str] | None = None,
    *,
    output_path: str | Path | None = None,
) -> str:
    """Generate a markdown report for the synthetic digital-twin pipeline."""

    recommendations = recommendations or recommend_actions(df)
    summary_rows = _summary_rows(df, validation_result)
    state_counts = df.get("twin_state", pd.Series(dtype=str)).value_counts()
    event_counts = df.get("event_label", pd.Series(dtype=str)).value_counts()

    warnings = validation_result.warnings or ["No validation warnings"]
    errors = validation_result.errors or ["No validation errors"]

    summary_table = "\n".join(
        ["| Metric | Value |", "|---|---:|"]
        + [f"| {metric} | {value} |" for metric, value in summary_rows]
    )

    report = f"""# Synthetic Hydraulic Digital Twin Report

## Publication boundary

This report is generated from fully synthetic data. It does not contain real FastBlade data, University of Edinburgh code, partner data, proprietary control logic, real facility diagrams or real operating parameters.

## Run summary

{summary_table}

## Digital-twin state counts

{_markdown_table(state_counts)}

## Synthetic event-label counts

These labels are generated by the synthetic data generator for demonstration and testing. They are not used as real operational truth.

{_markdown_table(event_counts)}

## Validation messages

### Errors

{chr(10).join(f"- {message}" for message in errors)}

### Warnings

{chr(10).join(f"- {message}" for message in warnings)}

## Recommendations

{chr(10).join(f"- {item}" for item in recommendations)}

## Notes

The current model is a baseline demonstration. It prioritises explainability, reproducibility and safe publication over hydraulic realism. Future work could add richer simulation scenarios, calibration-free uncertainty estimates, visual diagnostics and more detailed model-validation notes.
"""

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")

    return report


def generate_html_report(
    df: pd.DataFrame,
    validation_result: ValidationResult,
    recommendations: list[str] | None = None,
    *,
    output_path: str | Path | None = None,
) -> str:
    """Generate a self-contained HTML report for the synthetic digital-twin pipeline."""

    recommendations = recommendations or recommend_actions(df)
    summary_rows = _summary_rows(df, validation_result)
    state_counts = df.get("twin_state", pd.Series(dtype=str)).value_counts()
    event_counts = df.get("event_label", pd.Series(dtype=str)).value_counts()
    warnings = validation_result.warnings or ["No validation warnings"]
    errors = validation_result.errors or ["No validation errors"]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Synthetic Hydraulic Digital Twin Report</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.55;
      margin: 2rem auto;
      max-width: 980px;
      padding: 0 1rem;
      color: #1f2933;
      background: #ffffff;
    }}
    header {{
      border-bottom: 2px solid #1f2933;
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
    }}
    h1, h2, h3 {{
      line-height: 1.25;
    }}
    table {{
      border-collapse: collapse;
      margin: 1rem 0 1.5rem;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #cbd5e1;
      padding: 0.55rem 0.7rem;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f1f5f9;
    }}
    .notice {{
      background: #fff7ed;
      border: 1px solid #fed7aa;
      border-radius: 0.5rem;
      padding: 1rem;
    }}
    .muted {{
      color: #52606d;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Synthetic Hydraulic Digital Twin Report</h1>
    <p class="muted">
      Generated from a fully synthetic applied-AI workflow for hydraulic sensor data.
    </p>
  </header>

  <section class="notice">
    <h2>Publication boundary</h2>
    <p>
      This report is generated from fully synthetic data. It does not contain real
      FastBlade data, University of Edinburgh code, partner data, proprietary control
      logic, real facility diagrams or real operating parameters.
    </p>
  </section>

  <section>
    <h2>Run summary</h2>
    {_html_table_from_rows(summary_rows)}
  </section>

  <section>
    <h2>Digital-twin state counts</h2>
    {_html_table_from_series(state_counts)}
  </section>

  <section>
    <h2>Synthetic event-label counts</h2>
    <p>
      These labels are generated by the synthetic data generator for demonstration
      and testing. They are not used as real operational truth.
    </p>
    {_html_table_from_series(event_counts)}
  </section>

  <section>
    <h2>Validation messages</h2>
    <h3>Errors</h3>
    <ul>
      {_html_list(errors)}
    </ul>
    <h3>Warnings</h3>
    <ul>
      {_html_list(warnings)}
    </ul>
  </section>

  <section>
    <h2>Recommendations</h2>
    <ul>
      {_html_list(recommendations)}
    </ul>
  </section>

  <section>
    <h2>Notes</h2>
    <p>
      The current model is a baseline demonstration. It prioritises explainability,
      reproducibility and safe publication over hydraulic realism. Future work could
      add richer simulation scenarios, calibration-free uncertainty estimates, visual
      diagnostics and more detailed model-validation notes.
    </p>
  </section>
</body>
</html>
"""

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")

    return html
