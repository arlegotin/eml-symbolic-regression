---
status: passed
phase: 46
requirements:
  - MAT-01
  - MAT-02
  - MAT-03
  - MAT-04
  - MAT-05
---

# Phase 46 Verification

## Result

Phase 46 passed. The expanded v1.8 matrix is built, calibration is separately runnable, and calibration artifacts record budgets, variants, exclusions, and downstream scope guidance.

## Requirement Coverage

| Requirement | Evidence | Status |
|-------------|----------|--------|
| MAT-01 | `v1.8-family-*` suites include raw plus fixed `CEML_s`/`ZEML_s` for `s in {1,2,4,8}` | Passed |
| MAT-02 | Suite variants include `ZEML_8 -> ZEML_4` and `ZEML_8 -> ZEML_4 -> ZEML_2 -> ZEML_1` | Passed |
| MAT-03 | `family-calibration`, `family-shallow-pure-blind`, `family-shallow`, `family-basin`, `family-depth-curve`, `family-standard`, `family-showcase` presets exist | Passed |
| MAT-04 | Campaign manifests and operator-family tables expose formula, mode, depth, seed, family, and schedule | Passed |
| MAT-05 | `artifacts/diagnostics/v1.8-family-triage/go-no-go.md` records budgets, exclusions, and full-run scope | Passed |

## Verification Commands

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py tests/test_family_triage.py
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign family-calibration --output-root artifacts/campaigns --label v1.8-family-calibration --overwrite
```
