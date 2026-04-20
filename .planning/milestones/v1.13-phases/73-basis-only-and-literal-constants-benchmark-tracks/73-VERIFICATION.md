---
status: passed
verified_at: "2026-04-20"
implementation_commit: 994dbaf
---

# Phase 73: Basis-Only and Literal-Constants Benchmark Tracks - Verification

## Result

Passed.

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_campaign.py -q
```

Result: 104 passed in 29.81s.

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py::test_v113_basis_only_compile_fails_closed_on_literal_coefficients tests/test_benchmark_runner.py::test_logistic_v110_compile_benchmark_records_improved_unsupported_diagnostic tests/test_benchmark_runner.py::test_planck_v110_compile_benchmark_records_improved_unsupported_diagnostic -q
```

Result: 3 passed in 1.26s.

```bash
PYTHONPATH=src python -m pytest tests/test_verifier_demos_cli.py::test_cli_benchmark_writes_v110_focused_campaign_artifacts tests/test_benchmark_runner.py::test_cli_benchmark_writes_suite_result -q
```

Result: 2 passed in 4.41s.

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py tests/test_verifier_demos_cli.py -q
```

Result: 149 passed, 3 expected runtime warnings in 276.22s. This broader run completed before the final additive `benchmark_track.warm_start_status` field was added; the focused serialization/report/runner tests above were rerun afterward.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks
```

Result: listed `v1.13-paper-basis-only`, `v1.13-paper-literal-constants`, and `v1.13-paper-tracks`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-campaigns
```

Result: listed `paper-tracks`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.13-paper-tracks --case exp-literal-warm --seed 0 --output-dir /tmp/eml-phase73-tracks-literal
```

Result: 1 run, 0 unsupported, 0 failed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.13-paper-tracks --case beer-lambert-basis-only-compile --seed 0 --output-dir /tmp/eml-phase73-tracks-basis
```

Result: 1 run, 1 unsupported, 0 failed; the row failed closed under `basis_only` due to the literal coefficient.

```bash
git diff --check
```

Result: passed.

## Acceptance Checks

- Every publication target has basis-only and literal-constant configurations.
- Basis-only rows cannot silently use literal constants.
- Literal rows declare constants policy, literal catalog, warm-start status, and scaffold status.
- Mixed-track aggregate reports expose separate denominators.
- Existing benchmark and campaign contracts still pass.
