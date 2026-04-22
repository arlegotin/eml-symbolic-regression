# Phase 79 Summary: Baseline Claim Surface Quarantine

## Completed

- Added baseline row fields for `adapter_launch_status`, `fixed_budget_launched`, `main_surface_eligible`, and `claim_surface_policy`.
- Added baseline CSV columns and manifest counts for adapter launch status.
- Added a baseline manifest `claim_surface` policy that defaults to quarantined appendix/future-work context and declares no main-surface comparison claim.
- Reworded the baseline report and README to describe baseline rows as diagnostic scaffolding, not public comparator evidence.
- Extended publication claim audit with baseline quarantine checks and a Markdown section.
- Added a regression test that fails attempted main-surface baseline comparison claims when only unavailable/unsupported rows exist.

## Code Changes

- `src/eml_symbolic_regression/baselines.py`
  - Writes launch/quarantine metadata into JSON, CSV, manifest, and report outputs.
- `src/eml_symbolic_regression/publication.py`
  - Reads baseline rows when available.
  - Checks baseline quarantine fields.
  - Rejects main-surface baseline comparison claims without eligible completed external rows.
- `README.md`
  - Clarifies that baseline harness output is quarantined diagnostic context.
- `tests/test_baseline_harness.py`, `tests/test_publication_rebuild.py`
  - Lock baseline quarantine fields and claim-audit rejection behavior.

## Commits

- `cc7f1f4 docs(79): smart discuss context and plan`
- `87a1098 fix(79): quarantine baseline claim surface`

