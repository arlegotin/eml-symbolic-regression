---
phase: 91
plan: 91-01
status: complete
completed: 2026-04-22
---

# Plan 91-01 Summary: fail-closed v1.16 campaign package

## What Changed

- Extended `write_v116_paper_package` and `geml-paper-v116` so the package can source-lock the Phase 90 budget ladder.
- Generated `artifacts/paper/v1.16-geml/` from the completed pilot campaign and budget ladder.
- The full campaign was intentionally not run because the ladder decision is `stop_full_campaign_fail_closed`.

## Package Result

- Package decision: `inconclusive`
- Claim audit: `passed`
- Pilot rows: 12 paired raw/i*pi rows
- Exact recoveries: 0 raw, 0 i*pi
- Loss-only outcomes: 12
- Full campaign route: blocked by pilot gate

## Verification

- `python -m pytest tests/test_paper_v116.py -q` passed with 9 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli geml-paper-v116 --campaign-dir artifacts/campaigns/v1.16-geml-pilot --budget-ladder-dir artifacts/campaigns/v1.16-geml-budget-ladder --output-dir artifacts/paper/v1.16-geml --min-unique-seeds 3 --overwrite` completed with claim audit `passed`.

## Key Files

- `src/eml_symbolic_regression/paper_v116.py`
- `src/eml_symbolic_regression/cli.py`
- `tests/test_paper_v116.py`
- `artifacts/paper/v1.16-geml/`
