---
gsd_state_version: 1.0
milestone: v1.17
milestone_name: Natural-Bias Recovery Sandbox
current_phase: null
status: archived
stopped_at: v1.17 archived; ready for next milestone definition
last_updated: "2026-04-22T12:42:37.054Z"
last_activity: 2026-04-22
progress:
  total_phases: 5
  completed_phases: 5
  total_plans: 5
  completed_plans: 5
  percent: 100
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** None
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-22)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** No active milestone. v1.17 is archived; define the next milestone before new phase work.

## Current Position

Phase: None active
Plan: None active
Status: v1.17 archived; final package decision `still_inconclusive`
Last activity: 2026-04-22
Progress: [##########] 100% by completed phases

## Current Milestone

No milestone is active. v1.17 is archived with final decision `still_inconclusive`; broader i*pi/GEML campaigns remain blocked.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Updated for v1.17 |
| Requirements | `.planning/milestones/v1.17-REQUIREMENTS.md` | Archived for v1.17 |
| Roadmap | `.planning/milestones/v1.17-ROADMAP.md` | Archived for v1.17; phases 94-98 |
| Milestone audit | `.planning/milestones/v1.17-MILESTONE-AUDIT.md` | Archived for v1.17; status `tech_debt` |
| v1.17 evidence package | `artifacts/paper/v1.17-geml/` | Complete, audit passed, decision `still_inconclusive` |
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
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.17 |

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

- Start the next milestone with `$gsd-new-milestone`.

### Deferred Items

Items acknowledged and deferred across milestone closes (latest audit on 2026-04-22):

| Category | Item | Status |
|----------|------|--------|
| quick_task | 260419-ukc-rewrite-readme-to-make-it-clear-engaging | missing |
| quick_task | 260419-uxg-make-readme-clear-and-cool-without-menti | missing |
| quick_task | 260420-b8n-add-readme-plot-section-showing-how-demo | missing |
| quick_task | 260420-bdg-expand-readme-fit-plots-with-four-additi | missing |
| quick_task | 260420-bia-fix-readme-plot-gallery-to-one-conservat | missing |
| quick_task | 260420-g7h-include-useful-public-artifacts-in-sanit | unknown |
| quick_task | 260420-ixp-return-tests-to-generated-main-branch | unknown |
| quick_task | 260420-ng7-update-readme-with-v1-13-release-evidenc | missing |
| quick_task | 260420-nll-replace-readme-plots-with-clearer-v1-13- | missing |
| quick_task | 260420-nuw-simplify-readme-release-narrative-and-re | missing |
| quick_task | 260420-o1v-update-readme-plot-gallery-with-data-spl | missing |
| quick_task | 260420-o7r-simplify-readme-plot-gallery-labels-and- | missing |
| quick_task | 260420-oij-remove-readme-release-framing-and-label- | missing |
| quick_task | 260420-p9c-hide-github-workflows-from-generated-mai | unknown |

### Completed Quick Tasks

Historical quick-task records remain in prior state and milestone artifacts. No new quick task was opened during v1.17 initialization.

### Blockers/Concerns

- Larger raw/i*pi campaigns remain blocked by the v1.17 final gate.
- The committed v1.17 package generated no exact-recovery signal from the current v1.16 pilot artifacts.
- Local repair can easily become claim-contaminating if provenance is vague. Promotion must stay verifier-owned and accounting-separated.
- Branch behavior remains part of the i*pi operator contract, not an implementation detail.

## Session Continuity

Last session: 2026-04-22
Stopped at: v1.17 archived; ready for next milestone definition
Resume file: None

---
*Last updated: 2026-04-22 after v1.17 archive*
