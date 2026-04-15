---
gsd_state_version: 1.0
milestone: v1.5
milestone_name: milestone
current_phase: 29
status: executing
stopped_at: Milestone v1.5 roadmap created; ready for Phase 29 planning
last_updated: "2026-04-15T13:21:43.485Z"
last_activity: 2026-04-15 -- Phase 29 execution started
progress:
  total_phases: 5
  completed_phases: 0
  total_plans: 3
  completed_plans: 0
  percent: 0
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 29
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-15)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** Phase 29 — Paper Claim Contract and Proof Dataset Harness

## Current Position

Phase: 29 (Paper Claim Contract and Proof Dataset Harness) — EXECUTING
Plan: 1 of 3
Status: Executing Phase 29
Last activity: 2026-04-15 -- Phase 29 execution started
Progress: [----------] 0% by completed phases (v1.5: 0/5 planned)

## Performance Metrics

**Velocity:**

- Total plans completed: Historical v1, v1.1, v1.2, v1.3, and v1.4 milestones complete.
- Average duration: Not tracked
- Total execution time: Not tracked

**Recent Trend:**

- v1.4 improved overall standard/showcase recovery from 18/45 to 27/45.
- v1.4 blind recovery improved to 10/15, but `radioactive_decay` remains 0/5.
- v1.4 Beer-Lambert perturbation recovery remained 15/21, with high-noise failures diagnosed as active-slot perturbation.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete |
| v1.4 comparison report | `artifacts/campaigns/v1.4-comparison/comparison.md` | Complete |
| v1.5 requirements | `.planning/REQUIREMENTS.md` | Complete |
| v1.5 roadmap | `.planning/ROADMAP.md` | Complete |

## Current Milestone

**v1.5: Training Proof and Recovery Guarantees**

Goal: Prove paper-grounded EML training claims with real training runs, bounded 100% recovery targets, transparent failure boundaries, metrics, and reproducible datasets.

Target features:

- Executable paper claim suites and datasets.
- 100% verifier-owned training recovery on a declared bounded shallow proof suite.
- Repair for current `radioactive_decay` blind failures and scaled/signed exponential families.
- Perturbed true-tree basin recovery metrics and Beer-Lambert high-noise repair or a defensible narrowed bound.
- Depth-curve experiments that reproduce the paper's qualitative blind-vs-perturbed behavior.
- Proof report with raw runs, metrics, plots, and honest claim taxonomy.

## Phase Status

| Phase | Name | Status | Requirements |
|-------|------|--------|--------------|
| 29 | Paper Claim Contract and Proof Dataset Harness | Pending | CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04 |
| 30 | Bounded Shallow Blind Training Recovery | Pending | SHAL-01, SHAL-02, SHAL-03, SHAL-04 |
| 31 | Perturbed Basin Training and Local Repair | Pending | BASN-01, BASN-02, BASN-03, BASN-04, BASN-05 |
| 32 | Paper Depth-Curve Training Evidence | Pending | CURV-01, CURV-02, CURV-03, CURV-04 |
| 33 | Proof Campaign Report and Evidence Lockdown | Pending | EVID-01, EVID-02, EVID-03, EVID-04, EVID-05 |

## Accumulated Context

### Decisions

- v1.4 changed measured performance, not the definition of `recovered`.
- v1.4 used committed v1.3 `standard` and `showcase` campaigns as before/after baselines.
- Phase 25 primitive scaffolds are paper-grounded default initializers, not a relaxed recovery contract.
- Phase 26 records high-noise Beer-Lambert failures as active-slot perturbation instead of hiding them.
- Phase 27 compiler expansion remains fail-closed and validates Shockley before accepting it.
- Phase 28 comparison shows overall v1.4 recovery improved from 18/45 to 27/45 across standard and showcase campaigns.
- v1.5 interprets "100% fully functional training" as 100% recovery over explicitly declared bounded proof suites, plus honest measured failure boundaries for deeper blind recovery.

### Pending Todos

None recorded.

### Blockers/Concerns

The milestone must not claim universal blind recovery of arbitrary deep elementary expressions, because the source paper reports rapid blind recovery degradation beyond shallow depths.

## Session Continuity

Last session: 2026-04-15
Stopped at: Milestone v1.5 roadmap created; ready for Phase 29 planning
Resume file: None

---
*Last updated: 2026-04-15 after creating milestone v1.5 roadmap*
