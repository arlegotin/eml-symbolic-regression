---
status: passed
verified_at: "2026-04-21"
implementation_commit: 2ab6890
---

# Phase 77: Two-Axis Recovery Accounting and Headline Rebuild - Verification

## Result

Passed.

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_reports.py tests/test_campaign.py tests/test_publication_rebuild.py -q
```

Result: 46 passed.

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py::test_v113_basis_only_compile_fails_closed_on_literal_coefficients tests/test_benchmark_reports.py tests/test_campaign.py tests/test_publication_rebuild.py -q
```

Result: 47 passed.

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py tests/test_benchmark_contract.py tests/test_proof_contract.py tests/test_baseline_harness.py tests/test_publication_rebuild.py tests/test_campaign.py -q
```

Result: 141 passed, 3 warnings in 226.81s. The warnings are existing numerical overflow warnings in benchmark tests.

```bash
PYTHONPATH=src python -m compileall -q src/eml_symbolic_regression/benchmark.py src/eml_symbolic_regression/campaign.py src/eml_symbolic_regression/publication.py
```

Result: passed.

```bash
git diff --check
```

Result: passed.

## Acceptance Checks

- Paper-track aggregate logic reports trained exact recovery separately from compile-only support.
- Compile-only verified rows remain verification-passed support but are not trained recoveries.
- Claim audit rejects compile-only rows promoted into trained recovery.
- Existing smoke campaign, publication rebuild, proof contract, benchmark contract, and baseline harness tests pass.
