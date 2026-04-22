# Phase 85 Summary: Oscillatory Benchmark Pack and Negative Controls

## Status

Complete.

## Commits

- `f3865c1` - `docs(85): smart discuss context and plan`
- `5eba6ce` - `feat(85): add GEML oscillatory benchmark suite`

## Delivered

- Added normalized oscillatory demo targets for `sin_pi`, `cos_pi`, `harmonic_sum`, `standing_wave_snapshot`, and `log_periodic_oscillation`.
- Reused existing `damped_oscillator` as the damped oscillation target.
- Added negative-control demo targets for `quadratic_polynomial` and `rational_decay`, alongside existing `exp` and `log`.
- Added `v1.15-geml-oscillatory-smoke` and `v1.15-geml-oscillatory` built-in benchmark suites.
- Added campaign presets `geml-oscillatory-smoke` and `geml-oscillatory`.
- Paired every declared target across raw EML and i*pi EML with matched blind-training budgets, disabled scaffolds, matched datasets, matched constants, and stable operator-family metadata.
- Added fail-closed validation requiring branch-domain declarations for i*pi EML rows in the v1.15 target set.

## Tests

- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_builtin_suite_registry_expands_stable_run_ids tests/test_benchmark_contract.py::test_v115_oscillatory_targets_have_safe_deterministic_splits tests/test_benchmark_contract.py::test_v115_geml_oscillatory_suite_pairs_raw_and_ipi_budgets tests/test_benchmark_contract.py::test_v115_ipi_branch_domain_validation_fails_closed tests/test_campaign.py::test_campaign_presets_map_to_budgeted_suites -q`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py -q`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py::test_runner_filter_executes_subset tests/test_benchmark_runner.py::test_runner_executes_operator_family_smoke_matrix tests/test_benchmark_reports.py -q`
- `PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m compileall -q src tests`
- `git diff --check`

## Outcome

The project now has a branch-safe v1.15 benchmark protocol for natural i*pi EML oscillatory targets and negative controls, ready for Phase 86 paired execution and aggregation.
