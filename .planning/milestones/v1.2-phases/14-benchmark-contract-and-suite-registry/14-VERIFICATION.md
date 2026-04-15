status: passed

# Phase 14 Verification

Benchmark suite contracts are implemented and covered by focused tests.

| Requirement | Status | Evidence |
|-------------|--------|----------|
| BENC-01 | passed | `BenchmarkSuite`, `BenchmarkCase`, `DatasetConfig`, and `OptimizerBudget` define suite formula IDs, datasets, start modes, seeds, perturbations, budgets, verifier tolerance, and artifact roots. |
| BENC-02 | passed | `list_builtin_suites()` and `builtin_suite()` expose `smoke`, `v1.2-evidence`, and `for-demo-diagnostics`. |
| BENC-03 | passed | `BenchmarkValidationError` fail-closes unknown formulas, invalid modes, bad budgets, unsafe perturbations, duplicate cases, malformed suites, and missing suite paths. |
| BENC-04 | passed | `BenchmarkRun.run_id` hashes canonical run identity and writes deterministic artifact paths under the suite artifact root. |

## Verification Command

- `python -m pytest tests/test_benchmark_contract.py -q` passed with 5 tests.
