# Phase 80 Plan: Multivariate Verifier Target Matching

## Tasks

1. Replace first-variable fallback lookup.
   - Match sampled contexts against all input arrays.
   - Return the target only when the full input row identifies an unambiguous target.
   - Preserve `target_mpmath` priority.

2. Add regression tests.
   - Build a multivariate split with repeated first coordinates and different second coordinates/targets.
   - Verify that high-precision fallback passes for the correct candidate.
   - Keep existing univariate verifier tests passing.

3. Verify.
   - Run verifier-focused tests.
   - Compile `verify.py`.
   - Run `git diff --check`.

