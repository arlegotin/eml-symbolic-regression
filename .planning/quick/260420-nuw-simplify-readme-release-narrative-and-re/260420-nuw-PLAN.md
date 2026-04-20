# Quick Task 260420-nuw: Simplify README release narrative and replace plot gallery - Plan

**Date:** 2026-04-20
**Status:** Complete

## Goal

Make the README evidence section clearer and less chart-heavy, then replace the fit gallery with a conservative plot of every v1.13 publication target.

## Tasks

1. Replace the `Current Release Evidence` table and chart with brief prose.
2. Remove the now-unused README evidence-summary SVG.
3. Replace `readme-assets/fit-gallery.svg` with a simple all-target figure generated from `demo_specs()` and `group-formula.csv`.
4. Verify README links, SVG validity, stale references, and repo dev contract.

## Verification

- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- README local-link existence check
- stale README reference check
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`
