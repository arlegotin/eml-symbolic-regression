---
gsd_state_version: 1.0
milestone: v1.6
milestone_name: hybrid search pipeline and exact candidate recovery
current_phase: 36
status: ready
stopped_at: Phase 35 complete; Phase 36 is ready for discussion and planning
last_updated: "2026-04-16T10:50:51Z"
last_activity: 2026-04-16 -- Phase 35 completed; target-free discrete cleanup landed
progress:
  total_phases: 5
  completed_phases: 2
  total_plans: 2
  completed_plans: 2
  percent: 40
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 36
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-16)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** Phase 35 is complete — target-free discrete cleanup is in place and Phase 36 is ready

## Current Position

Phase: 36 (Post-Snap Constant Refit and Numerical Stability) — NOT STARTED
Plan: —
Status: Ready for phase discussion/planning
Last activity: 2026-04-16 -- Phase 35 completed; target-free discrete cleanup landed
Progress: [####......] 40% by completed phases (v1.6: 2/5 planned)

## Performance Metrics

**Velocity:**

- Total plans completed: Historical v1 through v1.5 milestones complete, plus 1 plan completed in v1.6.
- Average duration: Not tracked
- Total execution time: Not tracked

**Recent Trend:**

- v1.5 proved that representation and verifier contracts are strong while pure-blind shallow recovery remains weak (`2/18`) and deeper blind recovery degrades after depth 3.
- v1.5 scaffolded shallow proof reached `18/18`, and perturbed basin proof reached `9/9`, showing that basin return is much stronger than blind discovery.
- v1.6 focuses on search-quality upgrades that can weakly dominate the current exact-candidate selector while keeping archived baselines intact.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete |
| v1.4 comparison report | `artifacts/campaigns/v1.4-comparison/comparison.md` | Complete |
| v1.5 proof report | `artifacts/proof/v1.5/proof-report.md` | Complete |
| v1.5 milestone audit | `.planning/v1.5-MILESTONE-AUDIT.md` | Complete |
| v1.5 archived requirements | `.planning/milestones/v1.5-REQUIREMENTS.md` | Complete |
| v1.5 archived roadmap | `.planning/milestones/v1.5-ROADMAP.md` | Complete |
| v1.5 archived phase context | `.planning/milestones/v1.5-phases/` | Complete |
| v1.6 requirements | `.planning/REQUIREMENTS.md` | Complete |
| v1.6 roadmap | `.planning/ROADMAP.md` | Complete |
| Phase 34 planning and execution artifacts | `.planning/phases/34-exact-candidate-pool-and-checkpoint-snapping/` | Complete |
| Phase 35 planning and execution artifacts | `.planning/phases/35-snap-neighborhood-discrete-cleanup/` | Complete |

## Current Milestone

**v1.6: Hybrid Search Pipeline and Exact Candidate Recovery**

Goal: Upgrade the current MVP optimizer into a verifier-gated hybrid recovery pipeline that improves exact candidate quality without weakening the evidence contract.

Target features:

- Exact-candidate selection from restarts and hardening checkpoints rather than soft-loss-only winners.
- Target-free low-margin discrete cleanup and snap-neighborhood repair.
- Post-snap constant refit plus stronger `exp`/`log` numerical and domain controls.
- Short compiler macros and wider warm-start coverage with fail-closed fallback preserved.
- Honest proof and campaign reruns against archived v1.5 and v1.4 baselines.

## Phase Status

| Phase | Name | Status | Requirements |
|-------|------|--------|--------------|
| 34 | Exact Candidate Pool and Checkpoint Snapping | Complete | HARD-01, HARD-02, HARD-03, HARD-04 |
| 35 | Snap-Neighborhood Discrete Cleanup | Complete | DISC-01, DISC-02, DISC-03, DISC-04 |
| 36 | Post-Snap Constant Refit and Numerical Stability | Pending | REFI-01, REFI-02, STAB-01, STAB-02 |
| 37 | Compiler Macro Shortening and Warm-Start Coverage | Pending | COMP-01, COMP-02, COMP-03 |
| 38 | Hybrid Recovery Evaluation and Regression Lockdown | Pending | EVAL-01, EVAL-02, EVAL-03, EVAL-04 |

## Accumulated Context

### Decisions

- v1.4 changed measured performance, not the definition of `recovered`.
- v1.4 used committed v1.3 `standard` and `showcase` campaigns as before/after baselines.
- Phase 25 primitive scaffolds are paper-grounded default initializers, not a relaxed recovery contract.
- Phase 26 records high-noise Beer-Lambert failures as active-slot perturbation instead of hiding them.
- Phase 27 compiler expansion remains fail-closed and validates Shockley before accepting it.
- Phase 28 comparison shows overall v1.4 recovery improved from 18/45 to 27/45 across standard and showcase campaigns.
- v1.5 interprets "100% fully functional training" as 100% recovery over explicitly declared bounded proof suites, plus honest measured failure boundaries for deeper blind recovery.
- Phase 29 established the v1.5 proof contract: stable paper claim matrix, deterministic proof dataset manifests, proof-aware benchmark artifacts, derived evidence classes, claim-level threshold summaries, CLI inspection commands, and campaign proof metadata/reporting.
- Phase 30 review CR-01 is resolved by splitting the shallow claim contract: `paper-shallow-blind-recovery` is now a measured pure random-initialized blind boundary with scaffold initializers disabled, and `paper-shallow-scaffolded-recovery` owns the bounded 100% scaffolded proof suite.
- Phase 31 completed and verified perturbed true-tree basin recovery, verifier-gated local repair, and durable Beer-Lambert bound evidence. BASN-01 through BASN-05 are complete.
- Phase 32 completed a deterministic exact depth inventory, a measured `proof-depth-curve` suite, per-depth blind-versus-perturbed summaries, and campaign report hooks that preserve deeper blind failures as expected paper-boundary evidence.
- Phase 33 completed the one-command `proof-campaign` bundle rooted at `artifacts/proof/v1.5/`, keeping v1.5 proof denominators separate from v1.4 showcase baselines and carrying forward the perturbed basin bound report.
- v1.6 begins from the proof-bundle evidence that representation is strong but blind search quality is still the dominant bottleneck.
- v1.6 will prioritize weak-dominance upgrades first: exact-candidate pooling, discrete cleanup, refit, and compiler shortening must preserve the current exact candidate as fallback on declared benchmark paths.
- Phase 34 added explicit late hardening checkpoints, retained exact-candidate pooling, verifier-gated selection, and serialized legacy fallback provenance across blind, warm-start, basin, benchmark, and CLI flows.
- Phase 35 added replayable active-slot alternatives, bounded exact-AST-deduplicated neighborhood expansion, target-free cleanup, and repair artifacts for blind, warm-start, and perturbed-basin flows while preserving the original selected candidate manifest.

### Pending Todos

None recorded.

### Blockers/Concerns

The milestone intentionally does not claim universal blind recovery of arbitrary deep elementary expressions, because both the paper and the v1.5 proof bundle show rapid blind recovery degradation beyond shallow depths.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260415-wkr | Resolve Phase 30 by splitting pure blind and scaffolded shallow recovery claims | 2026-04-15 | 653979d | [260415-wkr-resolve-phase-30-by-splitting-pure-blind](./quick/260415-wkr-resolve-phase-30-by-splitting-pure-blind/) |

## Session Continuity

Last session: 2026-04-16
Stopped at: Phase 35 complete; Phase 36 is ready for discussion and planning
Resume file: None

---
*Last updated: 2026-04-16 after completing Phase 35 and advancing milestone v1.6 to Phase 36*
