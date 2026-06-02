# Development Guide

This project is intended to demonstrate reproducible applied-AI research software.

The first commit defines the development standards and confidentiality boundary. Source code, tests and examples will be added in later commits.

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

Once the source code and tests are added, run:

```bash
pytest
```

Coverage checks can later be run with:

```bash
pytest --cov=hydraulic_twin --cov-report=term-missing
```

## Development principles

- Keep all data synthetic.
- Keep modules small and testable.
- Prefer clear, explainable baselines before complex ML.
- Document assumptions and validation limits.
- Keep public names generic and non-facility-specific.
- Do not include real FastBlade data, diagrams, parameters, control logic or confidential material.

## Recommended commit sequence

```text
1. Initial project structure and confidentiality boundary
2. Add synthetic data pipeline and baseline digital twin workflow
3. Add tests and example report
4. Improve documentation and validation notes
5. Add coverage reporting and example visualisations
```
