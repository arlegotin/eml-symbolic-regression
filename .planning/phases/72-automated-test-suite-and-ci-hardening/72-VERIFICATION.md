---
status: passed
verified_at: "2026-04-20"
implementation_commit: 6b34b29
---

# Phase 72: Automated Test Suite and CI Hardening - Verification

## Result

Passed.

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_ci_contract.py tests/test_evidence_regression.py -q
```

Result: 5 passed in 1.28s.

```bash
python scripts/validate-ci-contract.py --mode dev --root .
```

Result: `dev: ok`.

```bash
PYTHONPATH=src python -m pytest tests/test_semantics_expression.py tests/test_master_tree.py tests/test_compiler_warm_start.py tests/test_verify.py tests/test_optimizer_cleanup.py tests/test_benchmark_contract.py tests/test_evidence_regression.py tests/test_publication_rebuild.py tests/test_ci_contract.py -q
```

Result: 153 passed, 4 expected runtime warnings in 58.75s.

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py::test_runner_filter_executes_subset tests/test_verifier_demos_cli.py::test_cli_demo_train_eml_writes_selection_and_fallback_provenance -q
```

Result: 2 passed, 2 expected runtime warnings in 47.12s.

```bash
bash scripts/publication-rebuild.sh
```

Result: passed; wrote and validated `artifacts/paper/v1.13` smoke outputs, which were removed after verification.

```bash
python scripts/validate-ci-contract.py --mode public-snapshot --root "$snapshot"
```

Result: `public-snapshot: ok` after simulating the committed `HEAD` public snapshot with the same private-file and raw-artifact removals used by CI.

```bash
git diff --check
```

Result: passed.

## Acceptance Checks

- `.github/workflows/ci.yml` exists and defines core, integration, publication, and branch-discipline jobs.
- CI job commands ran locally.
- The dev-tree validator passed against the current repository.
- A simulated public snapshot from committed `HEAD` passed validation.
- The evidence regression test writes and validates a training-through-verification artifact.
