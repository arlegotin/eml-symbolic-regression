# Phase 76: Full Evidence Rebuild, Claim Audit, and Public Main Sync - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning
**Mode:** Autonomous smart-discuss equivalent

<domain>
## Phase Boundary

Phase 76 is the v1.13 release gate. It must regenerate the bounded publication evidence package, audit claim safety, commit the resulting artifacts on `dev`, and validate the public snapshot path for `main`.

</domain>

<decisions>
## Implementation Decisions

### Bounded Full Rebuild

Use the v1.13 `paper-tracks` campaign as the full paper-track evidence run. A local probe completed 24 rows in about 43 seconds, which is acceptable for an explicit release rebuild but too expensive for normal CI smoke.

### Publication Root Orchestrates Linked Evidence

Extend `publication-rebuild` full mode so the publication root manifest links:

- v1.13 paper-track campaign artifacts,
- matched baseline harness artifacts,
- expanded dataset manifests,
- source locks,
- claim audit,
- release/public snapshot gate,
- validation results.

### Claim Audit Gate

Audit recovered rows for verifier evidence, constants-track labels, source artifacts, and baseline context. Final confirmation can be satisfied by explicit final-confirmation splits or by stronger symbolic/dense/adversarial verifier evidence for legacy proof datasets that predate final-confirmation splits.

### Public Main Sync

Do not directly force-push `main` from the local agent. Validate the dev and public snapshot contracts locally and rely on the existing `publish-main` workflow to publish sanitized `main` after `dev` is pushed.

</decisions>

<code_context>
## Existing Code Insights

- `publication.py` currently writes a v1.13 smoke provenance package but does not run full evidence, claim audit, or public snapshot readiness.
- `campaign.py` has a `paper-tracks` preset over `v1.13-paper-tracks`.
- `baselines.py` writes matched baseline artifacts and dependency locks.
- `datasets.py` writes expanded dataset manifests.
- `scripts/validate-ci-contract.py` validates dev and public snapshot branch contracts.
- `.github/workflows/publish-main.yml` is the existing sanitized main publication path.

</code_context>

<specifics>
## Specific Ideas

- Extend `PublicationRebuildPaths` with claim-audit and release-gate artifacts.
- In full mode:
  - run `paper-tracks` to `artifacts/campaigns/v1.13-paper-tracks-final`,
  - run `baseline-harness` to `artifacts/baselines/v1.13`,
  - write expanded dataset manifests to `artifacts/datasets/v1.13`,
  - write claim audit and release gate artifacts under `artifacts/paper/v1.13`,
  - include linked artifact locks in the publication manifest.
- Keep `--smoke` fast and CI-friendly.
- Update tests for the expanded publication package shape.

</specifics>

<deferred>
## Deferred Ideas

- Actually pushing `dev` and letting GitHub publish `main` requires explicit operator approval and network credentials.
- Installing and running full external SR systems remains out of scope unless dependencies are intentionally provisioned.

</deferred>
