---
gsd_state_version: 1.0
milestone: v1.17
milestone_name: Snap-First Exact Recovery and Candidate Neighborhood Search
current_phase: 94
status: planning
stopped_at: v1.17 milestone initialized; ready for Phase 94 planning
last_updated: "2026-04-22T12:09:41Z"
last_activity: 2026-04-22
progress:
  total_phases: 5
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 94
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-22)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** v1.17 Snap-First Exact Recovery and Candidate Neighborhood Search.

## Current Position

Phase: 94 - Snap-Mismatch Diagnostics and Low-Margin Inventory
Plan: Not started
Status: v1.17 milestone initialized; ready for Phase 94 planning
Last activity: 2026-04-22
Progress: [----------] 0% by completed phases

## Current Milestone

v1.17 is active. The milestone starts from the v1.16 final package decision `inconclusive`: 12 paired pilot rows, 0 exact recoveries for raw or i*pi EML, 12 loss-only outcomes, and a fail-closed stop before the full campaign. The work now targets the snap/candidate bottleneck before any larger i*pi/GEML campaign is reopened.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Updated for v1.17 |
| Requirements | `.planning/REQUIREMENTS.md` | Complete for v1.17 |
| Roadmap | `.planning/ROADMAP.md` | Complete for v1.17; phases 94-98 |
| Archived v1.16 requirements | `.planning/milestones/v1.16-REQUIREMENTS.md` | Complete |
| Archived v1.16 roadmap | `.planning/milestones/v1.16-ROADMAP.md` | Complete |
| Archived v1.16 milestone audit | `.planning/milestones/v1.16-MILESTONE-AUDIT.md` | Passed as inconclusive, fail-closed package |
| Archived v1.16 phase artifacts | `.planning/milestones/v1.16-phases/` | Complete |
| v1.16 final paper package | `artifacts/paper/v1.16-geml/` | Complete, audit passed, decision `inconclusive` |
| v1.15 GEML evidence package | `artifacts/paper/v1.15-geml/` | Complete, audit passed, decision `inconclusive_smoke_only` |
| v1.14 corrected evidence package | `artifacts/paper/v1.14/` | Complete, claim audit and release gate passed |
| v1.13 clean-room evidence package | `artifacts/paper/v1.13/` | Complete, audit and release gate passed |
| Research summary | `.planning/research/SUMMARY.md` | Existing context retained; no new domain research selected during initialization |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.16 |

## Accumulated Context

### Decisions

- v1.16 produced a complete, source-locked, claim-audited final package, but the scientific result is inconclusive rather than paper-positive.
- v1.16 exact recovery count is 0 for both raw EML and i*pi EML in the checked pilot denominator.
- v1.16's useful signal is loss-only: 12 loss-only rows, with 3 i*pi lower post-snap MSE rows and 9 raw lower post-snap MSE rows.
- The v1.16 full campaign was correctly stopped fail-closed because the pilot did not produce exact-recovery signal.
- v1.17 should work snap-first before spending more broad campaign budget.
- Exact-neighborhood search must remain target-agnostic and verifier-owned.
- Candidate ranking should prefer exact verifier status over post-snap loss.
- Loss-only, repaired, compile-only, same-AST, fallback, and original-snap evidence classes must remain separate.

### Pending Todos

- Plan Phase 94.

### Deferred Items

Items acknowledged and deferred at milestone close on 2026-04-20:

| Category | Item | Status |
|----------|------|--------|
| quick_task | 260419-ukc-rewrite-readme-to-make-it-clear-engaging | missing |
| quick_task | 260419-uxg-make-readme-clear-and-cool-without-menti | missing |
| quick_task | 260420-b8n-add-readme-plot-section-showing-how-demo | missing |
| quick_task | 260420-bdg-expand-readme-fit-plots-with-four-additi | missing |
| quick_task | 260420-bia-fix-readme-plot-gallery-to-one-conservat | missing |
| quick_task | 260420-g7h-include-useful-public-artifacts-in-sanit | unknown |
| quick_task | 260420-ixp-return-tests-to-generated-main-branch | unknown |

### Completed Quick Tasks

Historical quick-task records remain in prior state and milestone artifacts. No new quick task was opened during v1.17 initialization.

### Blockers/Concerns

- Larger raw/i*pi campaigns should remain blocked until Phase 97 produces at least one exact-recovery signal.
- Snap-neighborhood search could explode combinatorially; Phase 95 needs deterministic budget caps.
- Local repair can easily become claim-contaminating if provenance is vague. Promotion must stay verifier-owned and accounting-separated.
- Branch behavior remains part of the i*pi operator contract, not an implementation detail.

## Session Continuity

Last session: 2026-04-22
Stopped at: v1.17 milestone initialized; ready for Phase 94 planning
Resume file: None

---
*Last updated: 2026-04-22 after v1.17 milestone start*
