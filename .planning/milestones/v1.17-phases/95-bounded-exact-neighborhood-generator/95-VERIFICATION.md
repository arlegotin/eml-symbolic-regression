---
phase: 95
status: passed
verified: 2026-04-22
---

# Phase 95 Verification

## Goal

Generate local exact-tree alternatives around snapped candidates while preserving target-agnostic behavior.

## Must-Have Checks

- One-slot and two-slot alternatives are generated deterministically from low-margin candidate choices: verified by `test_write_v117_neighborhood_candidates_generates_bounded_deterministic_variants`.
- Candidate budgets, ordering, and pruning are source-locked and reproducible: verified by repeated writer output equality and manifest/source-lock outputs.
- Original snapped candidates and fallback candidates remain present with provenance: verified by first two candidate rows `original_snap` and `fallback_snap`.
- Tests reject target leakage surfaces: generated rows include `target_formula_leakage: false` and no `target_tree` field.

## Automated Checks

```bash
python -m pytest tests/test_paper_v117.py -q
```

Result: `5 passed`.

## Human Verification

None required.
