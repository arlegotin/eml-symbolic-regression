---
status: complete
completed: 2026-04-20T15:56:34Z
quick_id: 260420-oth
slug: show-unverified-eml-trial-curves-and-fun
implementation_commit: d5cf72b
---

# Summary

Updated the README plot gallery so missing verified EML curves are replaced by a separate gray unverified EML trial curve.

## Changes

- Added function-name labels beside each panel formula.
- Kept green dashed curves only for targets with recovered evidence rows.
- Added gray dotted fixed exact EML trial curves for targets without verified recovered rows.
- Updated README text and alt text to state that gray curves are not recovery claims.

## Verification

- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- `rg -n "v1\.13|release|Release|publication|Publication|extrapolated|same-AST|verified recovery" README.md readme-assets/fit-gallery.svg` returned no matches.
- Custom SVG count and ordering checks passed: 12 panels, 12 function labels, 12 formula labels, 24 axis labels, 8 recovered panels, 4 unverified-trial panels.
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`
