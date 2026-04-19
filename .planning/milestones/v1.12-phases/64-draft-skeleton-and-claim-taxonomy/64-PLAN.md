# Phase 64: Draft Skeleton and Claim Taxonomy - Plan

**Created:** 2026-04-19  
**Status:** Ready for execution

## Goal

Convert the v1.11 package into the first paper-shaped draft scaffold with claim boundaries visible from the start.

## Tasks

1. Add a reproducible draft generator that writes `artifacts/paper/v1.11/draft/`.
2. Generate `abstract.md`, `methods.md`, `results.md`, and `limitations.md` from the existing v1.11 evidence package.
3. Generate `claim-taxonomy.json`, `claim-taxonomy.csv`, and `claim-taxonomy.md` with denominator eligibility and safe claim language.
4. Add CLI wiring for the draft generator.
5. Add regression tests for generated draft files, taxonomy rows, and logistic/Planck unsupported language.
6. Run focused tests and generate the draft artifacts.

## Verification

- Draft files exist under `artifacts/paper/v1.11/draft/`.
- Taxonomy includes pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed rows.
- Draft text references v1.11 sources and does not promote logistic or Planck.
- CLI command works from the repo root with `PYTHONPATH=src`.

## Risks

- The draft should be paper-shaped but not overpolished; full manuscript prose is out of scope.
- Taxonomy wording must stay conservative because later phases will reuse it in audit checks.
