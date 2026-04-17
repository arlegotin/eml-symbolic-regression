---
status: complete
phase: 48
review: 48-REVIEW.md
fixed: 2026-04-17
---

# Phase 48 Review Fix Summary

## Findings Fixed

| Finding | Fix | Verification |
|---------|-----|--------------|
| WR-01 | `_run_reason()` now preserves unsupported reasons from `perturbed_true_tree` payloads. | `tests/test_benchmark_runner.py::test_centered_perturbed_tree_unsupported_reason_survives_aggregate` |
| WR-02 | Family-matrix tagging now accepts an explicit suite tag, so v1.8 suites emit `v1.8` tags instead of inherited `v1.7` tags. | `tests/test_benchmark_contract.py::test_v18_family_matrix_expands_scales_and_schedules` |
| IN-01 | No-centered-evidence paper recommendation now says to run the current family campaigns instead of stale v1.7 campaigns. | `tests/test_paper_decision.py::test_paper_decision_waits_when_centered_evidence_is_missing` |
| Evidence hygiene | `run_campaign(..., overwrite=True)` now replaces the campaign directory before rerun, preventing stale orphan run artifacts from surviving suite remaps. | `tests/test_campaign.py::test_campaign_refuses_silent_overwrite` |

## Artifact Refresh

Regenerated after fixes:

- `artifacts/campaigns/v1.8-family-smoke-triage/`
- `artifacts/campaigns/v1.8-family-calibration/`
- `artifacts/campaigns/v1.8-family-standard-scoped/`
- `artifacts/diagnostics/v1.8-family-triage/`
- `artifacts/diagnostics/v1.8-family-evidence/`
- `artifacts/paper/v1.8/`

Integrity scan found no stale `"v1.7"` tags or stale `v1.7 family campaigns` wording in the refreshed v1.8 artifact directories.

## Verification Commands

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_centered_warm_start_fails_closed_with_operator_metadata tests/test_benchmark_runner.py::test_centered_perturbed_tree_unsupported_reason_survives_aggregate tests/test_paper_decision.py tests/test_campaign.py tests/test_family_triage.py
rg -n '"v1\.7"|v1\.7 family campaigns' artifacts/campaigns/v1.8-family-smoke-triage artifacts/campaigns/v1.8-family-calibration artifacts/campaigns/v1.8-family-standard-scoped artifacts/paper/v1.8
```

The focused pytest command passed with 79 tests. The metadata scan returned no matches.
