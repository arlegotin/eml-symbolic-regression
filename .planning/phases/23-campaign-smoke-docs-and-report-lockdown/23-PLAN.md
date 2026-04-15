# Phase 23: Campaign Smoke, Docs, and Report Lockdown - Plan

status: planned

## Goal

Users can trust the campaign/report workflow and understand how to present the results honestly.

## Tasks

- Add CLI smoke coverage for the `campaign` command.
- Update README and implementation documentation.
- Generate and commit `artifacts/campaigns/v1.3-smoke/`.
- Run full pytest.
- Record final verification and phase summary.

## Verification

- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign smoke --output-root artifacts/campaigns --label v1.3-smoke --overwrite`
- `python -m pytest -q`
