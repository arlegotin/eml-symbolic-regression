---
phase: 70
slug: layered-verifier-and-split-isolation
status: complete
created: 2026-04-20
completed: 2026-04-20
workflow: gsd-execute-phase
plan: .planning/phases/70-layered-verifier-and-split-isolation/70-PLAN.md
key_files:
  created: []
  modified:
    - src/eml_symbolic_regression/verify.py
    - src/eml_symbolic_regression/optimize.py
    - tests/test_verify.py
summary_artifact: .planning/phases/70-layered-verifier-and-split-isolation/70-SUMMARY.md
---

# Phase 70 Summary: Layered Verifier and Split Isolation

## Status

Complete. Phase 70 adds layered verifier evidence fields and split-role isolation while preserving existing recovery statuses.

## Delivered

- Added split-role metadata and inference for training, selection, diagnostic, verifier, and final-confirmation splits.
- Added symbolic, dense randomized, adversarial, certificate, evidence-level, and metric-role fields to `VerificationReport.as_dict()`.
- Added deterministic dense/adversarial probe layers using `DataSplit.target_mpmath` when available, with explicit unsupported statuses otherwise.
- Added symbolic equivalence attempts when `target_sympy` is supplied.
- Updated exact-candidate ranking so final-confirmation splits are excluded from selection metrics while still available for full verification reports.
- Added focused tests for symbolic evidence, unsupported layer labels, split-role filtering, and final-confirmation exclusion from ranking.

## Verification Completed

```bash
PYTHONPATH=src python -m pytest tests/test_verify.py -q
```

Result: passed, 7 tests.

```bash
PYTHONPATH=src python -m pytest tests/test_verify.py tests/test_optimizer_cleanup.py tests/test_benchmark_reports.py -q
```

Result: passed, 32 tests with 2 pre-existing numerical warnings from centered-family semantics.

```bash
python -m compileall -q src/eml_symbolic_regression/verify.py src/eml_symbolic_regression/optimize.py
```

Result: passed.

```bash
PYTHONPATH=src python - <<'PY'
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.verify import verify_candidate
spec = get_demo('exp')
splits = spec.make_splits(points=8, seed=0)
report = verify_candidate(spec.candidate, splits, tolerance=1e-8, target_sympy=spec.candidate.to_sympy())
print(report.status, report.symbolic_status, report.dense_random_status, report.adversarial_status, report.certificate_status, report.evidence_level, report.metric_roles)
PY
```

Result: `recovered passed passed passed symbolic_equivalence symbolic {'training': 1, 'selection': 0, 'diagnostic': 2, 'verifier': 0, 'final_confirmation': 0}`.

## Commit

Implementation commit: `788cecb`.

## Notes

Interval/certificate evidence remains conservative: symbolic equivalence reports `symbolic_equivalence`; otherwise the report explicitly labels interval certificates as unsupported. Full interval arithmetic remains future work.
