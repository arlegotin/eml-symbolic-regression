---
phase: 9
subsystem: master-tree
status: complete
wave: 1
---

# Phase 9 Plan: Constant Catalog and AST Embedding

<objective>
Extend `SoftEMLTree` with finite constant catalogs and add exact AST embedding with snap round-trip diagnostics.
</objective>

## Tasks

- Add normalized constant terminal banks while keeping default `const:1`.
- Update soft evaluation and snapping for literal constants.
- Add embedding dataclasses and diagnostics.
- Test Beer-Lambert compile-to-embed round trip and missing-terminal errors.

## Verification

- `python -m pytest`
