# Quick Task 260420-oij: Remove README release framing and label plot panels - Plan

**Date:** 2026-04-20
**Status:** Complete

## Goal

Make the README speak about the current repository state and results directly, with no release or version framing, and label each plot panel by function.

## Tasks

1. Replace release/version language in README with current evidence narrative.
2. Remove versioned commands and artifact paths from README examples.
3. Regenerate `readme-assets/fit-gallery.svg` with formula labels per panel.
4. Keep the plot minimal: legend plus function labels and axis names, no numeric axis values, no status labels, no extrapolation series.
5. Verify README has no version/release framing and SVG remains valid.

## Verification

- `rg -n "v1\\.13|release|Release" README.md readme-assets/fit-gallery.svg`
- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- README local-link existence check
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`
