# Phase 86 Plan: Matched EML versus i*pi EML Campaign Runner

## Tasks

1. Expose Phase 84 metrics in benchmark run metrics.
   - Add pre-snap and post-snap MSE aliases.
   - Add gradient summary metrics.
   - Add branch proximity/crossing/min-distance metrics.
   - Add optimizer wall-clock, attempt count, and candidate count.

2. Add paired GEML comparison artifacts to campaign tables.
   - Group raw EML and i*pi EML rows by formula, seed, start mode, training mode, depth, and constants policy.
   - Emit paired CSV rows comparing verifier status, discovery class, pre/post snap losses, gradients, anomaly counts, branch counts, runtime, and artifact paths.
   - Emit JSON summary counts and markdown report.

3. Preserve claim-accounting fields.
   - Include `verification_outcome`, `evidence_regime`, `discovery_class`, `warm_start_evidence`, and `ast_return_status` in paired rows.
   - Classify trained recovery only from `discovery_class == trained_exact_recovery`.

4. Add tests.
   - Verify metric extraction exposes Phase 84 fields.
   - Verify synthetic raw/i*pi aggregate writes paired CSV, JSON, and markdown artifacts.
   - Verify existing campaign and benchmark report tests still pass.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_campaign.py tests/test_benchmark_reports.py -q`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_runner_filter_executes_subset -q`
- `PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m compileall -q src tests`
- `git diff --check`
