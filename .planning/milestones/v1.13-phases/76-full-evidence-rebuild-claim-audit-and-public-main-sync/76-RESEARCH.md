# Phase 76: Full Evidence Rebuild, Claim Audit, and Public Main Sync - Research

**Researched:** 2026-04-20
**Status:** Complete

## Existing Publication Rebuild

`publication.py` writes a v1.13 package with manifest, source locks, reproduction docs, and validation. In smoke mode this is appropriate for CI. In full mode it currently produces the same package shape and does not yet link the v1.13 paper-track evidence, baseline harness, dataset manifests, or claim audit.

## Evidence Inputs

Phase 73 added the `paper-tracks` campaign preset over `v1.13-paper-tracks`. A local probe completed:

- 24 total rows,
- 15 unsupported rows,
- 0 failed rows,
- aggregate outputs under the selected output root.

This makes it practical for a deliberate full publication rebuild.

Phase 75 added the matched baseline harness, which can write a default 80-row comparison matrix with unavailable external adapters reported explicitly.

Phase 74 added expanded dataset manifests, which should be generated and source-locked as broader-data context for the publication root.

## Claim Audit Strategy

The audit should pass only if:

- paper-track aggregate and run artifacts exist,
- recovered rows have verifier evidence,
- recovered rows carry benchmark track and constants policy,
- recovered rows have final-confirmation status or an explicit verifier-evidence substitute for legacy proof datasets,
- baseline context exists and is excluded from EML recovery denominators,
- source/output locks exist,
- no benchmark rows failed unexpectedly.

Unsupported rows should remain visible and do not fail the audit.

## Public Snapshot Strategy

The repo already has a dev-only `publish-main.yml` workflow that publishes a sanitized `main` branch with `--force-with-lease`. Phase 76 should validate:

- dev branch contract,
- simulated public snapshot contract,
- release package validation,
- claim audit status.

The local agent should not force-push `main` directly.

## Test Strategy

- Keep smoke rebuild tests fast.
- Add tests that smoke mode now writes claim-audit and release-gate placeholders.
- Add unit tests for the claim audit using synthetic aggregate/baseline fixtures.
- Run a real full publication rebuild once for verification and commit generated v1.13 artifacts.
