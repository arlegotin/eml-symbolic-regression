# Phase 86 Summary: Matched EML versus i*pi EML Campaign Runner

## Status

Complete.

## Commits

- `6181fb0` - `docs(86): smart discuss context and plan`
- `5e74d21` - `feat(86): add paired GEML campaign outputs`

## Delivered

- Exposed Phase 84 optimizer metrics in benchmark run metrics: pre-snap MSE, post-snap MSE, gradient maxima, branch counts, branch diagnostics, optimizer wall-clock, attempt count, and candidate count.
- Added those fields to campaign `runs.csv` output.
- Extended operator-family diagnostics with branch proximity/crossing/input totals, gradient medians, and optimizer wall-clock medians.
- Added stable GEML paired artifacts:
  - `geml-paired-comparison.csv`
  - `geml-paired-summary.json`
  - `geml-paired-comparison.md`
- Added paired report links to campaign reports when raw/i*pi pairs exist.
- Preserved v1.14 accounting fields in paired rows: `verification_outcome`, `evidence_regime`, `discovery_class`, `warm_start_evidence`, and `ast_return_status`.

## Tests

- `PYTHONPATH=src python -m pytest tests/test_campaign.py::test_campaign_writes_tidy_csvs_and_headline_metrics tests/test_campaign.py::test_campaign_tables_emit_geml_paired_comparison tests/test_benchmark_reports.py::test_run_metric_extraction_exposes_phase84_geml_fields -q`
- `PYTHONPATH=src python -m pytest tests/test_campaign.py tests/test_benchmark_reports.py -q`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_runner_filter_executes_subset -q`
- `PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m compileall -q src tests`
- `git diff --check`

## Outcome

The existing campaign runner now produces paired raw EML versus i*pi EML evidence under the Phase 85 protocol, with verifier-gated trained recovery and numerical diagnostics ready for Phase 87 claim-boundary packaging.
