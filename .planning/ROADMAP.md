# Roadmap: EML Symbolic Regression

**Created:** 2026-04-16
**Updated:** 2026-04-16
**Granularity:** Coarse
**Mode:** YOLO
**Current milestone:** v1.7 Centered-Family Baseline and Paper Decision
**Coverage:** 20 v1.7 requirements mapped, 0 unmapped

## Overview

v1.6 established the current honest baseline: raw EML representation and verification are strong, scaffolded and perturbed-basin return are strong, but pure random blind recovery remains weak and depth-sensitive. v1.7 uses the existing proof harness as the baseline engine and tests whether centered/scaled exp-log transports improve that search geometry.

The milestone adds family-aware semantics and exact AST support for `cEML_{s,t}`, `CEML_s`, and `ZEML_s`, integrates those families with the soft master tree and recovery pipeline, reruns the proof/campaign matrix under raw-vs-centered variants, and ends with a paper decision memo. It must preserve raw EML as the baseline, keep evidence regimes separate, and avoid unproved completeness claims.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)
- **v1.5 Training Proof and Recovery Guarantees** - Phases 29-33 complete (completed 2026-04-16; archive: `.planning/milestones/v1.5-ROADMAP.md`)
- **v1.6 Hybrid Search Pipeline and Exact Candidate Recovery** - Phases 34-38 complete (completed 2026-04-16; archive: `.planning/milestones/v1.6-ROADMAP.md`)
- **v1.7 Centered-Family Baseline and Paper Decision** - Phases 39-43 planned

## Completed Milestone Context

| Phase Range | Milestone | Status | Archive |
|-------------|-----------|--------|---------|
| 1-7 | v1.0 MVP | Complete | Historical planning pre-archive |
| 8-13 | v1.1 EML Compiler and Warm Starts | Complete | `.planning/milestones/v1.1-ROADMAP.md` |
| 14-18 | v1.2 Training Benchmark and Recovery Evidence | Complete | `.planning/milestones/v1.2-ROADMAP.md` |
| 19-23 | v1.3 Benchmark Campaign and Evidence Report | Complete | `.planning/milestones/v1.3-ROADMAP.md` |
| 24-28 | v1.4 Recovery Performance Improvements | Complete | `.planning/milestones/v1.4-ROADMAP.md` |
| 29-33 | v1.5 Training Proof and Recovery Guarantees | Complete | `.planning/milestones/v1.5-ROADMAP.md` |
| 34-38 | v1.6 Hybrid Search Pipeline and Exact Candidate Recovery | Complete | `.planning/milestones/v1.6-ROADMAP.md` |

## Phases

**Phase Numbering:**
- v1.7 continues from completed Phase 38 and starts at Phase 39.
- Integer phases are planned milestone work.
- Decimal phases can be inserted later for urgent gap closure.

- [x] **Phase 39: Centered Operator Semantics and Exact Forms** - Add family-aware training and verification semantics plus exact AST support for raw EML, `cEML_{s,t}`, `CEML_s`, and `ZEML_s`. (requirements: OPF-01, OPF-02, OPF-03, OPF-04, OPF-05)
- [x] **Phase 40: Family-Aware Master Tree and Recovery Pipeline** - Thread fixed-family and scheduled-family choices through soft training, snapping, candidate ranking, compiler/warm-start paths, cleanup, repair, and refit. (requirements: TRN-01, TRN-02, TRN-03, TRN-04, TRN-05)
- [x] **Phase 41: Operator-Family Campaign Matrix** - Add reproducible raw-vs-centered proof and showcase campaign presets with isolated artifacts and family-aware manifests. (requirements: EVD-01, EVD-02)
- [x] **Phase 42: Comparative Evidence Aggregation and Regression Locks** - Produce family comparison tables, anomaly diagnostics, verifier/repair/refit summaries, and smoke/regression locks. (requirements: EVD-03, EVD-04, EVD-05)
- [ ] **Phase 43: Paper Decision Memo and Completeness Boundary** - Convert the comparison evidence into a publish/wait decision, safe claim language, figure inventory, and optional completeness-search boundary report. (requirements: PAP-01, PAP-02, PAP-03, PAP-04, PAP-05)

## Phase Details

### Phase 39: Centered Operator Semantics and Exact Forms
**Goal**: Users can represent, evaluate, serialize, and verify centered/scaled EML-family nodes without disturbing raw EML semantics.
**Depends on**: Phase 38
**Requirements**: OPF-01, OPF-02, OPF-03, OPF-04, OPF-05
**Success Criteria** (what must be TRUE):
  1. Semantics APIs support raw EML, `cEML_{s,t}`, `CEML_s`, and `ZEML_s` with explicit training and verification modes.
  2. Centered-family implementations use `expm1` and `log1p`, preserve PyTorch `complex128` defaults, and keep training guards separate from faithful verification.
  3. Exact AST JSON records operator family, `s`, `t`, terminal convention, and children, and round-trips deterministically.
  4. SymPy and mpmath evaluation paths cover centered-family exact ASTs and are tested against backend semantics.
  5. Anomaly diagnostics report non-finites, overflow pressure, branch/domain events, and shifted-singularity distance for centered nodes.

### Phase 40: Family-Aware Master Tree and Recovery Pipeline
**Goal**: Users can run the existing differentiable recovery pipeline under raw or centered operator families while preserving raw-EML defaults and fallback behavior.
**Depends on**: Phase 39
**Requirements**: TRN-01, TRN-02, TRN-03, TRN-04, TRN-05
**Success Criteria** (what must be TRUE):
  1. Training can select a fixed operator family per run, including raw EML and declared `CEML_s`/`ZEML_s` scales.
  2. Snapping, exact-candidate pooling, verifier ranking, cleanup, repair, and refit operate on centered-family exact ASTs with provenance.
  3. Compiler and warm-start support either emit validated centered-family trees or fail closed with clear diagnostics.
  4. Scheduled `s` continuation runs preserve schedule metadata and can reproduce declared schedules such as `8 -> 4 -> 2 -> 1` and `8 -> 4`.
  5. Regression tests prove raw EML behavior and archived v1.6 command contracts remain unchanged by the family-aware implementation.

### Phase 41: Operator-Family Campaign Matrix
**Goal**: Users can run raw-vs-centered proof and showcase campaign matrices without overwriting archived v1.6 evidence.
**Depends on**: Phase 40
**Requirements**: EVD-01, EVD-02
**Success Criteria** (what must be TRUE):
  1. `proof-shallow-pure-blind`, `proof-shallow`, `proof-basin`, and `proof-depth-curve` can run under selected raw, `CEML_s`, `ZEML_s`, and continuation variants.
  2. Standard/showcase style campaign presets support the same operator-family variants with isolated output roots.
  3. Run manifests record operator family, scale, shift, terminal convention, continuation schedule, budget, seeds, and recovery regime.
  4. Campaign reports keep pure blind, scaffolded, compile-only, warm-start, repaired, and perturbed-basin evidence separate for every operator family.

### Phase 42: Comparative Evidence Aggregation and Regression Locks
**Goal**: Users can compare raw EML and centered-family behavior through aggregate evidence instead of individual run inspection.
**Depends on**: Phase 41
**Requirements**: EVD-03, EVD-04, EVD-05
**Success Criteria** (what must be TRUE):
  1. Aggregates report exact recovery rate by regime, depth, operator family, scale, continuation schedule, and target formula.
  2. Diagnostics summarize anomaly rates, post-snap verifier pass rate, repair/refit usage, and depth or node-count overhead.
  3. Reports compare centered-family results against archived v1.6 raw-EML anchors without overwriting those artifacts.
  4. Smoke and regression tests cover family-aware evidence commands, raw EML default behavior, and reporting contract stability.
  5. A v1.7 proof/evidence bundle records the operator-family comparison with reproducible commands and manifest-level provenance.

### Phase 43: Paper Decision Memo and Completeness Boundary
**Goal**: Users can make a publication decision from the centered-family evidence with safe claims and explicit boundaries.
**Depends on**: Phase 42
**Requirements**: PAP-01, PAP-02, PAP-03, PAP-04, PAP-05
**Success Criteria** (what must be TRUE):
  1. Decision memo recommends either publishing a robustness/geometry paper now or waiting for stronger successor-family evidence, with thresholds tied to v1.7 results.
  2. Safe claim language covers centering, local Jacobian normalization, curvature control, shifted singularity, and subtraction-limit behavior.
  3. Unsafe claim warnings explicitly cover unproved `CEML_s` completeness, `ZEML_s` zero-terminal limitations, universal recovery, and pocket-calculator replacement claims.
  4. Figure/table inventory identifies the headline exact-recovery-versus-depth comparison and supporting anomaly, verifier, repair/refit, and overhead tables.
  5. Any constructive completeness or interdefinability search outputs for `CEML_s` are inspectable and labeled as experimental or incomplete unless fully verified.

## Dependency Order

```text
Phase 38 -> Phase 39 -> Phase 40 -> Phase 41 -> Phase 42 -> Phase 43
```

Phase 39 establishes the mathematical and artifact representation for centered-family nodes. Phase 40 integrates those nodes into the train/snap/verify pipeline. Phase 41 turns the integration into reproducible campaigns. Phase 42 aggregates the comparison and locks regressions. Phase 43 converts the evidence into paper-facing claims, boundaries, and the next-milestone decision.

## Requirement Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| OPF-01 | Phase 39 | Complete |
| OPF-02 | Phase 39 | Complete |
| OPF-03 | Phase 39 | Complete |
| OPF-04 | Phase 39 | Complete |
| OPF-05 | Phase 39 | Complete |
| TRN-01 | Phase 40 | Complete |
| TRN-02 | Phase 40 | Complete |
| TRN-03 | Phase 40 | Complete |
| TRN-04 | Phase 40 | Complete |
| TRN-05 | Phase 40 | Complete |
| EVD-01 | Phase 41 | Complete |
| EVD-02 | Phase 41 | Complete |
| EVD-03 | Phase 42 | Complete |
| EVD-04 | Phase 42 | Complete |
| EVD-05 | Phase 42 | Complete |
| PAP-01 | Phase 43 | Pending |
| PAP-02 | Phase 43 | Pending |
| PAP-03 | Phase 43 | Pending |
| PAP-04 | Phase 43 | Pending |
| PAP-05 | Phase 43 | Pending |

**Coverage:** 20/20 v1.7 requirements mapped. No orphaned requirements. No duplicate phase assignments.

## Progress

**Execution Order:** Phase 39 -> Phase 40 -> Phase 41 -> Phase 42 -> Phase 43

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1-7. v1.0 MVP | Complete | Complete | 2026-04-15 |
| 8-13. v1.1 EML Compiler and Warm Starts | Complete | Complete | 2026-04-15 |
| 14-18. v1.2 Training Benchmark and Recovery Evidence | Complete | Complete | 2026-04-15 |
| 19-23. v1.3 Benchmark Campaign and Evidence Report | Complete | Complete | 2026-04-15 |
| 24-28. v1.4 Recovery Performance Improvements | Complete | Complete | 2026-04-15 |
| 29-33. v1.5 Training Proof and Recovery Guarantees | Complete | Complete | 2026-04-16 |
| 34-38. v1.6 Hybrid Search Pipeline and Exact Candidate Recovery | Complete | Complete | 2026-04-16 |
| 39. Centered Operator Semantics and Exact Forms | 1/1 | Complete | 2026-04-16 |
| 40. Family-Aware Master Tree and Recovery Pipeline | 1/1 | Complete | 2026-04-16 |
| 41. Operator-Family Campaign Matrix | 1/1 | Complete | 2026-04-16 |
| 42. Comparative Evidence Aggregation and Regression Locks | 1/1 | Complete | 2026-04-16 |
| 43. Paper Decision Memo and Completeness Boundary | 0/1 | Pending | - |

---
*Roadmap updated: 2026-04-16 after completing Phase 42*
