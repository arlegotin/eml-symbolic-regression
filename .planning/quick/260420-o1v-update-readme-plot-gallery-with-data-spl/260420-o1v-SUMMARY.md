# Quick Task 260420-o1v: Update README plot gallery with data splits and EML curves - Summary

**Date:** 2026-04-20
**Status:** Complete
**Implementation commit:** `1ba2677`

## Changes

- Regenerated `readme-assets/fit-gallery.svg` as a 12-panel plot over the v1.13 publication targets.
- Removed numeric axis tick labels from the plot.
- Added a plain legend for target line, verified EML curve, training dots, validation triangles, and extrapolation squares.
- Added blue training markers, red held-out validation markers, and black extrapolation markers in each panel.
- Added green dashed EML curves only for targets with at least one recovered row in `group-formula.csv`.
- Updated README copy and alt text to describe the new marker/line semantics.

## Verification

- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- README local-link existence check: `README local links ok`
- SVG element count check: 12 panels, 13 target lines including legend, 9 EML lines including legend, and marker classes present for train/validation/extrapolation.
- Numeric text check: no numeric-only SVG text labels.
- Stale style check: no `tick` class, gradients, filters, shadows, blur, or glow.
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`: `dev: ok`
