---
gsd_state_version: 1.0
milestone: v1.3
milestone_name: Benchmark Campaign and Evidence Report
current_phase: Not started
status: defining_requirements
stopped_at: defining v1.3 requirements and roadmap
last_updated: "2026-04-15T11:15:22Z"
last_activity: 2026-04-15
progress:
  total_phases: 0
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** Not started
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-15)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** Milestone v1.3 - Benchmark Campaign and Evidence Report

## Current Position

Phase: Not started (defining requirements)
Plan: -
Status: Defining requirements
Last activity: 2026-04-15
Progress: [----------] 0% by completed phases

## Performance Metrics

**Velocity:**

- Total plans completed: Historical v1, v1.1, and v1.2 phases complete; v1.3 not started
- Average duration: Not tracked
- Total execution time: Not tracked

**Recent Trend:**

- Trend: Unknown

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Research summary | `.planning/research/SUMMARY.md` | Local research decision recorded |
| Requirements | `.planning/REQUIREMENTS.md` | In progress |
| Roadmap | `.planning/ROADMAP.md` | Pending |

## Current Milestone

**v1.3: Benchmark Campaign and Evidence Report**

Goal: Showcase how the paper's EML symbolic-regression idea performs in practice by running a real benchmark campaign and producing crisp numbers, tables, graphs, and a polished evidence report.

Target features:

- Campaign presets that run the v1.2 benchmark matrix at smoke, standard, and showcase budgets with reproducible output folders.
- CSV exports for run-level metrics, grouped recovery rates, losses, timing, perturbation sensitivity, and failure taxonomy.
- Static publication-style plots for recovery rate, loss before/after snapping, Beer-Lambert perturbation behavior, runtime/depth, and unsupported/failure breakdowns.
- A self-contained report folder with `report.md`, figures, CSV/JSON data, exact commands, and an honest narrative about what works, what fails, and what remains hard.

## Phase Status

Pending roadmap creation.

## Accumulated Context

### Decisions

- v1.1 uses the research-recommended six-phase structure, renumbered from Phase 8 through Phase 13.
- Requirement traceability is complete: 22/22 v1.1 requirements mapped exactly once.
- `recovered` remains verifier-owned and post-snap; compiler output and training loss cannot promote a candidate alone.
- Literal constants are explicit warm-start/demo provenance, not pure `{1, eml}` recovery claims.
- Normalized Planck is stretch reporting only, not a trained-recovery milestone guarantee.
- The immediate evidence gap is robustness: strong Beer-Lambert perturbation failed once active slots changed, so v1.2 measured recovery rates instead of relying on single success cases.
- v1.2 established benchmark contracts, suite execution, formula matrix coverage, aggregate evidence reports, and smoke artifacts.
- v1.3 should produce showcase-grade evidence before optimizer changes.

### Pending Todos

None recorded.

### Blockers/Concerns

None.

## Session Continuity

Last session: 2026-04-15
Stopped at: v1.3 milestone initialized
Resume file: None

---
*Last updated: 2026-04-15 after starting milestone v1.3*
