---
gsd_state_version: 1.0
milestone: v1.12
milestone_name: Paper draft skeleton and refreshed shallow evidence
current_phase: 68
current_phase_name: Package Assembly, Source Locks, and Claim Audit
status: milestone_complete
stopped_at: v1.12 archived
last_updated: "2026-04-19T20:18:41.000Z"
last_activity: 2026-04-19
progress:
  total_phases: 5
  completed_phases: 5
  total_plans: 5
  completed_plans: 5
  percent: 100
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 68 - Package Assembly, Source Locks, and Claim Audit
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-19)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** v1.12 archived; no active milestone.

## Current Position

Phase: 68 - Package Assembly, Source Locks, and Claim Audit
Plan: Complete
Status: Milestone archived
Last activity: 2026-04-19 - Completed quick task 260419-uxg: public-facing README polish
Progress: [##########] 100% by completed phases

## Current Milestone

**v1.12: Paper draft skeleton and refreshed shallow evidence**

Goal: Turn the v1.11 evidence package into a paper-shaped draft while refreshing the most reviewer-visible shallow/depth evidence and making claim boundaries explicit.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Updated for v1.12 |
| Archived v1.11 requirements | `.planning/milestones/v1.11-REQUIREMENTS.md` | Complete |
| Requirements | `.planning/REQUIREMENTS.md` | Defined for v1.12 |
| Roadmap | `.planning/ROADMAP.md` | Active v1.12 phases 64-68 |
| Research summary | `.planning/research/SUMMARY.md` | Reuse existing context; no new domain research selected |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.11 |
| v1.11 final paper package | `artifacts/paper/v1.11/` | Complete, audit passed |
| v1.12 draft skeleton | `artifacts/paper/v1.11/draft/` | Phase 64 complete |
| v1.12 evidence refresh | `artifacts/campaigns/v1.12-evidence-refresh/` | Phase 65 complete |
| v1.12 paper-facing draft assets | `artifacts/paper/v1.11/draft/` | Phase 66 complete |
| v1.12 bounded probes | `artifacts/paper/v1.11/draft/` | Phase 67 complete |
| v1.12 supplement | `artifacts/paper/v1.11/v1.12-supplement/` | Phase 68 complete, audit passed |
| v1.12 training-detail assets | `artifacts/paper/v1.11/draft/training-detail/` | Quick task complete: 4,472 step rows, 232 candidate rows |

## Accumulated Context

### Decisions

- v1.12 continues phase numbering after v1.11 Phase 63.
- The paper should remain framed as a verifier-gated hybrid EML symbolic-regression methods/evidence paper, not broad blind-SR superiority.
- Pure blind, scaffolded, same-AST, warm-start, perturbed-basin, repair/refit, compile-only, unsupported, and failed evidence remain separate denominators.
- Logistic and Planck remain unsupported unless strict support and verifier contracts actually pass.
- Additional shallow/depth seeds are credibility refreshes, not a change in the claim standard.
- Conventional symbolic-regression comparison is useful but must not become a time sink; unavailable dependencies should be reported as deferred.
- A logistic strict-support push is bounded compiler work and may fail; no gate relaxation is allowed.

### Pending Todos

- Start the next milestone with `$gsd-new-milestone`.

### Completed Quick Tasks

| Date | Task | Status | Artifacts |
|------|------|--------|-----------|
| 2026-04-19 | Paper-ready training detail artifacts | Complete | `artifacts/paper/v1.11/draft/training-detail/` |
| 2026-04-19 | README clarity and usage rewrite | Complete | `.planning/quick/260419-ukc-rewrite-readme-to-make-it-clear-engaging/` |
| 2026-04-19 | Public-facing README polish | Complete | `.planning/quick/260419-uxg-make-readme-clear-and-cool-without-menti/` |

### Blockers/Concerns

- External SR baselines may require dependencies or network access. If unavailable locally, record that explicitly instead of blocking the milestone.
- Extra training runs should stay shallow and cheap; broad new campaigns are out of scope.

## Session Continuity

Last session: 2026-04-19
Stopped at: v1.12 archived
Resume file: None

---
*Last updated: 2026-04-19 after public-facing README polish*
