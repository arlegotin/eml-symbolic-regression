# Phase 76: Full Evidence Rebuild, Claim Audit, and Public Main Sync - Plan

**Planned:** 2026-04-20
**Status:** Ready for execution

## Objective

Turn the v1.13 publication rebuild from a smoke provenance package into the bounded full release gate that regenerates paper-track evidence, baseline context, dataset manifests, claim audit, release gate, and publication validation artifacts.

## Tasks

### 1. Publication Full Mode

- Extend `PublicationRebuildPaths` with:
  - `claim-audit.json`,
  - `claim-audit.md`,
  - `release-gate.json`,
  - `release-gate.md`.
- Keep smoke mode fast.
- In full mode, generate linked evidence artifacts:
  - `paper-tracks` campaign,
  - baseline harness,
  - expanded dataset manifests.

### 2. Claim Audit

- Add claim audit builder.
- Check paper-track aggregate and recovered rows.
- Require verifier evidence, track labels, constants policy, artifact source path, and baseline context.
- Treat unsupported rows as visible denominators, not failures.

### 3. Release/Public Snapshot Gate

- Add release gate builder.
- Validate dev contract with `scripts/validate-ci-contract.py --mode dev`.
- Validate a synthetic public snapshot with required public files and forbidden private files absent.
- Record that main publication is prepared through the existing `publish-main` workflow, not by local force-push.

### 4. Tests and Docs

- Update publication rebuild tests.
- Add claim audit tests.
- Document the full rebuild command and public-main handoff.

### 5. Verification and Artifacts

- Run focused tests.
- Run full publication rebuild:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir artifacts/paper/v1.13 --overwrite --allow-dirty
```

- Validate the generated package and public snapshot contract.

## Acceptance Checks

- Full rebuild generates campaign, baseline, dataset, publication, claim-audit, release-gate, source-lock, and validation artifacts.
- Claim audit passes only with verifier evidence, track labels, source locks, and baseline context.
- Public snapshot contract validates locally.
- Generated v1.13 artifacts are committed on `dev`.
- Direct remote `main` force-push is not attempted by the local agent.
