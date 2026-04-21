# Phase 79 Context: Baseline Claim Surface Quarantine

## Goal

Baseline scaffolding should remain useful as reproducibility context, but unavailable, unsupported, or denominator-excluded baseline rows must not carry public comparison weight.

## Relevant Requirements

- BASE-01: Main README, report, and paper-facing summaries do not use unavailable, unsupported, or denominator-excluded baseline rows as contextual comparison evidence.
- BASE-02: Baseline artifacts expose dependency status, denominator policy, unsupported reasons, and whether each adapter actually launched a fixed-budget run.
- BASE-03: Unavailable or unsupported external adapters are quarantined to appendix, scaffolding, or future-work language.
- BASE-04: Claim-audit checks reject main-surface baseline comparison language unless fixed-budget external rows completed on the same target set and split contract.

## Current State

- The baseline harness already writes dependency locks, per-row status, reasons, and denominator policy.
- CSV rows expose `dependency_status` and `denominator_policy`, but not a direct launch status or fixed-budget-launched boolean.
- The publication claim audit only checks that baseline context exists and is denominator-excluded.
- README exposes the baseline command but does not explicitly say those rows are quarantined diagnostics rather than comparison claims.

## Constraints

- Do not install or run optional external dependencies.
- Do not promote local polynomial or EML-reference rows into public comparator claims.
- Keep the current baseline harness useful for future matched external runs.
- Preserve existing baseline output schema compatibility by adding fields rather than renaming existing fields.

