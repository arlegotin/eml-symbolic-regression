---
phase: 90
plan: 90-01
status: complete
completed: 2026-04-22
---

# Plan 90-01 Summary: v1.16 budget ladder and pilot gate

## What Changed

- Added `write_v116_budget_ladder` to create deterministic smoke/pilot/full routing artifacts.
- Added failure taxonomy JSON/CSV/Markdown outputs for loss-only, snap/optimization miss, branch pathology, unsupported/over-depth, numerical instability, and verifier mismatch classes.
- Added `geml-v116-ladder` CLI command.
- Ran actual v1.16 smoke and pilot campaigns:
  - Smoke: `artifacts/campaigns/v1.16-geml-smoke`
  - Pilot: `artifacts/campaigns/v1.16-geml-pilot`
- Generated budget ladder: `artifacts/campaigns/v1.16-geml-budget-ladder`

## Pilot Result

The pilot found no verifier-gated exact recoveries. It produced 12 paired rows, all loss-only outcomes: 3 i*pi lower post-snap MSE rows and 9 raw lower post-snap MSE rows.

Budget-ladder decision: `stop_full_campaign_fail_closed`.

## Verification

- `python -m pytest tests/test_paper_v116.py -q` passed with 9 tests.
- Campaign commands completed successfully:
  - `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign geml-v116-smoke --label v1.16-geml-smoke --overwrite`
  - `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign geml-v116-pilot --label v1.16-geml-pilot --overwrite`
  - `PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v116-ladder --smoke-dir artifacts/campaigns/v1.16-geml-smoke --pilot-dir artifacts/campaigns/v1.16-geml-pilot --output-dir artifacts/campaigns/v1.16-geml-budget-ladder --overwrite`

## Key Files

- `src/eml_symbolic_regression/paper_v116.py`
- `src/eml_symbolic_regression/cli.py`
- `tests/test_paper_v116.py`
- `artifacts/campaigns/v1.16-geml-smoke/`
- `artifacts/campaigns/v1.16-geml-pilot/`
- `artifacts/campaigns/v1.16-geml-budget-ladder/`
