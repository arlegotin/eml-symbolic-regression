# Roadmap: EML Symbolic Regression

**Created:** 2026-04-15
**Updated:** 2026-04-15
**Granularity:** Coarse
**Mode:** YOLO
**Current milestone:** v1.2 Training Benchmark and Recovery Evidence
**Coverage:** 19 v1.2 requirements mapped, 0 unmapped

## Overview

v1.0 established exact EML semantics, soft master trees, optimizer, verifier, cleanup, demos, tests, and documentation. v1.1 added compiler-driven warm starts, exact AST embedding, deterministic perturbation manifests, and honest demo claim reporting.

v1.2 turns the current training evidence into a repeatable benchmark system. The milestone measures blind starts, compiler warm starts, perturbation sweeps, unsupported/stretch diagnostics, and verifier-owned recovery rates so future optimizer work is guided by aggregate evidence rather than individual success cases.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 planned

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

## Phases

**Phase Numbering:**
- Integer phases (14, 15, 16): Planned milestone work
- Decimal phases (14.1, 14.2): Urgent insertions, if needed later
- v1.2 continues from completed Phase 13 and starts at Phase 14

- [x] **Phase 14: Benchmark Contract and Suite Registry** - Define deterministic benchmark suite schemas, built-in suite registry, validation, and artifact identity. (completed 2026-04-15)
- [x] **Phase 15: Benchmark Runner and Training Modes** - Run suites and filtered subsets through existing blind-start and compiler warm-start paths while preserving failures. (completed 2026-04-15)
- [x] **Phase 16: Experiment Matrix and Formula Coverage** - Add the actual v1.2 formula/start/seed/perturbation matrix for shallow baselines, Beer-Lambert, Michaelis-Menten, Planck, and selected demo diagnostics. (completed 2026-04-15)
- [x] **Phase 17: Evidence Aggregation and Report Contracts** - Aggregate run artifacts into JSON and Markdown reports with recovery rates, failure classes, and provenance. (completed 2026-04-15)
- [x] **Phase 18: Smoke Tests, Docs, and Evidence Lockdown** - Lock benchmark parsing, smoke execution, aggregation math, claim taxonomy, and user-facing interpretation docs. (completed 2026-04-15)

## Phase Details

### Phase 14: Benchmark Contract and Suite Registry
**Goal**: Users can define, validate, and select deterministic benchmark suites before any training runs.
**Depends on**: Phase 13
**Requirements**: BENC-01, BENC-02, BENC-03, BENC-04
**Success Criteria** (what must be TRUE):
  1. User can define suite files with formula IDs, datasets, ranges, sample counts, start modes, seeds, perturbation levels, optimizer budgets, verifier settings, and artifact paths.
  2. User can select built-in suites for smoke checks, the full v1.2 evidence matrix, and `sources/FOR_DEMO.md` diagnostics.
  3. Invalid suite files fail closed with actionable validation errors before training starts.
  4. Every planned run has a stable run ID and deterministic artifact location.
**Plans**: TBD

### Phase 15: Benchmark Runner and Training Modes
**Goal**: Users can execute benchmark suites through existing training paths without hand-writing demo commands.
**Depends on**: Phase 14
**Requirements**: RUN-01, RUN-02, RUN-03, RUN-04
**Success Criteria** (what must be TRUE):
  1. User can run a full suite or filtered subset from the CLI.
  2. Blind-start runs call the existing optimizer across multiple seeds for shallow supported formulas.
  3. Compiler warm-start runs use the existing compile, embed, perturb, train, snap, and verify path.
  4. Unsupported, skipped, failed, and errored cases are recorded as run outcomes without aborting the whole suite.
**Plans**: TBD

### Phase 16: Experiment Matrix and Formula Coverage
**Goal**: Users can run the v1.2 evidence matrix that tests shallow blind recovery, Beer-Lambert perturbation robustness, and honest diagnostics for harder demos.
**Depends on**: Phase 15
**Requirements**: MATR-01, MATR-02, MATR-03, MATR-04
**Success Criteria** (what must be TRUE):
  1. The matrix includes blind-start baselines for shallow formulas such as `exp`, `log`, radioactive decay, and other low-depth formulas supported by current gates.
  2. Beer-Lambert runs include same-basin, mild perturbation, and stronger slot-changing perturbation settings.
  3. Michaelis-Menten runs record compiler depth, embedding eligibility, unsupported reasons, and training attempts only when current gates allow them.
  4. Normalized Planck and selected `sources/FOR_DEMO.md` formulas appear as stretch or diagnostic cases without requiring recovery.
**Plans**: TBD

### Phase 17: Evidence Aggregation and Report Contracts
**Goal**: Users can understand benchmark performance through aggregate evidence rather than isolated run artifacts.
**Depends on**: Phase 16
**Requirements**: EVID-01, EVID-02, EVID-03, EVID-04
**Success Criteria** (what must be TRUE):
  1. Each run JSON includes suite ID, run ID, formula, dataset spec, start mode, seed, perturbation config, optimizer config, losses, snap outcome, active slot changes, verifier status, timing, and errors.
  2. Aggregate JSON and Markdown reports compute recovery rates by formula, start mode, perturbation level, depth, and seed group.
  3. Reports separate blind recovery, same-AST warm-start return, verified-equivalent warm-start recovery, snapped-but-failed candidates, soft-fit-only attempts, unsupported cases, and execution failures.
  4. Reports preserve provenance for suite config, code version, environment summary, and artifact paths.
**Plans**: TBD

### Phase 18: Smoke Tests, Docs, and Evidence Lockdown
**Goal**: Users can trust the benchmark contract and interpret evidence without confusing failures or same-AST returns for discovery.
**Depends on**: Phase 17
**Requirements**: TEST-05, TEST-06, TEST-07
**Success Criteria** (what must be TRUE):
  1. Pytest coverage locks suite parsing, validation, stable run IDs, aggregation math, and claim taxonomy.
  2. A CI-scale benchmark smoke test exercises one blind-start run, one warm-start run, one unsupported/stretch diagnostic, and one aggregate report.
  3. Documentation explains how to run suites, read recovery evidence, and interpret limitations.
  4. Documentation and tests prevent any report from labeling a candidate `recovered` without verifier-owned recovery evidence.
**Plans**: TBD

## Dependency Order

```text
Phase 14 -> Phase 15 -> Phase 16 -> Phase 17 -> Phase 18
```

The order is intentionally linear. Suite contracts and run identity must exist before execution; execution must exist before the full experiment matrix; aggregation needs real artifacts; tests and docs lock the resulting evidence contract.

## Requirement Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| BENC-01 | Phase 14 | Complete |
| BENC-02 | Phase 14 | Complete |
| BENC-03 | Phase 14 | Complete |
| BENC-04 | Phase 14 | Complete |
| RUN-01 | Phase 15 | Complete |
| RUN-02 | Phase 15 | Complete |
| RUN-03 | Phase 15 | Complete |
| RUN-04 | Phase 15 | Complete |
| MATR-01 | Phase 16 | Complete |
| MATR-02 | Phase 16 | Complete |
| MATR-03 | Phase 16 | Complete |
| MATR-04 | Phase 16 | Complete |
| EVID-01 | Phase 17 | Complete |
| EVID-02 | Phase 17 | Complete |
| EVID-03 | Phase 17 | Complete |
| EVID-04 | Phase 17 | Complete |
| TEST-05 | Phase 18 | Complete |
| TEST-06 | Phase 18 | Complete |
| TEST-07 | Phase 18 | Complete |

**Coverage:** 19/19 v1.2 requirements mapped. No orphaned requirements. No duplicate phase assignments.

## Progress

**Execution Order:** Phase 14 -> Phase 15 -> Phase 16 -> Phase 17 -> Phase 18

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
| 14. Benchmark Contract and Suite Registry | 1/1 | Complete | 2026-04-15 |
| 15. Benchmark Runner and Training Modes | 1/1 | Complete | 2026-04-15 |
| 16. Experiment Matrix and Formula Coverage | 1/1 | Complete | 2026-04-15 |
| 17. Evidence Aggregation and Report Contracts | 1/1 | Complete | 2026-04-15 |
| 18. Smoke Tests, Docs, and Evidence Lockdown | 1/1 | Complete | 2026-04-15 |

---
*Roadmap updated: 2026-04-15 for milestone v1.2*
