# Phase 62 Summary

## Implemented

- Added `src/eml_symbolic_regression/paper_assets.py`.
- Added CLI command:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-assets --output-dir artifacts/paper/v1.11/assets
```

- Added tests in `tests/test_paper_assets.py`.
- Generated `artifacts/paper/v1.11/assets/` with:
  - 7 source tables in JSON, CSV, and Markdown,
  - 7 deterministic SVG figures,
  - 7 per-figure metadata JSON files,
  - 1 source-locking asset manifest.

## Generated Tables and Figures

| Asset | Purpose |
|-------|---------|
| `regime_recovery` | Shows recovery by separated evidence regime. |
| `depth_degradation` | Shows historical depth-curve recovery degradation. |
| `scientific_law_support` | Shows supported and unsupported scientific-law rows, including logistic and Planck. |
| `motif_depth_deltas` | Shows reusable motif compile-depth reductions. |
| `training_lifecycle` | Shows best soft loss and post-snap loss without treating loss as recovery. |
| `failure_taxonomy` | Shows visible unsupported and failed probe rows. |
| `baseline_diagnostics` | Shows prediction-only local baseline diagnostics outside EML recovery denominators. |

## Claim Boundaries

- Logistic and Planck remain unsupported in the scientific-law support asset.
- Regime recovery uses suite/start-mode-local denominators.
- Depth degradation uses archived v1.6 proof-depth-curve evidence as boundary context.
- Baseline diagnostics are labeled prediction-only and do not enter symbolic recovery claims.
