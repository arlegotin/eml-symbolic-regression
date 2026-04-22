# Phase 81 Summary: Corrected Evidence Rebuild and Claim Audit

## Status

Complete.

## Commits

- `e683c61` - `docs(81): smart discuss context and plan`
- `5b2b75c` - `fix(81): route corrected publication rebuild`
- `d2988de` - `fix(81): validate sanitized public snapshot`
- `c69cb04` - `docs(81): add corrected v1.14 evidence package`

## Delivered

- Routed corrected publication rebuild defaults from historical `artifacts/paper/v1.13` to `artifacts/paper/v1.14`.
- Kept the historical v1.13 root mapping intact while placing v1.14 linked artifacts under `artifacts/paper/v1.14/linked-artifacts/`.
- Updated CLI and script defaults to write the corrected package.
- Updated README current-evidence wording to separate:
  - 8 trained exact recoveries,
  - 1 compile-only verified support row,
  - 15 unsupported rows,
  - 0 failed rows.
- Fixed the synthetic public snapshot release-gate validation to use the same sanitized contract as CI: `pyproject.toml`, `README.md`, `src`, and `tests`, with private workflows omitted.
- Regenerated and committed the corrected v1.14 evidence package at `artifacts/paper/v1.14/`.
- Pruned the redundant publication-track `suite-result.json` snapshot from the committed package because it duplicates smaller aggregate/table/raw-run evidence and exceeds GitHub's 100 MB file limit.

## Evidence Package

- Manifest: `artifacts/paper/v1.14/manifest.json`
- Claim audit: `artifacts/paper/v1.14/claim-audit.json`
- Release gate: `artifacts/paper/v1.14/release-gate.json`
- Linked campaign artifacts: `artifacts/paper/v1.14/linked-artifacts/campaigns/v1.14-corrected-paper-tracks/`

## Outcome

The corrected package claim audit and release gate both pass. The package excludes compile-only verified support from trained recovery counts, preserves baseline quarantine fields, and no longer uses the stale 9-row recovered headline on the current publication surface.
