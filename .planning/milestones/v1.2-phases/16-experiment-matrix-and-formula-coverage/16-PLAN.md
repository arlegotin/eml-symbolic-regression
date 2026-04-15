---
phase: 16
subsystem: benchmark-matrix
status: complete
wave: 1
---

# Phase 16 Plan: Experiment Matrix and Formula Coverage

<objective>
Complete the v1.2 benchmark matrix coverage across shallow blind baselines, Beer-Lambert perturbations, Michaelis-Menten/Planck diagnostics, and selected FOR_DEMO formulas.
</objective>

## Tasks

- Add a radioactive-decay demo spec.
- Update built-in benchmark suites with the v1.2 formula/start/seed/perturbation matrix.
- Add tests proving matrix coverage and diagnostic executability.
- Verify benchmark contract and runner tests still pass.

## Verification

- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py`
