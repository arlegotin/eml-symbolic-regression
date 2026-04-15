---
phase: 14
subsystem: benchmark-contract
status: complete
wave: 1
---

# Phase 14 Plan: Benchmark Contract and Suite Registry

<objective>
Add a deterministic benchmark suite contract with validation, built-in registry, run expansion, and stable artifact identity.
</objective>

## Tasks

- Add benchmark dataclasses and JSON-compatible serialization helpers.
- Add built-in suites for smoke, v1.2 evidence, and FOR_DEMO diagnostics.
- Add validation errors for unknown formulas, bad modes, unsafe budgets, and malformed suite files.
- Add stable run IDs and artifact paths for expanded runs.
- Add focused tests for suite discovery, validation, and run ID stability.

## Verification

- `python -m pytest tests/test_benchmark_contract.py`
