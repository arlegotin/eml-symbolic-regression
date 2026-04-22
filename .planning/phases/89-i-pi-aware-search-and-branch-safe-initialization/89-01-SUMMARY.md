---
phase: 89
plan: 89-01
status: complete
completed: 2026-04-22
---

# Plan 89-01 Summary: i*pi generic initializers and v1.16 suites

## What Changed

- Added `phase_initializers` to optimizer and benchmark budget/config serialization.
- Added generic i*pi primitive initializers `ipi_phase_unit` and `ipi_log_unit`, recorded as `generic_ipi_operator_primitive` with `formula_leakage: false`.
- Added v1.16 benchmark suites: `v1.16-geml-smoke`, `v1.16-geml-pilot`, and `v1.16-geml-full`.
- Added campaign presets: `geml-v116-smoke`, `geml-v116-pilot`, and `geml-v116-full`.
- Added regression tests for initializer provenance, branch-safe suite metadata, raw budget compatibility, and preset registration.

## Verification

- `python -m pytest tests/test_optimizer_cleanup.py::test_optimizer_uses_generic_ipi_phase_initializer_without_formula_leakage tests/test_optimizer_cleanup.py::test_optimizer_runs_ipi_eml_with_branch_and_snap_metadata tests/test_benchmark_contract.py::test_v115_geml_oscillatory_suite_pairs_raw_and_ipi_budgets tests/test_benchmark_contract.py::test_v116_geml_suites_use_generic_ipi_initializers_and_match_raw_budgets tests/test_benchmark_contract.py::test_phase_initializers_fail_closed_for_raw_operator tests/test_campaign.py::test_campaign_presets_map_to_budgeted_suites -q` passed with 6 tests.

## Key Files

- `src/eml_symbolic_regression/optimize.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/campaign.py`
- `tests/test_optimizer_cleanup.py`
- `tests/test_benchmark_contract.py`
- `tests/test_campaign.py`
