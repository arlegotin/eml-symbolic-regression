# Phase 47 Summary: Full Family Evidence Campaigns

**Status:** Complete
**Completed:** 2026-04-17
**Requirements:** RUN-01, RUN-02, RUN-03, RUN-04, RUN-05

## Delivered

- Added `write_family_evidence_manifest` and CLI diagnostics for v1.8 completed/scoped family campaign accounting.
- Ran a post-calibration scoped `family-standard` campaign under `artifacts/campaigns/v1.8-family-standard-scoped/`.
- Linked completed smoke, calibration, and standard campaign aggregates plus operator-family regression locks.
- Recorded deliberate scope reasons for shallow pure-blind, shallow scaffolded, basin, depth-curve, and showcase campaigns under `artifacts/diagnostics/v1.8-family-evidence/`.
- Preserved archived v1.4-v1.7 anchors by writing all v1.8 outputs to new paths.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_family_triage.py tests/test_campaign.py`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign family-standard --output-root artifacts/campaigns --label v1.8-family-standard-scoped --overwrite --formula exp --formula log --formula beer_lambert --seed 0`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics family-evidence ...`

## Notes

- Standard scoped run summarized 55 runs: 4 verifier recoveries, 30 unsupported centered gates, 21 failed fits.
- `family-showcase` was skipped because neither smoke nor calibration showed a centered-family positive signal.
