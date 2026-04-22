# Phase 84 Plan: Family-Aware Training and Snapping Integration

## Tasks

1. Enrich optimizer trace and candidate artifacts.
   - Add gradient norm metrics to each training/hardening trace row.
   - Add branch diagnostic fields from `AnomalyStats` to trace rows and summaries.
   - Add explicit pre-snap/post-snap MSE aliases to exact candidate artifacts.
   - Add wall-clock timing metadata to run manifests.

2. Wire i*pi EML through optimizer smoke paths.
   - Verify `TrainingConfig(operator_family=ipi_eml_operator())` trains and snaps to `Geml` artifacts.
   - Preserve raw EML default behavior.
   - Preserve non-raw scaffold exclusions so raw witnesses are not reused.

3. Surface metrics in semantics alignment and verifier evidence.
   - Include selected candidate branch diagnostics from verifier reports.
   - Include branch-count summaries in anomaly summaries.
   - Preserve existing manifest keys.

4. Add regression tests.
   - Add i*pi optimizer smoke tests for family metadata, scaffold exclusions, candidate fields, branch fields, gradient norms, and timing.
   - Re-run raw/centered optimizer and Phase 83 verifier tests.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_master_tree.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m compileall -q src`
- `git diff --check`
