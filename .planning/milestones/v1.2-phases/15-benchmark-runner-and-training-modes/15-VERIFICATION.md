status: passed

# Phase 15 Verification

Benchmark suite execution now routes expanded runs through catalog verification, compile diagnostics, blind optimizer training, and compiler warm-start training. Unsupported and failed cases are preserved as structured artifacts.

| Requirement | Status | Evidence |
|-------------|--------|----------|
| RUN-01 | passed | `eml-sr benchmark` / `python -m eml_symbolic_regression.cli benchmark` can run a suite or filtered subset. |
| RUN-02 | passed | `execute_benchmark_run()` routes `blind` runs through `fit_eml_tree()` with per-run seeds and budgets. |
| RUN-03 | passed | `warm_start` runs use compile, embed, perturb, train, snap, and verify via `fit_warm_started_eml_tree()`. |
| RUN-04 | passed | Unsupported compiler/depth outcomes and unexpected errors are serialized as run artifacts without aborting the full suite. |

## Verification Commands

- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py -q` passed with 8 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks` listed all built-in suites.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark smoke --case planck-diagnostic --output-dir /tmp/eml-bench-phase15` wrote an unsupported diagnostic suite result.
