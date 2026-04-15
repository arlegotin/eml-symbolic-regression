---
phase: 10
subsystem: compiler
status: complete
wave: 1
---

# Phase 10 Plan: Arithmetic Rule Corpus and Depth Gates

<objective>
Implement arithmetic EML templates for addition, subtraction, negation, multiplication, division, reciprocal, and small integer powers.
</objective>

## Tasks

- Add verified EML helper templates.
- Compile SymPy `Add`, `Mul`, and `Pow`.
- Enforce `max_power`, `max_depth`, and `max_nodes`.
- Add tests for arithmetic validation and budget failures.

## Verification

- `python -m pytest`
