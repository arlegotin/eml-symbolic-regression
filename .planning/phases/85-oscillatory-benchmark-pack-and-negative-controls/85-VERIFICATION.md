status: passed

# Phase 85 Verification

## Result

Passed. The benchmark registry now contains branch-safe v1.15 oscillatory and negative-control targets with matched raw EML versus i*pi EML suites.

## Requirements Checked

- **BENCH-01:** Registered periodic and harmonic targets: `sin_pi`, `cos_pi`, and `harmonic_sum`.
- **BENCH-02:** Registered standing-wave coverage through `standing_wave_snapshot` and included existing `damped_oscillator`.
- **BENCH-03:** Registered positive-domain `log_periodic_oscillation`.
- **BENCH-04:** Registered negative controls: existing `exp`, existing `log`, new `quadratic_polynomial`, and new `rational_decay`.
- **BENCH-05:** Added matched raw/i*pi suite and campaign presets with paired datasets, depths, steps, restarts, constants, disabled scaffolds, snapping path, verifier gates, and split policy.
- **Branch fail-closed guard:** i*pi rows in the v1.15 target set must declare `branch_safe_domain`, `branch_safe_by_construction`, or `negative_control_domain`; malformed rows raise `BenchmarkValidationError`.

## Tests

Passed:

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_builtin_suite_registry_expands_stable_run_ids tests/test_benchmark_contract.py::test_v115_oscillatory_targets_have_safe_deterministic_splits tests/test_benchmark_contract.py::test_v115_geml_oscillatory_suite_pairs_raw_and_ipi_budgets tests/test_benchmark_contract.py::test_v115_ipi_branch_domain_validation_fails_closed tests/test_campaign.py::test_campaign_presets_map_to_budgeted_suites -q
# 5 passed in 1.51s

PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py -q
# 90 passed in 24.10s

PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py::test_runner_filter_executes_subset tests/test_benchmark_runner.py::test_runner_executes_operator_family_smoke_matrix tests/test_benchmark_reports.py -q
# 20 passed, 2 warnings in 64.86s

PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_verify.py -q
# 22 passed, 2 warnings in 11.15s

PYTHONPATH=src python -m compileall -q src tests
# passed

git diff --check
# passed
```

Warnings were existing numerical overflow and branch-domain warnings in stress fixtures.
