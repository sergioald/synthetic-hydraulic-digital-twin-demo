"""Create the README scenario overview figure.

The output is an SVG diagram designed for GitHub README rendering.
It is intentionally simple and text-based so it remains easy to edit.
"""

from __future__ import annotations

from pathlib import Path

SCENARIO_OVERVIEW_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720" role="img" aria-labelledby="title desc">
  <title id="title">Synthetic scenario configuration overview</title>
  <desc id="desc">Overview of scenario-specific YAML files feeding the same synthetic hydraulic digital-twin pipeline.</desc>

  <rect x="20" y="20" width="1160" height="680" rx="28" fill="#ffffff" stroke="#222222" stroke-width="2"/>

  <text x="600" y="70" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="700">
    Synthetic scenario configurations
  </text>
  <text x="600" y="105" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">
    Each YAML file exercises the same digital-twin workflow under a different synthetic condition
  </text>

  <g font-family="Arial, Helvetica, sans-serif" font-size="18">
    <rect x="80" y="155" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="230" y="191" text-anchor="middle" font-weight="700">normal.yaml</text>

    <rect x="80" y="235" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="230" y="271" text-anchor="middle" font-weight="700">pressure_loss.yaml</text>

    <rect x="80" y="315" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="230" y="351" text-anchor="middle" font-weight="700">sensor_drift.yaml</text>

    <rect x="80" y="395" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="230" y="431" text-anchor="middle" font-weight="700">missing_data.yaml</text>

    <rect x="80" y="475" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="230" y="511" text-anchor="middle" font-weight="700">pump_degradation.yaml</text>

    <rect x="820" y="155" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="970" y="191" text-anchor="middle" font-weight="700">abnormal_energy.yaml</text>

    <rect x="820" y="235" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="970" y="271" text-anchor="middle" font-weight="700">load_anomaly.yaml</text>

    <rect x="820" y="315" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="970" y="351" text-anchor="middle" font-weight="700">transient_event.yaml</text>

    <rect x="820" y="395" width="300" height="58" rx="14" fill="#f7f7f7" stroke="#222222"/>
    <text x="970" y="431" text-anchor="middle" font-weight="700">mixed_faults.yaml</text>
  </g>

  <g>
    <rect x="450" y="210" width="300" height="290" rx="24" fill="#ffffff" stroke="#222222" stroke-width="2"/>
    <text x="600" y="255" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700">
      Same pipeline
    </text>
    <text x="600" y="300" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">synthetic data</text>
    <text x="600" y="335" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">validation</text>
    <text x="600" y="370" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">features + energy</text>
    <text x="600" y="405" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">anomaly detection</text>
    <text x="600" y="440" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">state classification</text>
    <text x="600" y="475" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">Markdown report</text>
  </g>

  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#222222"/>
    </marker>
  </defs>

  <g stroke="#222222" stroke-width="2" marker-end="url(#arrow)">
    <line x1="380" y1="184" x2="450" y2="260"/>
    <line x1="380" y1="264" x2="450" y2="310"/>
    <line x1="380" y1="344" x2="450" y2="355"/>
    <line x1="380" y1="424" x2="450" y2="405"/>
    <line x1="380" y1="504" x2="450" y2="455"/>

    <line x1="820" y1="184" x2="750" y2="260"/>
    <line x1="820" y1="264" x2="750" y2="320"/>
    <line x1="820" y1="344" x2="750" y2="390"/>
    <line x1="820" y1="424" x2="750" y2="450"/>
  </g>

  <rect x="210" y="600" width="780" height="52" rx="14" fill="#f7f7f7" stroke="#222222"/>
  <text x="600" y="633" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18">
    Synthetic demonstration only — not calibrated operational hydraulic validation
  </text>
</svg>
"""


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_path = repo_root / "docs" / "assets" / "readme_scenario_overview.svg"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(SCENARIO_OVERVIEW_SVG, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
