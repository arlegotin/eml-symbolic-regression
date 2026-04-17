# Phase 44 Summary: Centered-Family Smoke Triage and Full-Run Gate

**Status:** Complete
**Completed:** 2026-04-17
**Requirements:** TRI-01, TRI-02, TRI-03, TRI-04

## Delivered

- Reproduced the expanded v1.8 `family-smoke` campaign under `artifacts/campaigns/v1.8-family-smoke-triage/`.
- Added `eml_symbolic_regression.family_triage` and CLI diagnostics for centered-family triage and go/no-go artifacts.
- Generated focused `exp`/`log` calibration inputs through the new `family-calibration` preset.
- Wrote triage artifacts under `artifacts/diagnostics/v1.8-family-triage/`, classifying centered blind failures, centered same-family seed gates, and Planck depth exclusions.
- Established a `conditional_go_scoped` full-run gate.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_family_triage.py tests/test_campaign.py tests/test_benchmark_contract.py`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign family-smoke --output-root artifacts/campaigns --label v1.8-family-smoke-triage --overwrite`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics family-triage --smoke-aggregate artifacts/campaigns/v1.8-family-smoke-triage/aggregate.json --calibration-aggregate artifacts/campaigns/v1.8-family-calibration/aggregate.json --output-dir artifacts/diagnostics/v1.8-family-triage`

## Notes

- Smoke recovered raw `exp` and raw Beer-Lambert warm-start paths, while centered `exp` blind rows failed and centered warm-start rows remained explicit unsupported gates.
- The gate allows scoped evidence work but blocks overclaiming centered warm-start support.
