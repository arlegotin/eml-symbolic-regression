---
phase: 70
status: passed
verified_at: 2026-04-20
score: 8/8
---

# Phase 70 Verification: Layered Verifier and Split Isolation

## Verdict

Status: `passed`

Phase goal achieved: verifier reports now expose symbolic, dense randomized, adversarial, certificate, evidence-level, and split-role metadata, and candidate ranking excludes final-confirmation splits from selection metrics.

## Must-Have Checks

| Must-have | Result | Evidence |
|-----------|--------|----------|
| Verifier attempts symbolic equivalence before numeric fallback where possible. | passed | `verify_candidate(..., target_sympy=...)` reports `symbolic_status: passed`; unsupported paths report `unsupported_no_target`. |
| Non-symbolic candidates are checked on fresh dense randomized points plus adversarial probes when target evaluators exist. | passed | Dense/adversarial probe layers run from deterministic fresh contexts using `DataSplit.target_mpmath`; tests assert `passed` statuses. |
| Interval/certificate status is reported with unsupported labels. | passed | `certificate_status` is `symbolic_equivalence` for symbolic proof and `unsupported_interval_certificate` otherwise. |
| Candidate ranking uses only allowed selection data and cannot see final confirmation splits. | passed | `selection_candidate_splits` removes `final_confirmation`, and `_select_exact_candidate` uses filtered splits for `selection_metrics`. |
| Artifacts label training, selection, diagnostic, verifier, and final-confirmation metrics. | passed | `SplitResult.role` and `VerificationReport.metric_roles` are included in `as_dict()`. |
| Existing verifier statuses remain backward compatible. | passed | Existing optimizer and benchmark report tests pass. |
| Symbolic zero target is handled correctly. | passed | Regression test covers `target_sympy=0`. |
| Report fields are JSON-friendly. | passed | Existing report serialization tests pass with additive fields. |

## Automated Checks

```bash
PYTHONPATH=src python -m pytest tests/test_verify.py -q
```

Result: passed, 8 tests.

```bash
PYTHONPATH=src python -m pytest tests/test_verify.py tests/test_optimizer_cleanup.py tests/test_benchmark_reports.py -q
```

Result: passed, 33 tests with 2 pre-existing numerical warnings from centered-family semantics.

```bash
python -m compileall -q src/eml_symbolic_regression/verify.py src/eml_symbolic_regression/optimize.py
```

Result: passed.

## Requirement Coverage

- VERIF-01: passed through optional SymPy equivalence attempts.
- VERIF-02: passed through explicit evidence-layer and evidence-level labels.
- VERIF-03: passed through deterministic fresh dense randomized probes.
- VERIF-04: passed through deterministic adversarial boundary/near-boundary probes.
- VERIF-05: passed through certificate status labels, including unsupported status.
- SPLIT-01: passed by excluding final-confirmation splits from ranking metrics.
- SPLIT-02: passed by keeping final-confirmation data out of selection scoring while retaining post-selection verification reporting.
- SPLIT-03: passed through split-role labels and metric role counts.

## Residual Risk

Interval/certificate support is intentionally conservative. Full interval arithmetic remains future work, but unsupported certificate status is now explicit and machine-readable.
