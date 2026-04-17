# Phase 48 Summary: Paper Decision Refresh and Milestone Audit

**Status:** Complete
**Completed:** 2026-04-17
**Requirements:** PAP-01, PAP-02, PAP-03, PAP-04, PAP-05

## Delivered

- Updated paper decision generation for v1.8 outputs and aggregate-path citations in safe/unsafe claim documents.
- Added a `publish_raw_eml_searchability_note` decision path when raw EML outperforms centered families.
- Generated `artifacts/paper/v1.8/` from v1.8 smoke, calibration, and scoped standard aggregates.
- Added tests covering aggregate citations and the raw-note decision.
- Prepared milestone verification and audit artifacts with explicit centered-family overclaim checks.
- Fixed code-review findings for perturbed unsupported reasons, v1.8 family tags, stale paper guidance, and campaign overwrite hygiene.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_paper_decision.py`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_centered_warm_start_fails_closed_with_operator_metadata tests/test_benchmark_runner.py::test_centered_perturbed_tree_unsupported_reason_survives_aggregate tests/test_paper_decision.py tests/test_campaign.py tests/test_family_triage.py`
- `PYTHONPATH=src python -m pytest --ignore=tests/test_shallow_blind_proof_regression.py`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli paper-decision --aggregate artifacts/campaigns/v1.8-family-smoke-triage/aggregate.json --aggregate artifacts/campaigns/v1.8-family-calibration/aggregate.json --aggregate artifacts/campaigns/v1.8-family-standard-scoped/aggregate.json --output-dir artifacts/paper/v1.8`

## Notes

- The decision is `publish_raw_eml_searchability_note`: raw EML recovered 80.0% across supplied v1.8 aggregates, while the best centered recovery rate was 0.0%.
- Centered results are reported as negative or diagnostic evidence, not reframed as success.
