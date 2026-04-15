---
phase: 12
subsystem: cli
status: complete
wave: 1
---

# Phase 12 Plan: Demo Promotion and Claim Reporting

<objective>
Add CLI flags and report fields for compile-only and compiler warm-start demos with honest stage statuses.
</objective>

## Tasks

- Add `--compile-eml` and `--warm-start-eml`.
- Add compiler/warm-start budget flags.
- Write stage statuses into demo reports.
- Generate Beer-Lambert, Michaelis-Menten, and Planck warm-start artifacts.

## Verification

- CLI smoke tests and `python -m pytest`.
