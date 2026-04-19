---
gsd_state_version: 1.0
milestone: v1.11
milestone_name: Paper-strength evidence and figure package
current_phase: 61
current_phase_name: Ablation and Baseline Diagnostics
status: ready_to_execute
stopped_at: Phase 60 complete; Phase 61 ready
last_updated: "2026-04-19T00:00:00.000Z"
last_activity: 2026-04-19 -- Milestone v1.11 started
progress:
  total_phases: 5
  completed_phases: 2
  total_plans: 0
  completed_plans: 0
  percent: 40
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 61 - Ablation and Baseline Diagnostics
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-19)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** v1.11 paper-strength evidence, real training runs, low-hanging ablations, and plot-ready artifacts.

## Current Position

Phase: 61 - Ablation and Baseline Diagnostics
Plan: None
Status: Ready to execute
Last activity: 2026-04-19 -- Phase 60 completed with real v1.11 training/probe campaigns
Progress: [####------] 40% by completed phases

## Current Milestone

**v1.11: Paper-strength evidence and figure package**

Goal: Produce a stronger paper-ready evidence package by running real training where it is honest, adding low-hanging empirical comparisons and ablations, and generating plot-rich artifacts that clearly illustrate the EML hybrid pipeline.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Updated for v1.11 |
| Archived v1.10 requirements | `.planning/milestones/v1.10-REQUIREMENTS.md` | Complete |
| Requirements | `.planning/REQUIREMENTS.md` | Defined for v1.11 |
| Roadmap | `.planning/ROADMAP.md` | Active v1.11 phases 59-63 |
| Research summary | `.planning/research/SUMMARY.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.10 |
| v1.9 raw-hybrid paper package | `artifacts/paper/v1.9/raw-hybrid/` | Baseline paper package |
| v1.10 focused motif evidence | `artifacts/campaigns/v1.10-logistic-evidence/`, `artifacts/campaigns/v1.10-planck-diagnostics/` | Source evidence for v1.11 package |
| v1.11 raw-hybrid source package | `artifacts/paper/v1.11/raw-hybrid/` | Initial source-locked package generated |
| v1.11 paper training campaign | `artifacts/campaigns/v1.11-paper-training/` | Complete |
| v1.11 logistic/Planck probes | `artifacts/campaigns/v1.11-logistic-planck-probes/` | Complete |

## Accumulated Context

### Decisions

- v1.11 continues phase numbering from Phase 59 after v1.10 Phase 58.
- The paper should be framed as a verifier-gated hybrid EML symbolic-regression methods/evidence paper, not as broad blind-SR superiority.
- Real training should be run only in claim-safe regimes; warm-start/scaffolded/same-AST/repair/perturbed evidence must remain separately labeled.
- Logistic and Planck remain unsupported unless the strict compiler and verifier contract actually passes.
- Low-hanging paper-strengthening work includes v1.10 paper-package refresh, training reruns, ablation tables, plot generation, and scoped external/conventional baseline diagnostics.
- v1.11 phases are: Phase 59 evidence contracts/source locks, Phase 60 claim-safe training, Phase 61 ablations/baselines, Phase 62 figures/tables, Phase 63 package/audit.

### Pending Todos

Begin Phase 61 execution.

### Blockers/Concerns

External baseline dependencies may not be installed or may require network access. If unavailable, v1.11 should include explicit conventional/local baselines and mark external comparisons as deferred rather than blocking paper-package generation.

## Session Continuity

Last session: 2026-04-19
Stopped at: Phase 60 complete; Phase 61 ready
Resume file: None

---
*Last updated: 2026-04-19 after Phase 60*
