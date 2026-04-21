# Phase 79 Plan: Baseline Claim Surface Quarantine

## Tasks

1. Add explicit baseline launch/quarantine fields.
   - Add `adapter_launch_status`, `fixed_budget_launched`, and `main_surface_eligible` to baseline rows and CSV.
   - Summarize launch status and claim-surface policy in the baseline manifest.
   - Render the baseline report as diagnostic/future-work context.

2. Tighten publication claim audit.
   - Load baseline rows when available and verify quarantine fields are present.
   - Fail if a manifest declares main-surface comparison claims without completed fixed-budget external rows.
   - Surface baseline quarantine details in claim-audit JSON/Markdown.

3. Update public wording.
   - Clarify README baseline harness language as quarantined diagnostics.
   - Avoid using unavailable/unsupported baseline rows as comparison evidence.

4. Add regression tests.
   - Baseline harness rows and CSV expose launch/quarantine fields.
   - Baseline report says unavailable/missing adapters are future-work context.
   - Claim audit rejects attempted main-surface comparison claims without eligible completed external rows.

## Verification

- Run focused baseline and publication rebuild tests.
- Run compile checks for touched modules.
- Run `git diff --check`.

