---
phase: 15
subsystem: benchmark-runner
status: complete
wave: 1
---

# Phase 15 Plan: Benchmark Runner and Training Modes

<objective>
Run benchmark suites through existing catalog, compile, blind training, and warm-start training paths while preserving every run outcome.
</objective>

## Tasks

- Add run execution functions and result artifacts to `benchmark.py`.
- Add filtering for formula, start mode, case ID, and seed.
- Add CLI commands for listing and running benchmark suites.
- Add tests for catalog/compile/blind/warm-start execution and unsupported-case preservation.

## Verification

- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py`
