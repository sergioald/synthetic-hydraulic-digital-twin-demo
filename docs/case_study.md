# Case study: Synthetic hydraulic digital twin

## One-line summary

This repository is a confidentiality-safe applied-AI case study showing how a
digital-twin-style workflow can be structured for sensor-heavy hydraulic systems
using fully synthetic data.

## Why this case study exists

Real hydraulic testing facilities, industrial control systems and research rigs
can generate valuable sensor data. However, public release is often restricted
because the data may contain:

- facility-specific operating conditions;
- proprietary control logic;
- partner or industrial datasets;
- sensitive test parameters;
- raw sensor exports;
- internal diagnostic thresholds;
- confidential reports or diagrams.

This repository solves that portfolio/publication problem by replacing real data
with a synthetic but structured analogue. The aim is not to reproduce a real
facility, but to demonstrate the software architecture, data workflow and
engineering reasoning around an applied-AI digital-twin pipeline.

## Problem represented by the synthetic workflow

A sensor-rich hydraulic system may need to answer questions such as:

- Are the incoming sensor signals complete and plausible?
- Are pressure, flow, load, temperature and power signals behaving consistently?
- Is energy use increasing unexpectedly?
- Are there periods that deserve engineering review?
- Can system states be classified into interpretable categories?
- Can the workflow produce a readable report for non-ML stakeholders?

The repository demonstrates how these questions can be addressed in a
reproducible software workflow without using real operational data.

## Synthetic workflow

The pipeline follows this sequence:

```text
synthetic data generation
→ sensor validation
→ feature engineering
→ hydraulic/electrical energy estimation
→ anomaly detection
→ digital-twin state classification
→ Markdown report generation
```

The output is a synthetic dataset, interpretable state labels, anomaly flags,
energy summaries and an engineering-style Markdown report.

## What the project demonstrates

### Research-software structure

The repository uses a standard Python package layout, a command-line interface,
configuration files, tests, documentation and continuous integration. This makes
it easier to review, reproduce and extend than a single notebook or ad-hoc
script.

### Configuration-driven execution

The default workflow and the scenario workflows are controlled by YAML files.
This makes it clear which synthetic events are being exercised and avoids hiding
key assumptions inside code.

### Synthetic scenario design

The scenario configurations allow reviewers to run targeted examples, including:

- normal operation;
- pressure loss;
- sensor drift;
- missing data;
- pump degradation;
- abnormal energy use;
- load-response anomaly;
- transient response;
- mixed synthetic faults.

Each scenario uses the same pipeline, which makes it useful for regression
testing, demonstrations and comparison.

### Explainable anomaly and state logic

The anomaly-detection layer combines transparent rule-based checks with a simple
Isolation Forest baseline. The state-classification layer maps features,
validation issues and anomaly flags into interpretable labels such as:

- `normal`;
- `sensor_issue`;
- `pressure_loss_suspected`;
- `inefficient_operation`;
- `pump_degradation_suspected`;
- `load_response_anomaly`;
- `transient_response`.

The point is not to claim operational diagnosis, but to show how a digital-twin
workflow can turn raw sensor streams into reviewable engineering states.

### Reporting for engineering review

The generated Markdown report summarises:

- run-level information;
- validation messages;
- digital-twin state counts;
- synthetic event-label counts;
- recommendations;
- interpretation notes.

This supports an applied-AI communication pattern where results are made readable
for engineers, facility users and project reviewers.

## What the tests demonstrate

The tests check software behaviour, including:

- reproducible synthetic data generation;
- required sensor columns and timestamp structure;
- validation checks for missing or implausible data;
- feature-engineering outputs;
- energy-model outputs;
- anomaly-detection outputs;
- state-classification outputs;
- report generation;
- command-line execution;
- end-to-end scenario configuration runs.

The tests help show that the repository is structured as maintainable research
software rather than a static code dump.

## What the tests do not demonstrate

The tests do not prove:

- calibration against a real hydraulic system;
- real fault-diagnosis accuracy;
- operational safety;
- physical fidelity of the synthetic signals;
- suitability for live control decisions;
- generalisation to unseen industrial datasets.

This distinction is deliberate. The repository is a public demonstration of
method structure and software practice, not a validated operational monitoring
product.

## How to run the case study

Install the package in development mode:

```bash
python -m pip install -e ".[dev]"
```

Run the default workflow:

```bash
hydraulic-twin run \
  --config configs/default.yaml \
  --output reports/example_report.md \
  --data-output data/synthetic_run.csv
```

Run all scenarios:

```bash
python examples/run_scenarios.py
```

Run the tests:

```bash
pytest
```

Run linting and formatting checks:

```bash
pre-commit run --all-files
```

## Why this is useful for reviewers

This case study gives reviewers a concrete example of:

- applied AI for engineering sensor systems;
- digital-twin-style software design;
- anomaly detection and state classification;
- reproducible data workflows;
- testable research code;
- confidentiality-safe public communication.

It is designed to be read quickly but also to be runnable and inspectable.

## Future extensions

Possible next steps include:

- richer synthetic scenario parameters;
- uncertainty summaries in reports;
- additional baseline anomaly-detection models;
- HTML report generation;
- model-card documentation;
- simple dashboard or Streamlit interface;
- small benchmark comparing rule-based and ML anomaly flags;
- optional synthetic data schema export;
- GitHub release assets for generated example reports.
  
