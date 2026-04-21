# Phase 81 Context: Corrected Evidence Rebuild and Claim Audit

## Goal

Regenerate public evidence artifacts from the corrected Phase 77-80 contracts and make stale claim surfaces fail closed.

## Relevant Requirements

- PUB-01: The publication evidence package is regenerated after accounting, warm-start labeling, baseline surface, and verifier fixes land.
- PUB-02: README, campaign report, aggregate JSON/Markdown, claim-audit outputs, and paper-facing tables contain no stale 9-row recovered headline.
- PUB-03: CI or release-gate checks lock the corrected schema, corrected headline counts, and absence of compile-only recovery promotion.
- PUB-04: Historical v1.13 artifacts remain inspectable while corrected artifacts have source locks and regeneration commands.

## Current State

- Phases 77-80 changed the accounting, warm-start labels, baseline quarantine, and verifier behavior.
- The existing checked-in `artifacts/paper/v1.13/` and `artifacts/campaigns/v1.13-paper-tracks-final/` packages are historical and should not be overwritten.
- `publication-rebuild` currently defaults to v1.13 paths and links generated evidence into top-level `artifacts/`.
- Claim audit already locks corrected headline counts and compile-only exclusion; Phase 79 added baseline quarantine checks.

## Constraints

- Preserve historical v1.13 artifacts.
- Regenerate corrected artifacts with source locks and commands.
- Keep the full campaign bounded to the existing 24-row paper-track suite.
- Do not install optional external baseline dependencies.

