---
phase: 90
status: passed
verified: 2026-04-22
---

# Phase 90 Verification

## Goal

Run cheap smoke and pilot campaigns to decide whether search improvements merit the full paper campaign.

## Must-Haves

- Smoke and pilot outputs compare raw EML versus i*pi EML by target family and seed: verified by generated campaign paired tables.
- Pilot gate prevents full run if no exact recovery signal appears: verified by `stop_full_campaign_fail_closed` in `artifacts/campaigns/v1.16-geml-budget-ladder/manifest.json`.
- Failure taxonomy classifies the pilot rows as loss-only outcomes: verified by `failure-taxonomy.json`, `.csv`, and `.md`.
- Reproducible commands and source locks exist for campaign and ladder outputs.

## Automated Checks

```bash
python -m pytest tests/test_paper_v116.py -q
```

Result: passed, 9 tests.

## Campaign Checks

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign geml-v116-smoke --label v1.16-geml-smoke --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign geml-v116-pilot --label v1.16-geml-pilot --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v116-ladder --smoke-dir artifacts/campaigns/v1.16-geml-smoke --pilot-dir artifacts/campaigns/v1.16-geml-pilot --output-dir artifacts/campaigns/v1.16-geml-budget-ladder --overwrite
```

Result: all commands completed successfully. Pilot paired summary: 12 paired rows, 0 raw exact recoveries, 0 i*pi exact recoveries, 12 loss-only outcomes.
