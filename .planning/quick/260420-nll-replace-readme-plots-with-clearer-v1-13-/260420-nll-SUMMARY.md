# Quick Task 260420-nll: Replace README plots with clearer v1.13 evidence and fit visuals - Summary

**Date:** 2026-04-20
**Status:** Complete
**Implementation commit:** `f0a78ad`

## Changes

- Removed the confusing report-derived README chart embeds for recovery by formula, recovery by start mode, failure taxonomy, and snap-loss comparison.
- Added `readme-assets/v113-evidence-summary.svg`, a README-specific denominator-first summary of the v1.13 release evidence.
- Replaced `readme-assets/fit-gallery.svg` with a current 2x2 gallery that separates verified overlays from unsupported targets.
- Updated README copy and image alt text so unsupported examples are not presented as recovered candidates.

## Verification

- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- `python -m xml.etree.ElementTree readme-assets/v113-evidence-summary.svg`
- `git diff --check`
- README local-link existence check: `README local links ok`
- README stale-chart reference check: no matches for removed chart names.
- `python scripts/validate-ci-contract.py --mode dev --root .`: `dev: ok`
