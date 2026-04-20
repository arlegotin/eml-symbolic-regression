---
status: complete
completed: 2026-04-20T16:05:03Z
quick_id: 260420-p1b
slug: restyle-readme-plot-gallery-with-status-
implementation_commit: 33e38d6
---

# Summary

Restyled the README plot gallery and added current EML evidence status labels.

## Changes

- Removed per-plot frame rectangles.
- Enlarged the plot regions within the same three-column grid.
- Made target curves pale gray.
- Removed generic unverified EML trial curves.
- Added `EML: worked` labels for recovered targets.
- Added `EML: failed (...)` labels for unrecovered targets, using reasons from the checked-in campaign table.

## Verification

- `python -m xml.etree.ElementTree readme-assets/fit-gallery.svg`
- `rg -n "v1\.13|release|Release|publication|Publication|extrapolated|same-AST|verified recovery|unverified" README.md readme-assets/fit-gallery.svg` returned no matches.
- Custom SVG count checks passed: 0 frame rectangles, 12 function labels, 12 formula labels, 8 worked labels, 4 failed labels, 24 axis labels, 8 recovered EML curves.
- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`
