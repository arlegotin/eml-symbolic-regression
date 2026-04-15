---
phase: 16
plan: 16-PLAN
subsystem: benchmark-matrix
tags: [benchmarks, formulas, evidence]
duration: same-session
completed: 2026-04-15
requirements-completed: [MATR-01, MATR-02, MATR-03, MATR-04]
---

# Phase 16 Summary

Added `radioactive_decay` as a named demo formula and expanded built-in benchmark suites to cover shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten warm diagnostics, Planck stretch diagnostics, and selected FOR_DEMO formulas.

## Changed Files

- `src/eml_symbolic_regression/datasets.py`
- `src/eml_symbolic_regression/benchmark.py`
- `tests/test_benchmark_contract.py`
- `tests/test_benchmark_runner.py`

## Verification

- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py -q` passed with 10 tests.
- CLI demo listing includes `radioactive_decay`.
