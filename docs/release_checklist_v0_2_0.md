# v0.2.0 release checklist

Use this checklist before creating a public GitHub release.

## 1. Confirm branch state

```bash
git checkout main
git pull origin main
git status
```

Expected:

```text
nothing to commit, working tree clean
```

## 2. Run quality checks

```bash
pre-commit run --all-files
pytest
```

Optional coverage command:

```bash
pytest --cov=hydraulic_twin --cov-report=term-missing
```

## 3. Regenerate reproducible assets

```bash
python examples/create_example_figures.py
python examples/create_scenario_overview_figure.py
python examples/run_scenarios.py
```

Then check that generated CSV/report outputs have not been staged accidentally:

```bash
git status
```

Generated scenario outputs should normally remain ignored:

```text
data/scenarios/
reports/scenarios/
```

## 4. Review documentation

Check the following files:

```text
README.md
CHANGELOG.md
docs/case_study.md
docs/reviewer_guide.md
docs/scenario_configs.md
docs/validation_scope.md
docs/confidentiality_statement.md
docs/synthetic_data_design.md
```

Confirm that all documents consistently state that the repository uses synthetic
data only.

## 5. Confirm confidentiality boundary

Before release, confirm the repository does not contain:

- real FastBlade data;
- partner or industrial data;
- raw facility sensor exports;
- facility-specific diagrams;
- proprietary control logic;
- confidential reports;
- private file paths;
- personal information;
- internal credentials or tokens.

Useful commands:

```bash
git grep -n "FastBlade"
git grep -n "confidential"
git grep -n "password"
git grep -n "token"
git grep -n "C:\\"
git grep -n "/Users/"
```

Manual review is still required.

## 6. Update changelog release date

In `CHANGELOG.md`, change:

```markdown
## [0.2.0] - Unreleased
```

to the release date, for example:

```markdown
## [0.2.0] - 2026-06-22
```

Only do this when you are ready to create the release.

## 7. Commit release-date update

```bash
git add CHANGELOG.md
git commit -m "Prepare v0.2.0 release"
git push
```

## 8. Create tag

```bash
git tag -a v0.2.0 -m "v0.2.0"
git push origin v0.2.0
```

## 9. Create GitHub release

On GitHub:

1. Go to **Releases**.
2. Select **Draft a new release**.
3. Choose tag `v0.2.0`.
4. Use release title:

```text
v0.2.0 — Scenario configs and validation-scope documentation
```

5. Use this summary:

```markdown
This release strengthens the repository as a public, confidentiality-safe applied-AI and research-software demo.

Highlights:
- scenario-based synthetic configurations;
- tests for features, reporting, CLI execution and full pipeline runs;
- validation-scope documentation;
- reviewer-facing case study and guide;
- README updates and generated-output cleanup.

The repository remains fully synthetic and does not include real facility data, partner data, proprietary control logic or confidential operational material.
```

## 10. After release

Confirm:

- release is visible on GitHub;
- README badge still works;
- Actions are green;
- repository description and topics are updated;
- generated files are not accidentally tracked.

## 11. Suggested next release ideas

Possible `v0.3.0` improvements:

- model-card documentation;
- HTML report output;
- uncertainty summary in reports;
- scenario comparison table;
- simple dashboard;
- packaged example release assets;
- additional anomaly-detection baseline.
