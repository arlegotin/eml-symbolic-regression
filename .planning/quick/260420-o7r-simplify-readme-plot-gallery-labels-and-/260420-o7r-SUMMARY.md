# Quick Task 260420-o7r: Simplify README plot gallery labels and emphasize EML curves - Summary

**Date:** 2026-04-20
**Status:** Complete
**Implementation commit:** `002f65a`

## Changes

- Regenerated `readme-assets/fit-gallery.svg` with no visible plot title, panel labels, formula labels, axis labels, or status labels.
- Kept only the legend text: target, verified EML, training data, and validation data.
- Removed the extrapolation marker series from the plot.
- Updated README plot prose and alt text to remove extrapolation.
- Drew verified EML polylines last in recovered panels and increased the dashed green stroke width.
- Scaled each panel to the train plus held-out validation domain for tighter zoom.

## Verification

- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- Visible SVG text check: only `target`, `verified EML`, `training data`, and `validation data`.
- SVG count check: 12 panels, 13 target lines including legend, 9 EML lines including legend, train/validation markers present, 0 extrapolation matches.
- Verified EML order check: `eml-order-ok panels=8`.
- README local-link existence check: `README local links ok`.
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`: `dev: ok`
