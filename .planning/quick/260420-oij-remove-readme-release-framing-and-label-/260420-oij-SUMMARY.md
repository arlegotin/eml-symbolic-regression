# Quick Task 260420-oij: Remove README release framing and label plot panels - Summary

**Date:** 2026-04-20
**Status:** Complete
**Implementation commit:** `431edef`

## Changes

- Rewrote README evidence prose around the current checked-in results instead of release/version framing.
- Removed versioned artifact paths and versioned command examples from README.
- Renamed the plot section to `Target Curves And Data`.
- Regenerated `readme-assets/fit-gallery.svg` with 12 formula labels and x/y or t/y axis labels.
- Kept the plot free of numeric tick values, status labels, and extrapolation markers.
- Kept verified EML curves drawn after the black target curves.

## Verification

- `rg -n "v1\\.13|release|Release|publication|Publication" README.md readme-assets/fit-gallery.svg`: no matches.
- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- SVG label check: 12 formula labels and 24 axis labels.
- Verified EML order check: `eml-order-ok panels=8`.
- README local-link existence check: `README local links ok`.
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`: `dev: ok`
