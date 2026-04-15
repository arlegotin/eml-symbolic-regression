---
phase: 8
subsystem: compiler
status: complete
wave: 1
---

# Phase 8 Plan: Compiler Contract and Direct Rules

<objective>
Implement a fail-closed SymPy-to-EML compiler that produces exact `Expr` ASTs, metadata, and validation evidence.
</objective>

## Tasks

- Add compiler dataclasses, reason codes, and `UnsupportedExpression`.
- Compile allowed symbols, constants, `exp`, and `log` into existing exact AST nodes.
- Add independent SymPy-vs-EML validation helper.
- Expose compiler result serialization for reports.

## Verification

- Unit tests cover direct rules and fail-closed negative cases.
- `python -m pytest`
