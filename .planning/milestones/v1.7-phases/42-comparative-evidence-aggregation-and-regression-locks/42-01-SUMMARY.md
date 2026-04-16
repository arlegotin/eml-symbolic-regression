# Phase 42 Summary: Comparative Evidence Aggregation and Regression Locks

**Status:** Complete
**Completed:** 2026-04-16
**Requirements:** EVD-03, EVD-04, EVD-05

## Delivered

- Added campaign-level operator-family recovery tables grouped by operator family, continuation schedule, formula, start mode, training mode, and depth.
- Added operator-family diagnostic tables with verifier pass rate, unsupported rate, repair/refit usage, anomaly totals, shifted-singularity diagnostics, post-snap loss, and active-node/complexity summaries.
- Added operator-family comparison Markdown and compact regression-lock JSON outputs under each campaign `tables/` directory.
- Linked operator-family comparison outputs from campaign reports when more than one operator family is present.
- Extended benchmark metric extraction with centered-family anomaly counters and candidate-complexity metadata.

## Verification

```bash
python -m pytest tests/test_campaign.py tests/test_benchmark_reports.py tests/test_benchmark_contract.py
```

Result: `87 passed`.

## Notes

- The comparison artifacts are generated for all campaigns. Single-family campaigns still get the CSV/JSON files, while the report section appears only when multiple operator families are present.
- Regression locks intentionally store rates and group counts, not timestamps, so future tests can compare family behavior without brittle provenance churn.
