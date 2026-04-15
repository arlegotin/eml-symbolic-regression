# Roadmap: EML Symbolic Regression

**Created:** 2026-04-15
**Updated:** 2026-04-15
**Granularity:** Coarse
**Mode:** YOLO
**Current milestone:** v1.3 Benchmark Campaign and Evidence Report
**Coverage:** 23 v1.3 requirements mapped, 0 unmapped

## Overview

v1.0 established exact EML semantics, soft master trees, optimizer, verifier, cleanup, demos, tests, and documentation. v1.1 added compiler-driven warm starts, exact AST embedding, deterministic perturbation manifests, and honest demo claim reporting. v1.2 added repeatable benchmark suites, run artifacts, aggregate evidence reports, and smoke benchmark artifacts.

v1.3 turns the benchmark harness into a polished showcase: run a real campaign, export tidy tables, generate static figures, and assemble a self-contained evidence report that explains how the paper's EML idea performs in this implementation.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 planned

## Completed Milestone Context

| Phase | Name | Status |
|-------|------|--------|
| 1 | Semantics, AST, and Deterministic Artifacts | Complete |
| 2 | Complete Master Trees and Soft Evaluation | Complete |
| 3 | Optimizer, Restarts, Hardening, and Recovery Statuses | Complete |
| 4 | Verifier and Acceptance Contract | Complete |
| 5 | Local Cleanup, SymPy Export, and Reports | Complete |
| 6 | Demo Harness and Public Showcase | Complete |
| 7 | Tests and Documentation | Complete |
| 8 | Compiler Contract and Direct Rules | Complete |
| 9 | Constant Catalog and AST Embedding | Complete |
| 10 | Arithmetic Rule Corpus and Depth Gates | Complete |
| 11 | Perturbed Warm-Start Training | Complete |
| 12 | Demo Promotion and Claim Reporting | Complete |
| 13 | Regression Tests and Documentation Lockdown | Complete |
| 14 | Benchmark Contract and Suite Registry | Complete |
| 15 | Benchmark Runner and Training Modes | Complete |
| 16 | Experiment Matrix and Formula Coverage | Complete |
| 17 | Evidence Aggregation and Report Contracts | Complete |
| 18 | Smoke Tests, Docs, and Evidence Lockdown | Complete |

## Phases

**Phase Numbering:**
- Integer phases (19, 20, 21): Planned milestone work
- Decimal phases (19.1, 19.2): Urgent insertions, if needed later
- v1.3 continues from completed Phase 18 and starts at Phase 19

- [ ] **Phase 19: Campaign Presets and Run Manifests** - Add named campaign presets, budget tiers, output-folder guardrails, and manifest metadata. (requirements: CAMP-01, CAMP-02, CAMP-03, CAMP-04, CAMP-05)
- [ ] **Phase 20: Tidy CSV Export and Derived Metrics** - Export run-level and grouped CSV tables plus headline metrics for analysis and plotting. (requirements: DATA-01, DATA-02, DATA-03, DATA-04)
- [ ] **Phase 21: Static Plot Generation** - Generate deterministic static figures for recovery, losses, perturbation sensitivity, runtime/depth, and failure taxonomy. (requirements: PLOT-01, PLOT-02, PLOT-03, PLOT-04, PLOT-05, PLOT-06)
- [ ] **Phase 22: Evidence Report Assembly** - Assemble a self-contained campaign report with figures, tables, commands, narrative, limitations, and next experiments. (requirements: REPT-01, REPT-02, REPT-03, REPT-04, REPT-05)
- [ ] **Phase 23: Campaign Smoke, Docs, and Report Lockdown** - Lock campaign presets, CSV export, plots, report assembly, and documentation with CI-scale tests. (requirements: TEST-11, TEST-12, TEST-13)

## Phase Details

### Phase 19: Campaign Presets and Run Manifests
**Goal**: Users can run named benchmark campaign presets into reproducible output folders without manually composing filters and budgets.
**Depends on**: Phase 18
**Requirements**: CAMP-01, CAMP-02, CAMP-03, CAMP-04, CAMP-05
**Success Criteria** (what must be TRUE):
  1. User can choose `smoke`, `standard`, or `showcase` campaign presets that map to suites, filters, budget tiers, seeds, and output roots.
  2. User receives a versioned campaign output directory containing raw run artifacts, aggregate outputs, and a campaign manifest.
  3. The standard preset includes shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten diagnostics, Planck diagnostics, and selected FOR_DEMO cases.
  4. Re-running a campaign cannot silently overwrite prior evidence unless the user explicitly opts in.
  5. Runtime and budget guardrails make the difference between smoke, standard, and showcase campaigns clear.
**Plans**: TBD

### Phase 20: Tidy CSV Export and Derived Metrics
**Goal**: Users can analyze benchmark results through flat CSV tables and headline metric summaries.
**Depends on**: Phase 19
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04
**Success Criteria** (what must be TRUE):
  1. Run-level CSV includes formula, start mode, seed, depth, steps, perturbation noise, best loss, post-snap loss, verifier status, recovery class, runtime, changed slots, and artifact path.
  2. Grouped CSV summaries report recovery rates by formula, start mode, perturbation level, depth, and failure class.
  3. Headline metrics JSON/CSV summarize total runs, recovery, unsupported/failure rates, same-AST rate, median losses, and runtimes.
  4. Unsupported and failed cases include reason codes and source artifact links.
**Plans**: TBD

### Phase 21: Static Plot Generation
**Goal**: Users can generate crisp, deterministic figures from campaign CSV/aggregate data.
**Depends on**: Phase 20
**Requirements**: PLOT-01, PLOT-02, PLOT-03, PLOT-04, PLOT-05, PLOT-06
**Success Criteria** (what must be TRUE):
  1. Recovery-rate plots compare formulas and start modes without merging blind recovery and same-AST warm-start return.
  2. Loss plots show best soft loss versus post-snap loss on appropriate scales.
  3. Beer-Lambert perturbation plots show recovery class and changed-slot behavior by noise level.
  4. Runtime and depth/budget plots make practical cost visible.
  5. Failure-taxonomy plots show unsupported and failed cases by formula and class.
  6. Figure filenames are stable and suitable for Markdown linking.
**Plans**: TBD

### Phase 22: Evidence Report Assembly
**Goal**: Users receive a self-contained benchmark evidence report suitable for explaining the original paper's practical performance.
**Depends on**: Phase 21
**Requirements**: REPT-01, REPT-02, REPT-03, REPT-04, REPT-05
**Success Criteria** (what must be TRUE):
  1. Campaign folder contains `report.md` with headline metrics, tables, figures, exact commands, and links to raw artifacts.
  2. Report narrative clearly explains what EML demonstrates well in this implementation.
  3. Limitations separate blind recovery, same-AST warm-start return, verified-equivalent warm-start recovery, unsupported gates, and failed fits.
  4. Report includes next experiments that translate measured failures into optimizer or compiler priorities.
  5. A documented single CLI command can reproduce the report from a clean checkout.
**Plans**: TBD

### Phase 23: Campaign Smoke, Docs, and Report Lockdown
**Goal**: Users can trust the campaign/report workflow and understand how to present the results honestly.
**Depends on**: Phase 22
**Requirements**: TEST-11, TEST-12, TEST-13
**Success Criteria** (what must be TRUE):
  1. Focused tests cover campaign preset expansion, output folder creation, overwrite protection, CSV export, and headline metrics.
  2. Focused tests cover plot file generation and report assembly using CI-scale fixtures.
  3. Documentation describes campaign commands, output structure, CSV schemas, plot meanings, and honest presentation rules.
  4. Full pytest passes after report workflow integration.
**Plans**: TBD

## Dependency Order

```text
Phase 19 -> Phase 20 -> Phase 21 -> Phase 22 -> Phase 23
```

The order is intentionally linear. Campaign presets define where evidence lives; CSV export turns evidence into analyzable tables; plots consume the tables; the report assembles figures and narrative; tests and docs lock the workflow.

## Requirement Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| CAMP-01 | Phase 19 | Pending |
| CAMP-02 | Phase 19 | Pending |
| CAMP-03 | Phase 19 | Pending |
| CAMP-04 | Phase 19 | Pending |
| CAMP-05 | Phase 19 | Pending |
| DATA-01 | Phase 20 | Pending |
| DATA-02 | Phase 20 | Pending |
| DATA-03 | Phase 20 | Pending |
| DATA-04 | Phase 20 | Pending |
| PLOT-01 | Phase 21 | Pending |
| PLOT-02 | Phase 21 | Pending |
| PLOT-03 | Phase 21 | Pending |
| PLOT-04 | Phase 21 | Pending |
| PLOT-05 | Phase 21 | Pending |
| PLOT-06 | Phase 21 | Pending |
| REPT-01 | Phase 22 | Pending |
| REPT-02 | Phase 22 | Pending |
| REPT-03 | Phase 22 | Pending |
| REPT-04 | Phase 22 | Pending |
| REPT-05 | Phase 22 | Pending |
| TEST-11 | Phase 23 | Pending |
| TEST-12 | Phase 23 | Pending |
| TEST-13 | Phase 23 | Pending |

**Coverage:** 23/23 v1.3 requirements mapped. No orphaned requirements. No duplicate phase assignments.

## Progress

**Execution Order:** Phase 19 -> Phase 20 -> Phase 21 -> Phase 22 -> Phase 23

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Semantics, AST, and Deterministic Artifacts | Complete | Complete | 2026-04-15 |
| 2. Complete Master Trees and Soft Evaluation | Complete | Complete | 2026-04-15 |
| 3. Optimizer, Restarts, Hardening, and Recovery Statuses | Complete | Complete | 2026-04-15 |
| 4. Verifier and Acceptance Contract | Complete | Complete | 2026-04-15 |
| 5. Local Cleanup, SymPy Export, and Reports | Complete | Complete | 2026-04-15 |
| 6. Demo Harness and Public Showcase | Complete | Complete | 2026-04-15 |
| 7. Tests and Documentation | Complete | Complete | 2026-04-15 |
| 8. Compiler Contract and Direct Rules | Complete | Complete | 2026-04-15 |
| 9. Constant Catalog and AST Embedding | Complete | Complete | 2026-04-15 |
| 10. Arithmetic Rule Corpus and Depth Gates | Complete | Complete | 2026-04-15 |
| 11. Perturbed Warm-Start Training | Complete | Complete | 2026-04-15 |
| 12. Demo Promotion and Claim Reporting | Complete | Complete | 2026-04-15 |
| 13. Regression Tests and Documentation Lockdown | Complete | Complete | 2026-04-15 |
| 14. Benchmark Contract and Suite Registry | Complete | Complete | 2026-04-15 |
| 15. Benchmark Runner and Training Modes | Complete | Complete | 2026-04-15 |
| 16. Experiment Matrix and Formula Coverage | Complete | Complete | 2026-04-15 |
| 17. Evidence Aggregation and Report Contracts | Complete | Complete | 2026-04-15 |
| 18. Smoke Tests, Docs, and Evidence Lockdown | Complete | Complete | 2026-04-15 |
| 19. Campaign Presets and Run Manifests | 0/1 | Pending | - |
| 20. Tidy CSV Export and Derived Metrics | 0/1 | Pending | - |
| 21. Static Plot Generation | 0/1 | Pending | - |
| 22. Evidence Report Assembly | 0/1 | Pending | - |
| 23. Campaign Smoke, Docs, and Report Lockdown | 0/1 | Pending | - |

---
*Roadmap updated: 2026-04-15 for milestone v1.3*
