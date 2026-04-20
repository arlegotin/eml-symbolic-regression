# Quick Task 260420-nuw: Simplify README release narrative and replace plot gallery - Summary

**Date:** 2026-04-20
**Status:** Complete
**Implementation commits:** `18aedfb`, `6d289c4`

## Changes

- Replaced the `Current Release Evidence` table and chart with a short narrative.
- Removed the now-unused `readme-assets/v113-evidence-summary.svg` chart asset.
- Replaced `readme-assets/fit-gallery.svg` with a conservative 12-panel target-function figure.
- Generated the replacement plot from `demo_specs()` and `artifacts/campaigns/v1.13-paper-tracks-final/tables/group-formula.csv`.
- Removed old plot jargon from the visible plot labels: no `verified recovery`, no `same-AST return`, no white sample dots, no smoothing curves.

## Verification

- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- README local-link existence check: `README local links ok`
- Stale reference check: no matches for removed chart names, old plot labels, circle/path/dash/glossy SVG elements.
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`: `dev: ok`
