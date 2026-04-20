# Phase 76: Full Evidence Rebuild, Claim Audit, and Public Main Sync - Summary

**Completed:** 2026-04-20
**Status:** Complete
**Implementation commit:** `2dbe429`
**Evidence commit:** `31006ac`

## What Changed

- Extended publication rebuild full mode so `publication-rebuild` now generates:
  - paper-track campaign evidence,
  - matched baseline context,
  - expanded dataset manifests,
  - root publication manifest and source locks,
  - claim audit JSON/Markdown,
  - release gate JSON/Markdown,
  - publication validation JSON/Markdown,
  - reproduction instructions.
- Added claim audit checks that block publication when recovered claims lack verifier evidence, track labels, source artifact links, final-confirmation or substitute verifier evidence, or baseline context.
- Added a release gate that validates the `dev` CI contract and a synthetic public snapshot contract.
- Recorded public branch publication as ready for `.github/workflows/publish-main.yml`; the local agent did not force-push `main`.
- Kept smoke rebuild mode fast with explicit skipped claim-audit and release-gate placeholders.
- Excluded raw campaign run payloads and `suite-result.json` from publication source locks and the committed evidence package.
- Documented the full v1.13 rebuild command and public-main handoff in `docs/IMPLEMENTATION.md`.

## Release Evidence

- Full rebuild output: `artifacts/paper/v1.13/manifest.json`
- Claim audit: `artifacts/paper/v1.13/claim-audit.json`
- Release gate: `artifacts/paper/v1.13/release-gate.json`
- Paper-track aggregate: `artifacts/campaigns/v1.13-paper-tracks-final/aggregate.json`
- Baseline harness: `artifacts/baselines/v1.13/manifest.json`
- Dataset manifests: `artifacts/datasets/v1.13/`

The final committed paper-track aggregate contains 24 paper-track rows, no execution failures, separate basis-only and literal-constant denominators, and 9 verifier-recovered rows.

## Requirement Coverage

- `PUB-01`: Complete. Full v1.13 publication rebuild generated the campaign, baseline, dataset, paper, validation, source-lock, claim-audit, and release-gate artifacts in the committed layout.
- `PUB-02`: Complete. The root manifest links the generated artifacts, source locks, reproduction command, environment and git provenance, claim audit, release gate, and validation results.
- `PUB-03`: Complete. Claim audit passed only after confirming verifier evidence, track labels, source artifact links, final-confirmation or substitute verifier evidence, and baseline context.
- `PUB-04`: Complete for the local release gate. The public snapshot contract validates and the release gate records `ready_for_publish_main_workflow`; direct remote `main` publication was left to `.github/workflows/publish-main.yml`.

## Verification

- Publication rebuild tests passed.
- Publication, baseline, and expanded dataset regression tests passed together.
- `scripts/validate-ci-contract.py --mode dev --root .` passed.
- Smoke publication rebuild passed.
- Full publication rebuild passed.
- Root manifest status, claim audit status, and release gate status are all `passed`.
- Manifest links 22 curated outputs and excludes raw run payloads.
- `git diff --check` passed.

## Notes

- The final publication manifest was generated while the tree was dirty only because the rebuild produced new untracked artifacts. Those curated artifacts are now committed in `31006ac`.
- Large raw run payloads remain reproducible from the campaign command but are intentionally not committed.
