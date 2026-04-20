---
status: complete
created: 2026-04-20T16:01:35.084Z
quick_id: 260420-p1b
slug: restyle-readme-plot-gallery-with-status-
---

# Quick Task: Restyle README plot gallery with status labels

## Goal

Update the README target gallery to match the requested visual and evidence framing:

- make the target curve a very light gray reference line;
- remove per-panel frames and use the freed space for larger plots;
- keep spacing readable across the grid;
- label each panel with function name, formula, and whether EML worked under the current evidence rows or failed/was unsupported, including the reason.

## Plan

1. Regenerate `readme-assets/fit-gallery.svg` from current demo specs and campaign table.
2. Update the README plot description and alt text to match the new status labels and lighter target line.
3. Verify SVG parsing, plot counts, status labels, and wording constraints.
4. Commit implementation changes and close the quick task.

## Result

Completed in commit `33e38d6`.

- Removed plot frame rectangles and enlarged plot drawing areas.
- Changed target curves to a pale gray reference line.
- Removed generic unverified EML trial curves.
- Added per-panel `EML: worked` or `EML: failed (...)` labels from the current campaign table.
