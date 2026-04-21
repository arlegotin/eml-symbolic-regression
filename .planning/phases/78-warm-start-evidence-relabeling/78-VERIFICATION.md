# Phase 78 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_reports.py tests/test_campaign.py -q
```

Result: `37 passed in 27.03s`

```bash
PYTHONPATH=src python -m compileall -q src/eml_symbolic_regression/benchmark.py src/eml_symbolic_regression/campaign.py
```

Result: passed.

```bash
git diff --check
```

Result: passed.

## Requirement Coverage

- WARM-01: Covered by `warm_start_evidence=exact_seed_round_trip` for zero-perturbation same-AST rows.
- WARM-02: Covered by campaign `runs.csv` and report fields for perturbation noise, warm steps, warm restarts, total restarts, return kind, and AST-return status.
- WARM-03: Covered by report/README wording changes and campaign regression asserting no warm-start robustness or basin language in the zero-noise smoke report.
- WARM-04: Covered by README, aggregate, campaign report, and tests.

## Residual Risk

- Existing committed v1.13 artifacts are not regenerated in this phase. Phase 81 owns corrected artifact rebuild and source-lock refresh.

