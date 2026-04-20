# Quick Task 260420-ixp: Return Tests to Main

## Summary

Updated the public branch publishing workflow so `tests` is included in the generated `main` snapshot.

## Files Changed

- `.github/workflows/publish-main.yml`
- `.planning/STATE.md`
- `.planning/quick/260420-ixp-return-tests-to-generated-main-branch/PLAN.md`
- `.planning/quick/260420-ixp-return-tests-to-generated-main-branch/SUMMARY.md`

## Verification

- `git diff --check`
- Local source branch has 28 tracked files under `tests`.
- Remote `main` verification is performed after the workflow runs.
