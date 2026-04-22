# Phase 83 Summary: i*pi EML Restricted Theory and Branch Contract

## Status

Complete.

## Commits

- `252f16b` - `docs(83): smart discuss context and plan`
- `5a5a31c` - `feat(83): add ipi branch theory contract`

## Delivered

- Added reusable principal-log branch diagnostics in `branch.py`.
- Extended `AnomalyStats` with branch input counts, proximity counts, crossing counts, minimum branch-cut distance, and invalid-domain skip counts.
- Extended verifier reports with structured `branch_diagnostics`, including branch convention, canonical branch schema fields, branch-safety guard contract, and branch-related candidate failure classification.
- Added high-precision executable i*pi EML theory checks for reciprocal, positive-real recovery, real-axis derivative, and one-step composition magnitude bound.
- Generated theory artifacts under `artifacts/theory/v1.15/`.
- Documented restricted theory assumptions, non-claims, principal-log branch convention, and faithful-verification boundaries.

## Tests

- `PYTHONPATH=src python -m pytest tests/test_geml_theory.py tests/test_semantics_expression.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py::test_runner_filter_executes_subset tests/test_benchmark_reports.py -q`
- `PYTHONPATH=src python -m compileall -q src`
- `git diff --check`

## Outcome

i*pi EML now has an explicit restricted-domain theory artifact and branch-diagnostic contract before entering training and benchmark phases.
