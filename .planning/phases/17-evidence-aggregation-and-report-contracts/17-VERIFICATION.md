status: passed

# Phase 17 Verification

Benchmark runs now emit normalized metrics and aggregate evidence reports in JSON and Markdown.

| Requirement | Status | Evidence |
|-------------|--------|----------|
| EVID-01 | passed | Run artifacts include suite/run identity, formula, dataset, start mode, seed, perturbation, optimizer config, normalized metrics, stage statuses, timing, and errors. |
| EVID-02 | passed | `aggregate_evidence()` and `write_aggregate_reports()` write aggregate JSON and Markdown with recovery rates grouped by formula, start mode, perturbation, depth, and seed group. |
| EVID-03 | passed | `classify_run()` separates blind recovery, same-AST warm-start return, verified-equivalent warm-start recovery, snapped-but-failed, soft-fit-only, unsupported, and execution failure classes. |
| EVID-04 | passed | Reports preserve suite config, run artifact paths, environment summary, and git code version. |

## Verification Commands

- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py -q` passed with 13 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark smoke --case planck-diagnostic --output-dir /tmp/eml-bench-phase17` wrote `suite-result.json`, `aggregate.json`, and `aggregate.md`.
