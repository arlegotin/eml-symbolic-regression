---
phase: 18
subsystem: benchmark-lockdown
status: complete
wave: 1
---

# Phase 18 Plan: Smoke Tests, Docs, and Evidence Lockdown

<objective>
Add CI-scale benchmark smoke coverage and documentation that explains how to run and interpret v1.2 evidence reports.
</objective>

## Tasks

- Add smoke test for blind, warm-start, unsupported/stretch, and aggregate reports.
- Update README with benchmark commands and interpretation notes.
- Update implementation docs with benchmark schemas, taxonomy, and limitations.
- Run full pytest suite.

## Verification

- `python -m pytest -q`
