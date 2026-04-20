# Phase 70 Research: Layered Verifier and Split Isolation

## RESEARCH COMPLETE

## Current State

`verify.py` currently verifies candidates over supplied splits with NumPy and selected mpmath points. It returns status, per-split numeric errors, high-precision max error, and a high-precision status. It does not label symbolic equivalence, dense randomized checks, adversarial probes, certificate/interval status, or metric roles.

`optimize.py` currently uses all provided `verification_splits` when ranking exact candidates. That is good for verifier-owned candidate selection but unsafe once final-confirmation splits exist, because the ranking key can include held-out/extrapolation/future final-confirmation errors.

## Implementation Notes

- Additive verifier fields are safest because many tests and artifacts already consume `VerificationReport.as_dict()`.
- Symbolic equivalence can be implemented with SymPy only when the caller supplies `target_sympy`; otherwise status should be `unsupported_no_target`.
- Dense/adversarial probes need a callable target. Existing `DataSplit.target_mpmath` is the right hook. If absent, report `unsupported_no_target_evaluator`.
- For deterministic probes, use a local NumPy random generator with a fixed seed. Do not reuse training arrays.
- For split isolation, final-confirmation splits should be filtered out before ranking exact candidates. Full verifier reports can still include final-confirmation splits after candidate choice.

## Recommended Plan

1. Extend `DataSplit`, `SplitResult`, and `VerificationReport` with role/evidence metadata.
2. Add symbolic, dense randomized, adversarial, certificate, and split-role helpers in `verify.py`.
3. Update `_select_exact_candidate` in `optimize.py` so ranking uses only selection-allowed splits while full verification reports can still include final-confirmation splits.
4. Add tests for symbolic evidence, unsupported evidence labels, fresh probe results, and final-confirmation exclusion.

## Risks

- Overly strict symbolic simplification could make valid candidates fail due to SymPy branch complexity. Treat symbolic evidence as one layer, not the only pass condition.
- Dense/adversarial probes without target evaluators should be unsupported, not failed.
- Existing benchmark outputs will gain fields; keep old top-level status and split result keys stable.
