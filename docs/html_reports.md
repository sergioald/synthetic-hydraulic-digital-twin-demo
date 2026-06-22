# HTML reports

The workflow can generate a self-contained HTML report in addition to the
default Markdown report.

The HTML report is intended for quick local review, portfolio demonstrations
and sharing results with non-technical readers. It is generated from the same
synthetic pipeline data and has the same interpretation boundary as the
Markdown report.

## Generate Markdown and HTML reports

Run:

```bash
hydraulic-twin run \
  --config configs/default.yaml \
  --output reports/example_report.md \
  --html-output reports/example_report.html \
  --data-output data/synthetic_run.csv
```

On Windows PowerShell:

```powershell
hydraulic-twin run `
  --config configs/default.yaml `
  --output reports/example_report.md `
  --html-output reports/example_report.html `
  --data-output data/synthetic_run.csv
```

## Generate a scenario HTML report

```bash
hydraulic-twin run \
  --config configs/scenarios/pressure_loss.yaml \
  --output reports/scenarios/pressure_loss_report.md \
  --html-output reports/scenarios/pressure_loss_report.html \
  --data-output data/scenarios/pressure_loss_synthetic_run.csv
```

## What the HTML report contains

The HTML report includes:

- publication boundary;
- run summary;
- digital-twin state counts;
- synthetic event-label counts;
- validation errors and warnings;
- recommendations;
- notes on the synthetic and baseline nature of the workflow.

## Generated-output policy

HTML reports are reproducible generated outputs. They should normally not be
committed unless a specific example report is intentionally added as a release
asset or documentation artifact.

## Interpretation boundary

The HTML report does not change the validation status of the workflow. It is a
presentation format for synthetic outputs, not evidence of operational
calibration or real-world diagnostic accuracy.
