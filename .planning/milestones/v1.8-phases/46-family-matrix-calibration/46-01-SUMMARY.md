# Phase 46 Summary: Family Matrix Calibration

**Status:** Complete
**Completed:** 2026-04-17
**Requirements:** MAT-01, MAT-02, MAT-03, MAT-04, MAT-05

## Delivered

- Added v1.8 family suite IDs for smoke, calibration, shallow pure-blind, shallow scaffolded, basin, depth-curve, standard, and showcase matrices.
- Expanded variants to raw EML, fixed `CEML_1/2/4/8`, fixed `ZEML_1/2/4/8`, and schedules `ZEML_8 -> ZEML_4` and `ZEML_8 -> ZEML_4 -> ZEML_2 -> ZEML_1`.
- Added `family-calibration` campaign preset with focused `exp`/`log` probes.
- Ran calibration under `artifacts/campaigns/v1.8-family-calibration/`.
- Regenerated triage/go-no-go outputs from smoke plus calibration aggregates.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py tests/test_family_triage.py`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign family-calibration --output-root artifacts/campaigns --label v1.8-family-calibration --overwrite`

## Notes

- Calibration recovered raw `exp`/`log` but recovered 0/20 centered calibration rows, which directly informed the scoped full-run gate.
