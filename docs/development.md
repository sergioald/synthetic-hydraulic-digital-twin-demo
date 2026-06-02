# Development Guide

This project is intended to demonstrate reproducible applied-AI research software.

The current implementation includes a minimal working synthetic pipeline, tests, a CLI, an example script and repository quality checks.

## Local setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the project with development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Install the pre-commit hooks:

```bash
pre-commit install
```

## Repository checks

Run all pre-commit checks manually:

```bash
pre-commit run --all-files
```

The checks include:

- trailing whitespace removal
- end-of-file fixing
- YAML, TOML and JSON validation
- large-file checks
- Python linting with Ruff
- Python formatting with Ruff

## Tests

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=hydraulic_twin --cov-report=term-missing
```

## Run the synthetic workflow

Run the quickstart example:

```bash
python examples/quickstart.py
```

Or run the CLI:

```bash
hydraulic-twin run \
  --config configs/default.yaml \
  --output reports/example_report.md \
  --data-output data/synthetic_run.csv
```

## Development principles

- Keep all data synthetic.
- Keep modules small and testable.
- Prefer clear baselines before complex ML.
- Document assumptions and validation limits.
- Do not include real FastBlade data, diagrams, parameters, control logic or confidential material.
