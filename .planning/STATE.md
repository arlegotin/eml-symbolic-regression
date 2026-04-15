---
gsd_state_version: 1.0
milestone: v1.2
milestone_name: Training Benchmark and Recovery Evidence
current_phase: 16
status: ready_for_phase_planning
stopped_at: phase 15 complete; ready for phase 16
last_updated: "2026-04-15T10:42:56Z"
last_activity: 2026-04-15
progress:
  total_phases: 5
  completed_phases: 2
  total_plans: 2
  completed_plans: 2
  percent: 40
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 16
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-15)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** Milestone v1.2 - Training Benchmark and Recovery Evidence

## Current Position

Phase: 16 of 18 (Experiment Matrix and Formula Coverage)
Plan: Not started
Status: Ready to plan phase 16
Last activity: 2026-04-15
Progress: [####------] 40% by completed phases (v1.2: 2/5)

## Performance Metrics

**Velocity:**

- Total plans completed: Historical v1 and v1.1 phases complete; v1.2 phases 14-15 complete
- Average duration: Not tracked
- Total execution time: Not tracked

**Recent Trend:**

- Trend: Unknown

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Research summary | `.planning/research/SUMMARY.md` | Skipped for v1.2; local evidence milestone |
| Requirements | `.planning/REQUIREMENTS.md` | Complete |
| Roadmap | `.planning/ROADMAP.md` | Complete |

## Current Milestone

**v1.2: Training Benchmark and Recovery Evidence**

Goal: Turn anecdotal training runs into a repeatable benchmark harness that measures when EML recovery works, when it fails, and how strong the evidence is.

Target features:

- Benchmark suite definitions for blind starts, compiler warm starts, perturbation sweeps, and demo/stretch diagnostics.
- Per-run JSON artifacts and aggregate reports for loss, snap outcome, verifier status, recovery rate, active slot changes, runtime, and failures.
- Coverage for shallow blind baselines, Beer-Lambert perturbation levels, Michaelis-Menten and Planck diagnostics, and selected `sources/FOR_DEMO.md` formulas.
- Documentation that separates promising infrastructure from actual measured recovery performance.

## Phase Status

| Phase | Name | Status | Requirements |
|-------|------|--------|--------------|
| 1 | Semantics, AST, and Deterministic Artifacts | Complete | SEM-01, SEM-02, SEM-03, SEM-04 |
| 2 | Complete Master Trees and Soft Evaluation | Complete | TREE-01, TREE-02, TREE-03, TREE-04 |
| 3 | Optimizer, Restarts, Hardening, and Recovery Statuses | Complete | OPT-01, OPT-02, OPT-03, OPT-04 |
| 4 | Verifier and Acceptance Contract | Complete | VER-01, VER-02, VER-03 |
| 5 | Local Cleanup, SymPy Export, and Reports | Complete | CLEAN-01, CLEAN-02, CLEAN-03 |
| 6 | Demo Harness and Public Showcase | Complete | DEMO-01, DEMO-02, DEMO-03, DEMO-04 |
| 7 | Tests and Documentation | Complete | TEST-01, TEST-02 |
| 8 | Compiler Contract and Direct Rules | Complete | COMP-01, COMP-02, COMP-03, COMP-04 |
| 9 | Constant Catalog and AST Embedding | Complete | CONST-01, CONST-02, EMBED-01, EMBED-02, EMBED-03 |
| 10 | Arithmetic Rule Corpus and Depth Gates | Complete | ARITH-01, ARITH-02, ARITH-03 |
| 11 | Perturbed Warm-Start Training | Complete | WARM-01, WARM-02, WARM-03, WARM-04 |
| 12 | Demo Promotion and Claim Reporting | Complete | DEMO-05, DEMO-06, DEMO-07, DEMO-08 |
| 13 | Regression Tests and Documentation Lockdown | Complete | TEST-03, TEST-04 |
| 14 | Benchmark Contract and Suite Registry | Complete | BENC-01, BENC-02, BENC-03, BENC-04 |
| 15 | Benchmark Runner and Training Modes | Complete | RUN-01, RUN-02, RUN-03, RUN-04 |
| 16 | Experiment Matrix and Formula Coverage | Pending | MATR-01, MATR-02, MATR-03, MATR-04 |
| 17 | Evidence Aggregation and Report Contracts | Pending | EVID-01, EVID-02, EVID-03, EVID-04 |
| 18 | Smoke Tests, Docs, and Evidence Lockdown | Pending | TEST-05, TEST-06, TEST-07 |

## Accumulated Context

### Decisions

- v1.1 uses the research-recommended six-phase structure, renumbered from Phase 8 through Phase 13.
- Requirement traceability is complete: 22/22 v1.1 requirements mapped exactly once.
- `recovered` remains verifier-owned and post-snap; compiler output and training loss cannot promote a candidate alone.
- Literal constants are explicit warm-start/demo provenance, not pure `{1, eml}` recovery claims.
- Normalized Planck is stretch reporting only, not a trained-recovery milestone guarantee.
- The immediate evidence gap is robustness: strong Beer-Lambert perturbation failed once active slots changed, so v1.2 must measure recovery rates instead of relying on single success cases.
- v1.2 continues phase numbering from v1.1 and maps 19 requirements across phases 14-18.
- Phase 14 established benchmark contracts, built-in suite registry, validation, stable run IDs, and deterministic artifact paths.
- Phase 15 added benchmark suite execution, CLI commands, filtered runs, and structured unsupported/failure artifacts.

### Pending Todos

None recorded.

### Blockers/Concerns

None.

## Session Continuity

Last session: 2026-04-15
Stopped at: Phase 15 complete; ready for Phase 16 planning
Resume file: None

---
*Last updated: 2026-04-15 after completing phase 15*
