# Phase 81 Plan: Corrected Evidence Rebuild and Claim Audit

## Tasks

1. Route corrected publication output to v1.14.
   - Update CLI/script defaults to `artifacts/paper/v1.14`.
   - Keep v1.13 artifact paths untouched.
   - Place linked campaign, baseline, and dataset outputs under the corrected package.

2. Refresh public wording.
   - Update README headline copy to separate trained exact recoveries from compile-only verified support.
   - Point users at the corrected v1.14 package and keep historical v1.13 inspectable.

3. Run the corrected rebuild.
   - Execute the publication rebuild with `--output-dir artifacts/paper/v1.14 --overwrite --allow-dirty`.
   - Verify claim audit and release gate pass.
   - Confirm aggregate/report artifacts have corrected fields and no stale 9-row recovered headline.

4. Add/adjust regression tests.
   - Lock v1.14 output routing so linked evidence does not overwrite top-level historical v1.13 artifacts.
   - Lock README/rebuild command defaults where appropriate.

## Verification

- Run focused publication rebuild tests.
- Run the corrected publication rebuild command.
- Run claim-audit/release-gate validation checks.
- Run compile checks and `git diff --check`.

