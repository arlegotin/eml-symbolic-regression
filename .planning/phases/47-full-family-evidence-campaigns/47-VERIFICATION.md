---
status: passed
phase: 47
requirements:
  - RUN-01
  - RUN-02
  - RUN-03
  - RUN-04
  - RUN-05
---

# Phase 47 Verification

## Result

Phase 47 passed. The milestone has completed v1.8 smoke, calibration, and scoped standard campaign evidence, plus explicit scope decisions for the larger matrices.

## Requirement Coverage

| Requirement | Evidence | Status |
|-------------|----------|--------|
| RUN-01 | `family-shallow-pure-blind` scoped with reason in `family-evidence-manifest.md` | Passed |
| RUN-02 | `family-shallow`, `family-basin`, and `family-depth-curve` scoped with reasons in `family-evidence-manifest.md` | Passed |
| RUN-03 | `family-standard` ran after calibration; `family-showcase` skipped due no centered signal | Passed |
| RUN-04 | Completed campaigns include recovery, anomaly, shifted-singularity, repair/refit, unsupported, and complexity tables | Passed |
| RUN-05 | Operator-family lock artifacts exist under v1.8 campaign paths without overwriting older anchors | Passed |

## Verification Commands

```bash
PYTHONPATH=src python -m pytest tests/test_family_triage.py tests/test_campaign.py
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign family-standard --output-root artifacts/campaigns --label v1.8-family-standard-scoped --overwrite --formula exp --formula log --formula beer_lambert --seed 0
PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics family-evidence --completed-manifest artifacts/campaigns/v1.8-family-smoke-triage/campaign-manifest.json --completed-manifest artifacts/campaigns/v1.8-family-calibration/campaign-manifest.json --completed-manifest artifacts/campaigns/v1.8-family-standard-scoped/campaign-manifest.json --output-dir artifacts/diagnostics/v1.8-family-evidence
```
