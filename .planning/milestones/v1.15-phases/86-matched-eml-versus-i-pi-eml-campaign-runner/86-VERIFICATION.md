status: passed

# Phase 86 Verification

## Result

Passed. Campaign outputs now include paired raw EML versus i*pi EML rows and aggregate diagnostics under the existing campaign protocol.

## Requirements Checked

- **EVID-01:** `write_campaign_tables()` emits paired raw EML and i*pi EML rows for matched formula/seed/start-mode/training-mode/depth/constants-policy pairs.
- **EVID-02:** Paired and diagnostic outputs include trained exact recovery after snapping, pre-snap MSE, post-snap MSE, gradient stats, overflow/NaN counts, branch counts, runtime, optimizer wall-clock, and environment metadata from existing campaign manifests.
- **v1.14 accounting preservation:** Paired rows include `verification_outcome`, `evidence_regime`, `discovery_class`, `warm_start_evidence`, and `ast_return_status`, and trained recovery is based on `discovery_class == trained_exact_recovery`.

## Tests

Passed:

```bash
PYTHONPATH=src python -m pytest tests/test_campaign.py::test_campaign_writes_tidy_csvs_and_headline_metrics tests/test_campaign.py::test_campaign_tables_emit_geml_paired_comparison tests/test_benchmark_reports.py::test_run_metric_extraction_exposes_phase84_geml_fields -q
# 3 passed in 5.15s

PYTHONPATH=src python -m pytest tests/test_campaign.py tests/test_benchmark_reports.py -q
# 39 passed in 29.24s

PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_runner_filter_executes_subset -q
# 72 passed, 2 warnings in 48.42s

PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_verify.py -q
# 22 passed, 2 warnings in 10.22s

PYTHONPATH=src python -m compileall -q src tests
# passed

git diff --check
# passed
```

Warnings were existing numerical overflow and branch-domain warnings in benchmark stress fixtures.
