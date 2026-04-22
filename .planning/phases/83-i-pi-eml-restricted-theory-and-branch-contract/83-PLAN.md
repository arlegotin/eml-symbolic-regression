# Phase 83 Plan: i*pi EML Restricted Theory and Branch Contract

## Tasks

1. Add principal-log branch diagnostics.
   - Implement reusable branch diagnostic helpers for complex second-slot inputs.
   - Track branch convention, proximity, crossing/hit counts, invalid-domain skips, and failure class.
   - Wire branch summaries into `AnomalyStats`.

2. Expose branch diagnostics in verification.
   - Extend `VerificationReport` serialization with branch diagnostics.
   - Detect branch-related candidate failures without changing recovery semantics.
   - Preserve existing verifier report keys.

3. Add restricted i*pi theory checks.
   - Implement high-precision executable checks for reciprocal and nested recovery identities on `y > 0`.
   - Implement derivative and one-step composition magnitude checks for real-axis assumptions.
   - Generate JSON/Markdown theory artifacts with explicit assumption and non-claim sections.

4. Document and test the contract.
   - Document principal-log branch convention and restricted-identity boundaries.
   - Add tests for branch diagnostics, verifier serialization, and theory artifacts.
   - Confirm existing Phase 82 semantics and nearby verifier tests still pass.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_semantics_expression.py tests/test_verify.py -q`
- New focused Phase 83 theory/branch tests.
- `PYTHONPATH=src python -m compileall -q src`
- `git diff --check`
