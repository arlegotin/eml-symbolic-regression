# Phase 85 Plan: Oscillatory Benchmark Pack and Negative Controls

## Tasks

1. Register benchmark targets.
   - Add periodic targets for `sin(pi*x)` and `cos(pi*x)`.
   - Add a simple harmonic sum target.
   - Add a standing-wave snapshot target.
   - Add a log-periodic positive-domain target.
   - Add polynomial and rational negative-control targets.

2. Add matched v1.15 benchmark suites.
   - Add built-in suite IDs to the registry.
   - Pair every declared target across raw EML and i*pi EML rows.
   - Keep points, depth, steps, restarts, scaffolds, constants, verifier policy, and split policy matched except for operator family.
   - Mark target-family and negative-control tags for downstream aggregation.

3. Add fail-closed validation for i*pi branch-domain declarations.
   - Require branch-domain tags for i*pi rows in the v1.15 target set.
   - Enforce positive finite domains for log-periodic rows.
   - Raise `BenchmarkValidationError` for missing or unsafe branch declarations.

4. Add tests.
   - Verify new targets are present and produce finite deterministic splits.
   - Verify built-in v1.15 suites validate and preserve matched raw/i*pi budgets.
   - Verify branch-domain validation fails closed for malformed i*pi rows.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py tests/test_benchmark_reports.py -q`
- `PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m compileall -q src tests`
- `git diff --check`
