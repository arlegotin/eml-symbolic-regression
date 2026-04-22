# Phase 80 Context: Multivariate Verifier Target Matching

## Goal

High-precision verifier fallback must map a sampled context to the correct target row for multivariate splits. It must not select targets by the first input variable alone.

## Relevant Requirements

- VER-01: Multivariate splits without `target_mpmath` no longer match scalar targets using only the first input variable.
- VER-02: The verifier either requires `target_mpmath` for multivariate high-precision checks or uses a stable full-row key.
- VER-03: Tests cover repeated first-coordinate rows with different remaining coordinates and target values.
- VER-04: Existing univariate verifier tests and behavior remain unchanged.

## Current State

- `DataSplit.sample_mpmath_contexts()` samples full per-row contexts.
- `_target_scalar_from_split()` uses `target_mpmath` when available.
- Without `target_mpmath`, `_target_scalar_from_split()` currently finds the first row whose first input variable matches the context. That is correct only for univariate splits or multivariate splits with unique first coordinates.

## Constraints

- Preserve existing univariate fallback behavior.
- Prefer full-row lookup over requiring `target_mpmath`, because sampled contexts already originate from split rows.
- Keep this as a verifier fix only; no optimizer or dataset-generation changes.

