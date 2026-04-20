---
status: complete
task_id: 260420-ng7
completed: 2026-04-20
commit: 38cc14f
---

# Quick Task 260420-ng7: Update README with v1.13 release evidence and plots - Summary

## What Changed

- Added a `Current Release Evidence` section to `README.md`.
- Added v1.13 headline numbers:
  - 24 paper-track rows,
  - 9 verifier-recovered rows,
  - 15 unsupported rows,
  - 0 failed rows,
  - separate basis-only and literal-constant denominators.
- Embedded four committed SVG plots from `artifacts/campaigns/v1.13-paper-tracks-final/figures/`.
- Added links to v1.13 manifest, claim audit, release gate, reproduction notes, campaign tables, baseline report, and dataset manifests.
- Added quick-start commands for the paper-track campaign, publication rebuild, expanded datasets, and baseline harness.

## Verification

- `git diff --check` passed.
- README local artifact links were checked and all referenced local paths exist.
- `python scripts/validate-ci-contract.py --mode dev --root .` passed.

## Commit

- `38cc14f docs(readme): add v1.13 release evidence plots`
