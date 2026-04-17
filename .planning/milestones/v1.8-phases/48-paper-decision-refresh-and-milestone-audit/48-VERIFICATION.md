---
status: passed
phase: 48
requirements:
  - PAP-01
  - PAP-02
  - PAP-03
  - PAP-04
  - PAP-05
---

# Phase 48 Verification

## Result

Phase 48 passed. The v1.8 paper package is generated from actual v1.8 aggregate paths, chooses a raw-EML note, cites evidence inputs, and preserves the centered-family claim boundary.

## Requirement Coverage

| Requirement | Evidence | Status |
|-------------|----------|--------|
| PAP-01 | `artifacts/paper/v1.8/` generated | Passed |
| PAP-02 | `decision-memo.md` chooses `publish_raw_eml_searchability_note` | Passed |
| PAP-03 | `safe-claims.md` and `unsafe-claims.md` cite v1.8 aggregate paths and warn against regime merging | Passed |
| PAP-04 | `decision-memo.md` reports best centered recovery rate as 0.0% and avoids success framing | Passed |
| PAP-05 | `.planning/v1.8-MILESTONE-AUDIT.md` covers requirements, evidence integrity, and overclaim checks | Passed |
| Review fixes | `48-REVIEW-FIX.md` covers WR-01, WR-02, IN-01, and campaign overwrite hygiene | Passed |

## Verification Commands

```bash
PYTHONPATH=src python -m pytest tests/test_paper_decision.py
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_centered_warm_start_fails_closed_with_operator_metadata tests/test_benchmark_runner.py::test_centered_perturbed_tree_unsupported_reason_survives_aggregate tests/test_paper_decision.py tests/test_campaign.py tests/test_family_triage.py
PYTHONPATH=src python -m pytest --ignore=tests/test_shallow_blind_proof_regression.py
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-decision --aggregate artifacts/campaigns/v1.8-family-smoke-triage/aggregate.json --aggregate artifacts/campaigns/v1.8-family-calibration/aggregate.json --aggregate artifacts/campaigns/v1.8-family-standard-scoped/aggregate.json --output-dir artifacts/paper/v1.8
rg -n '"v1\.7"|v1\.7 family campaigns' artifacts/campaigns/v1.8-family-smoke-triage artifacts/campaigns/v1.8-family-calibration artifacts/campaigns/v1.8-family-standard-scoped artifacts/paper/v1.8
```

The broad non-expensive suite passed with 245 tests. The focused review-fix suite passed with 79 tests. The v1.8 artifact metadata scan returned no matches.
