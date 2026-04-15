---
phase: 12
plan: 12-PLAN
subsystem: cli
tags: [demos, reporting, cli]
duration: same-session
completed: 2026-04-15
requirements-completed: [DEMO-05, DEMO-06, DEMO-07, DEMO-08]
---

# Phase 12 Summary

CLI reports now separate catalog showcase, compiled seed, blind baseline, warm-start attempt, and trained exact recovery. Beer-Lambert promotes through verified warm-start recovery; Michaelis-Menten and Planck default to unsupported depth diagnostics.

## Changed Files

- `src/eml_symbolic_regression/cli.py`
- `artifacts/beer-lambert-warm-report.json`
- `artifacts/michaelis-menten-warm-report.json`
- `artifacts/planck-warm-report.json`
- `tests/test_compiler_warm_start.py`

## Verification

- `PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml --points 80 --output artifacts/beer-lambert-warm-report.json`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli demo michaelis_menten --warm-start-eml --points 80 --output artifacts/michaelis-menten-warm-report.json`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli demo planck --warm-start-eml --points 80 --output artifacts/planck-warm-report.json`
- `python -m pytest` passed.
