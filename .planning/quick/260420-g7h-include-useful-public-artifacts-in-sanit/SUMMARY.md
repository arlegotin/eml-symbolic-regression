# Quick Task 260420-g7h: Include Useful Public Artifacts

## Summary

Updated the public branch publishing workflow so `artifacts` is included in the generated `main` snapshot with a curated pruning policy.

## Public Artifact Policy

Kept paper-facing artifacts such as reports, markdown summaries, tables, figures, manifests, source locks, and claim audits.

Removed noisy or oversized artifact classes from `main` only:

- `runs/` and `raw-runs/` raw payload directories
- `suite-result.json` and `*-suite-result.json`
- `aggregate.json` and `*-aggregate.json`
- `training-step-traces.{json,csv,md}`
- duplicated `artifacts/paper/**/sources/**` bundles
- `.DS_Store`

## Files Changed

- `.github/workflows/publish-main.yml`
- `.planning/STATE.md`
- `.planning/quick/260420-g7h-include-useful-public-artifacts-in-sanit/PLAN.md`
- `.planning/quick/260420-g7h-include-useful-public-artifacts-in-sanit/SUMMARY.md`

## Verification

- `git diff --check`
- Dry-run pathspec count: 1,306 tracked artifact files, 559 pruned from `main`, 747 retained for the public snapshot.
- Remote `main` verification is performed after the workflow runs.
