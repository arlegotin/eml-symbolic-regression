---
status: passed
phase: 44
requirements:
  - TRI-01
  - TRI-02
  - TRI-03
  - TRI-04
---

# Phase 44 Verification

## Result

Phase 44 passed. The smoke result is reproducible, centered failures are classified with artifact paths, focused calibration probes are available, and the pre-full-run gate is recorded.

## Requirement Coverage

| Requirement | Evidence | Status |
|-------------|----------|--------|
| TRI-01 | `artifacts/campaigns/v1.8-family-smoke-triage/report.md`, `aggregate.json`, `tables/operator-family-*.csv` | Passed |
| TRI-02 | `artifacts/diagnostics/v1.8-family-triage/family-triage.md` classifies centered blind failures and unsupported paths | Passed |
| TRI-03 | `family-calibration` preset and `artifacts/campaigns/v1.8-family-calibration/` | Passed |
| TRI-04 | `artifacts/diagnostics/v1.8-family-triage/go-no-go.md` records `conditional_go_scoped` | Passed |

## Verification Commands

```bash
PYTHONPATH=src python -m pytest tests/test_family_triage.py tests/test_campaign.py tests/test_benchmark_contract.py
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign family-smoke --output-root artifacts/campaigns --label v1.8-family-smoke-triage --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics family-triage --smoke-aggregate artifacts/campaigns/v1.8-family-smoke-triage/aggregate.json --calibration-aggregate artifacts/campaigns/v1.8-family-calibration/aggregate.json --output-dir artifacts/diagnostics/v1.8-family-triage
```
