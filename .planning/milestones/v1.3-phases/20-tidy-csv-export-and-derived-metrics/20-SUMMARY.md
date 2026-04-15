# Phase 20: Tidy CSV Export and Derived Metrics - Summary

**Completed:** 2026-04-15
**Status:** Complete

## Delivered

- Added `tables/runs.csv` with run identity, optimizer budget, perturbation, losses, verifier status, recovery class, runtime, changed slots, reason, and artifact path.
- Added grouped CSV summaries by formula, start mode, perturbation noise, depth, and recovery/failure class.
- Added `headline-metrics.json` and `headline-metrics.csv`.
- Added `failures.csv` with unsupported/failed cases, reason codes, and artifact links.
- Added table paths to `campaign-manifest.json`.

## Verification

```bash
python -m pytest tests/test_campaign.py tests/test_benchmark_reports.py -q
```

Result: 8 passed.
