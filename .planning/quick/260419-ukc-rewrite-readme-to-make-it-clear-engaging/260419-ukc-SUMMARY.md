---
quick_id: 260419-ukc
slug: rewrite-readme-to-make-it-clear-engaging
status: complete
created: 2026-04-19
completed: 2026-04-19
workflow: gsd-quick
files_modified:
  - README.md
summary_artifact: .planning/quick/260419-ukc-rewrite-readme-to-make-it-clear-engaging/260419-ukc-SUMMARY.md
---

# Quick Task 260419-ukc Summary: README Rewrite

## Status

README rewrite completed.

The README now presents the project as a verifier-gated hybrid EML symbolic-regression package, with a clearer explanation of EML, the complete depth-bounded tree idea, the optimization/snapping/verification pipeline, installation, concise CLI usage, demo/evidence taxonomy, limits, and repository map.

## Claim Boundaries Preserved

- Training loss alone is not described as recovery.
- Compiler output alone is not described as trained recovery.
- Warm-start, same-AST, scaffolded, repaired, refit, compile-only, verified_showcase, perturbed-basin, and unsupported regimes are kept separate.
- Arrhenius and Michaelis-Menten are described as exact compiler warm-start / same-AST evidence, not blind discovery.
- Planck and logistic remain unsupported/stretch diagnostics unless strict support and verifier contracts pass.
- Repaired candidates remain repair-only evidence.

## Verification Completed

```bash
rg -n "eml\\(x, y\\)|complete depth-bounded|complex128|snapping|verifier|mpmath|claim boundaries" README.md
```

Result: passed.

```bash
rg -n "not blind discovery|training loss alone|same-AST|repaired candidate|unsupported|verifier" README.md
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli --help
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks
```

Result: passed.

## Full Test Suite

```bash
python -m pytest
```

Result: not completed. The run collected 358 tests and reached the benchmark tests before it was stopped. It generated out-of-scope artifact churn under `artifacts/diagnostics/phase31-basin-bound/`, so full verification was halted and should not be counted as completed for this docs-only task.

## Out-of-Scope Churn Observed

The interrupted pytest run modified generated benchmark diagnostics under:

- `artifacts/diagnostics/phase31-basin-bound/`

Those artifact changes are not part of the README rewrite; they were restored/removed and were not committed.

## Commit

README commit: `91b6996`.
