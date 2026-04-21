# Phase 78 Summary: Warm-Start Evidence Relabeling

## Completed

- Added `warm_start_evidence` and `ast_return_status` to run payloads, aggregate run summaries, aggregate groupings, and campaign CSV rows.
- Added `total_restarts` to aggregate run summaries and campaign CSV rows using the active restart count for each start mode.
- Labeled zero-perturbation same-AST warm starts as `exact_seed_round_trip`.
- Added a campaign report `Warm-Start Evidence` section exposing perturbation noise, warm steps, warm restarts, total restarts, return kind, and AST-return status.
- Reworded README and generated report text so zero-perturbation same-AST warm starts are exact seed round-trips, not blind discovery or claims about behavior away from the seed.

## Code Changes

- `src/eml_symbolic_regression/benchmark.py`
  - Derives warm-start evidence labels and AST-return status.
  - Carries those labels into metrics, aggregate rows, and aggregate Markdown groupings.
- `src/eml_symbolic_regression/campaign.py`
  - Exports the new CSV columns.
  - Adds report-level warm-start evidence rows.
  - Removes unsupported warm-start basin/robustness wording from zero-noise report paths.
- `README.md`
  - Updates evidence label and boundary wording.
- `tests/test_benchmark_reports.py`, `tests/test_campaign.py`
  - Lock the exact seed round-trip label and new CSV/report columns.

## Commits

- `9c71e7a docs(78): smart discuss context and plan`
- `ab0b663 fix(78): relabel warm-start evidence`

