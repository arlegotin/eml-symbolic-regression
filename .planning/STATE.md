---
gsd_state_version: 1.0
milestone: v1.4
milestone_name: Recovery Performance Improvements
current_phase: 27
status: ready_for_phase_planning
stopped_at: Phase 26 complete; ready for Phase 27 planning
last_updated: "2026-04-15T15:45:00Z"
last_activity: 2026-04-15
progress:
  total_phases: 5
  completed_phases: 3
  total_plans: 3
  completed_plans: 3
  percent: 60
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 27
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-15)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** Milestone v1.4 - Recovery Performance Improvements

## Current Position

Phase: Not started (defining requirements)
Plan: Not started
Status: Phase 26 complete; ready to plan phase 27
Last activity: 2026-04-15 - Phase 26 warm-start perturbation diagnostics completed
Progress: [######----] 60% by completed phases (v1.4: 3/5 planned)

## Performance Metrics

**Velocity:**

- Total plans completed: Historical v1, v1.1, v1.2, and v1.3 phases complete; v1.4 has 3/5 phases complete
- Average duration: Not tracked
- Total execution time: Not tracked

**Recent Trend:**

- Trend: Unknown

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Research summary | `.planning/research/SUMMARY.md` | Complete |
| Requirements | `.planning/REQUIREMENTS.md` | Complete |
| Roadmap | `.planning/ROADMAP.md` | Complete |

## Current Milestone

**v1.4: Recovery Performance Improvements**

Goal: Improve real end-to-end recovery performance against the committed v1.3 standard/showcase baselines, then rerun the same campaigns to produce before/after evidence.

Target features:

- Baseline failure triage using v1.3 standard/showcase artifacts.
- Blind optimizer improvements for shallow formulas that currently snap but fail verification.
- Warm-start robustness improvements for stronger Beer-Lambert perturbations.
- Compiler depth/operator coverage improvements for selected FOR_DEMO formulas.
- Before/after campaign comparison reports using the same standard/showcase contracts.

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
| 16 | Experiment Matrix and Formula Coverage | Complete | MATR-01, MATR-02, MATR-03, MATR-04 |
| 17 | Evidence Aggregation and Report Contracts | Complete | EVID-01, EVID-02, EVID-03, EVID-04 |
| 18 | Smoke Tests, Docs, and Evidence Lockdown | Complete | TEST-05, TEST-06, TEST-07 |
| 19 | Campaign Presets and Run Manifests | Complete | CAMP-01, CAMP-02, CAMP-03, CAMP-04, CAMP-05 |
| 20 | Tidy CSV Export and Derived Metrics | Complete | DATA-01, DATA-02, DATA-03, DATA-04 |
| 21 | Static Plot Generation | Complete | PLOT-01, PLOT-02, PLOT-03, PLOT-04, PLOT-05, PLOT-06 |
| 22 | Evidence Report Assembly | Complete | REPT-01, REPT-02, REPT-03, REPT-04, REPT-05 |
| 23 | Campaign Smoke, Docs, and Report Lockdown | Complete | TEST-11, TEST-12, TEST-13 |
| 24 | Baseline Failure Triage and Diagnostic Harness | Complete | DIAG-01, DIAG-02, DIAG-03, DIAG-04 |
| 25 | Blind Optimizer Recovery Improvements | Complete | BLIND-01, BLIND-02, BLIND-03, BLIND-04 |
| 26 | Warm-Start Perturbation Robustness | Complete | PERT-01, PERT-02, PERT-03, PERT-04 |
| 27 | Compiler Coverage and Depth Reduction | Pending | COV-01, COV-02, COV-03, COV-04 |
| 28 | Before/After Campaign Evaluation | Pending | EVAL-01, EVAL-02, EVAL-03, EVAL-04, EVAL-05 |

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
- v1.3 continues phase numbering from v1.2 and maps 23 requirements across phases 19-23.
- Phase 19 added campaign presets, guarded output folders, manifest metadata, and the campaign CLI.
- Phase 20 added tidy CSV exports, grouped summaries, headline metrics, and failed/unsupported reason tables.
- Phase 21 added deterministic SVG plots for recovery, loss, perturbation behavior, runtime, and failure taxonomy.
- Phase 22 added self-contained campaign `report.md` assembly with metrics, links, limitations, and next experiments.
- Phase 23 added CLI/docs coverage, committed the v1.3 smoke campaign artifact, and verified the full test suite.
- v1.4 should change the measured performance, not the definition of `recovered`.
- v1.4 should use the committed v1.3 `standard` and `showcase` campaigns as before/after baselines.
- v1.4 maps 21 requirements across phases 24-28.

### Pending Todos

None recorded.

### Blockers/Concerns

None.

## Session Continuity

Last session: 2026-04-15
Stopped at: v1.4 roadmap created; ready for Phase 24 planning
Resume file: None

---
*Last updated: 2026-04-15 after creating milestone v1.4 roadmap*
