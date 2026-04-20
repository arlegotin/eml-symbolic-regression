---
status: passed
verified_at: "2026-04-20"
implementation_commit: b7f32ce
---

# Phase 75: Matched Conventional Baseline Harness - Verification

## Result

Passed.

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_baseline_harness.py -q
```

Result: 3 passed in 1.23s.

```bash
PYTHONPATH=src python -m pytest tests/test_baseline_harness.py tests/test_expanded_datasets.py tests/test_proof_dataset_manifest.py -q
```

Result: 25 passed in 2.34s.

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_cli_parses_semantics_mode_for_demo_and_benchmark tests/test_baseline_harness.py -q
```

Result: 4 passed in 1.16s.

```bash
PYTHONPATH=src python -m pytest tests/test_baseline_harness.py tests/test_expanded_datasets.py tests/test_proof_dataset_manifest.py tests/test_benchmark_contract.py::test_cli_parses_semantics_mode_for_demo_and_benchmark -q
```

Result: 26 passed in 2.47s.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli baseline-harness --dataset unit_aware_ohm_law --adapter eml_reference --adapter polynomial_least_squares --adapter pysr --constants-policy literal_constants --start-condition blind --start-condition warm_start --points 12 --output-dir /tmp/eml-phase75-baseline-smoke --overwrite
```

Result: wrote manifest, rows JSON/CSV, report Markdown, and dependency locks.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli baseline-harness --output-dir /tmp/eml-phase75-baseline-default --overwrite
```

Result: wrote the default 80-row harness matrix with 10 completed rows, 40 unavailable external rows, and 30 unsupported condition rows.

```bash
git diff --check
```

Result: passed.

## Acceptance Checks

- EML and conventional symbolic rows share dataset manifests, seeds, constants policies, start conditions, and budget fields.
- The polynomial conventional baseline completes and records final-confirmation metrics.
- Missing optional external SR adapters fail closed as `unavailable`.
- Dependency/source locks are written.
- Baseline comparison rows are excluded from EML recovery denominators.
- CLI writes the full baseline harness artifact bundle.
