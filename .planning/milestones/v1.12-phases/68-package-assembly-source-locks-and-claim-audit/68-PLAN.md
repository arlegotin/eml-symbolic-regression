# Phase 68: Package Assembly, Source Locks, and Claim Audit - Plan

**Created:** 2026-04-19  
**Status:** Ready for execution

## Goal

Assemble the v1.12 supplement to the v1.11 paper package and verify that the draft, refreshed evidence, figures/tables, probes, and claim boundaries are source-backed.

## Tasks

1. Add v1.12 supplement path and dataclass to `paper_v112.py`.
2. Add source-lock collection for draft files, paper-facing assets, refresh tables, and bounded probes.
3. Add v1.12 claim audit checks for draft presence, taxonomy coverage, refresh counts, logistic/Planck no-promotion status, probe outcomes, and source-lock coverage.
4. Add supplement manifest, source-locks, claim-audit, claim-audit markdown, and reproduction markdown outputs.
5. Add CLI wiring for `paper-supplement`.
6. Add focused tests for supplement generation and audit behavior.
7. Generate the actual supplement artifacts and update requirements.

## Verification

- Supplement manifest exists under `artifacts/paper/v1.11/v1.12-supplement/`.
- Source locks cover all v1.12-added artifact families.
- Claim audit status is `passed`.
- Reproduction commands mention draft, refresh, figures, probes, and supplement commands.
- Focused tests pass.

## Risks

- The audit should fail if unsupported rows are silently promoted.
- Source locks should cover compact paper-facing artifacts without unnecessarily bloating the package with duplicate run payloads.
