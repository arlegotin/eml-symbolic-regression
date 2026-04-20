# Quick Task 260420-p9c: Hide GitHub Workflows from Main

## Summary

Updated the public branch publisher so generated `main` removes the full `.github` tree while keeping workflows on `dev`.

Also changed the generated public commit message to `Update`.

The workflow's visible Actions label is now `Publish main`.

The CI branch/snapshot contract now validates the hidden `.github` policy.

## Files Changed

- `.github/workflows/publish-main.yml`
- `.github/workflows/ci.yml`
- `scripts/validate-ci-contract.py`
- `.planning/STATE.md`
- `.planning/quick/260420-p9c-hide-github-workflows-from-generated-mai/PLAN.md`
- `.planning/quick/260420-p9c-hide-github-workflows-from-generated-mai/SUMMARY.md`

## Verification

- `git diff --check`
- `python scripts/validate-ci-contract.py --mode dev --root .`
- `python -m pytest tests/test_ci_contract.py -q`
- Simulated public snapshot validates with `.github` removed.
- Remote publish and CI verification run after push.
