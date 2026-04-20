---
status: complete
created: 2026-04-20T15:52:10.944Z
quick_id: 260420-oth
slug: show-unverified-eml-trial-curves-and-fun
---

# Quick Task: Show unverified EML trial curves and function names in README plots

## Goal

Update the README plot gallery so every panel has an EML-related curve without overstating the evidence:

- keep green dashed curves for verified recovered EML rows;
- add a separately styled and labeled unverified EML trial curve where no verified curve exists;
- label each panel with the function name and formula;
- keep axes labeled while leaving numeric axis values hidden;
- keep the plotting style plain and academic.

## Plan

1. Regenerate `readme-assets/fit-gallery.svg` from the current demo target set.
2. Update `README.md` plot description and alt text to explain verified versus unverified curves.
3. Validate SVG parsing, README wording constraints, plot element counts, and repo checks.
4. Commit code/docs changes and GSD task artifacts separately.

## Result

Completed in commit `d5cf72b`.

- `README.md` now explains verified EML curves versus fixed unverified EML trial curves.
- `readme-assets/fit-gallery.svg` now labels every panel with function name and formula.
- Every panel has either a green verified EML curve or a gray fixed exact EML trial curve.
