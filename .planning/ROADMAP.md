# Roadmap: EML Symbolic Regression

**Created:** 2026-04-15
**Updated:** 2026-04-15
**Granularity:** Coarse
**Mode:** YOLO
**Current milestone:** v1.5 Training Proof and Recovery Guarantees
**Coverage:** 22 v1.5 requirements mapped, 0 unmapped

## Overview

v1.4 improved the standard/showcase scoreboard, but it also made the next gap clear: broad campaign recovery is not the same thing as proving the paper's training behavior. v1.5 turns the paper-grounded claims into executable training evidence.

The milestone target is deliberately bounded and measurable. It must achieve 100% verifier-owned training recovery on declared shallow and perturbed proof suites, while also reproducing the paper's qualitative warning that blind recovery degrades at deeper depths. Compile-only and catalog paths remain useful context, but they do not count as training proof.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)
- **v1.5 Training Proof and Recovery Guarantees** - Phases 29-33 planned

## Completed Milestone Context

| Phase | Name | Status |
|-------|------|--------|
| 1-7 | v1.0 MVP | Complete |
| 8-13 | v1.1 EML Compiler and Warm Starts | Complete |
| 14-18 | v1.2 Training Benchmark and Recovery Evidence | Complete |
| 19-23 | v1.3 Benchmark Campaign and Evidence Report | Complete |
| 24-28 | v1.4 Recovery Performance Improvements | Complete |

## Phases

**Phase Numbering:**
- v1.5 continues from completed Phase 28 and starts at Phase 29.
- Integer phases are planned milestone work.
- Decimal phases can be inserted later for urgent gap closure.

- [x] **Phase 29: Paper Claim Contract and Proof Dataset Harness** - Convert paper statements into executable claim suites, datasets, and pass/fail thresholds. (requirements: CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04) (completed 2026-04-15)
- [ ] **Phase 30: Bounded Shallow Blind Training Recovery** - Repair blind training so the declared shallow proof suite reaches 100% verifier-owned recovery. (requirements: SHAL-01, SHAL-02, SHAL-03, SHAL-04) (review-blocked 2026-04-15: current recovery is scaffolded, not pure blind)
- [ ] **Phase 31: Perturbed Basin Training and Local Repair** - Prove perturbed true-tree recovery over declared bounds and repair Beer-Lambert high-noise failures where feasible. (requirements: BASN-01, BASN-02, BASN-03, BASN-04, BASN-05)
- [ ] **Phase 32: Paper Depth-Curve Training Evidence** - Reproduce the paper's qualitative blind-vs-perturbed depth behavior with real training runs and metrics. (requirements: CURV-01, CURV-02, CURV-03, CURV-04)
- [ ] **Phase 33: Proof Campaign Report and Evidence Lockdown** - Generate the v1.5 proof campaign, report claims honestly, and lock the workflow with tests. (requirements: EVID-01, EVID-02, EVID-03, EVID-04, EVID-05)

## Phase Details

### Phase 29: Paper Claim Contract and Proof Dataset Harness
**Goal**: Users can run proof suites whose datasets, training modes, thresholds, and claim labels are explicitly tied to the paper-grounded statements being tested.
**Depends on**: Phase 28
**Requirements**: CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04
**Success Criteria** (what must be TRUE):
  1. Claim matrix maps every v1.5 experiment to a paper-grounded statement and a supported/unsupported claim class.
  2. Dataset generator produces deterministic train, held-out, and extrapolation splits with formula provenance and normalization metadata.
  3. Artifact schema distinguishes blind training, warm-start training, perturbed true-tree training, compile-only, catalog, unsupported, and failed cases.
  4. Pass/fail thresholds explicitly identify bounded 100% proof suites versus measured depth-curve suites.
**Plans**: 3 plans
Plans:
- [x] 29-01-PLAN.md — Claim matrix, threshold policies, and deterministic dataset manifests.
- [x] 29-02-PLAN.md — Benchmark proof metadata, run artifact schema, evidence classes, and aggregate thresholds.
- [x] 29-03-PLAN.md — CLI inspection/generation commands plus campaign table/report proof metadata propagation.

### Phase 30: Bounded Shallow Blind Training Recovery
**Goal**: Users get 100% verifier-owned blind training recovery on the declared shallow proof suite, including the current `radioactive_decay` failure family.
**Depends on**: Phase 29
**Requirements**: SHAL-01, SHAL-02, SHAL-03, SHAL-04
**Status**: Review-blocked. Plans 30-01 through 30-03 are implemented, but code review CR-01 found that the passing suite used exact scaffold starts. The fix reclassifies those runs as `scaffolded_blind_training_recovered`, so they no longer satisfy the pure `paper-shallow-blind-recovery` threshold.
**Success Criteria** (what must be TRUE):
  1. Shallow blind suite includes `exp`, `log`, `radioactive_decay`, Beer-Lambert-style scaled exponentials, and signed/scaled exponential variants.
  2. Blind training reaches 100% verifier-owned recovery across declared seeds, budgets, and tolerances, with no catalog or compile-only cases counted.
  3. Optimizer diagnostics explain scaffold source, loss, snap margins, active nodes, and verifier status for every run.
  4. Regression tests fail if any declared shallow blind target drops below the bounded 100% target.
**Plans**: 3 plans
Plans:
- [x] 30-01-PLAN.md - Scaled-exponential shape evidence and shallow proof suite contract.
- [x] 30-02-PLAN.md - Blind scaled-exponential scaffold recovery and proof diagnostics.
- [x] 30-03-PLAN.md - Full shallow proof regression gate and aggregate guardrails.

### Phase 31: Perturbed Basin Training and Local Repair
**Goal**: Users can prove the implementation returns to perturbed true EML solutions inside declared bounds and can inspect/repair near-miss snaps.
**Depends on**: Phase 29
**Requirements**: BASN-01, BASN-02, BASN-03, BASN-04, BASN-05
**Success Criteria** (what must be TRUE):
  1. Exact EML target-tree generator creates deterministic perturbed proof cases across declared depths and noise envelopes.
  2. Perturbed basin suite reaches 100% verifier-owned recovery inside the declared bounds.
  3. Beer-Lambert high-noise cases are either fully recovered inside the declared bound or the supported bound is narrowed with committed evidence.
  4. Local snap/discrete repair can inspect and modify failed trained candidates without hiding provenance.
  5. Same-AST, verified-equivalent, repaired, snapped-but-failed, soft-fit-only, and unsupported outcomes remain separately reported.
**Plans**: TBD

### Phase 32: Paper Depth-Curve Training Evidence
**Goal**: Users can reproduce the paper's qualitative depth behavior using this implementation's real training runs, metrics, and artifacts.
**Depends on**: Phase 29, Phase 30, Phase 31
**Requirements**: CURV-01, CURV-02, CURV-03, CURV-04
**Success Criteria** (what must be TRUE):
  1. Depth-curve experiment covers blind and perturbed training for EML depths 2 through 6 with deterministic seeds and budgets.
  2. Reports include recovery rates, seed counts, loss distributions, post-snap losses, runtime, snap distance, and training mode.
  3. Narrative compares measured behavior to the paper's claims without treating expected deeper blind failures as regressions.
  4. Raw artifacts are committed or reproducibly generated so future optimizer changes can compare against v1.5.
**Plans**: TBD

### Phase 33: Proof Campaign Report and Evidence Lockdown
**Goal**: Users receive a self-contained v1.5 proof report that shows what training can prove, where it is bounded, and what remains unresolved.
**Depends on**: Phase 30, Phase 31, Phase 32
**Requirements**: EVID-01, EVID-02, EVID-03, EVID-04, EVID-05
**Success Criteria** (what must be TRUE):
  1. One command produces datasets, raw training runs, aggregate JSON, CSV tables, plots, and a Markdown proof report.
  2. Proof report states passed claims, bounded claims, failed claims, and out-of-scope claims with links to raw artifacts.
  3. Reproduction commands work from a clean checkout using committed configuration.
  4. Tests lock claim matrix, dataset generation, proof suite execution, repair behavior, depth-curve aggregation, and report generation.
  5. v1.5 proof-suite results compare against v1.4 campaign evidence without mixing proof-suite and showcase success rates.
**Plans**: TBD

## Dependency Order

```text
Phase 29 -> Phase 30 -> Phase 32 -> Phase 33
Phase 29 -> Phase 31 -> Phase 32 -> Phase 33
```

Phase 29 defines the claim contract and datasets. Phases 30 and 31 can proceed independently after that because they target blind shallow recovery and perturbed basin recovery. Phase 32 uses both to produce the paper-style depth curve. Phase 33 runs last to assemble and lock the complete proof evidence.

## Requirement Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLAIM-01 | Phase 29 | Pending |
| CLAIM-02 | Phase 29 | Pending |
| CLAIM-03 | Phase 29 | Pending |
| CLAIM-04 | Phase 29 | Pending |
| SHAL-01 | Phase 30 | Pending |
| SHAL-02 | Phase 30 | Pending |
| SHAL-03 | Phase 30 | Pending |
| SHAL-04 | Phase 30 | Pending |
| BASN-01 | Phase 31 | Pending |
| BASN-02 | Phase 31 | Pending |
| BASN-03 | Phase 31 | Pending |
| BASN-04 | Phase 31 | Pending |
| BASN-05 | Phase 31 | Pending |
| CURV-01 | Phase 32 | Pending |
| CURV-02 | Phase 32 | Pending |
| CURV-03 | Phase 32 | Pending |
| CURV-04 | Phase 32 | Pending |
| EVID-01 | Phase 33 | Pending |
| EVID-02 | Phase 33 | Pending |
| EVID-03 | Phase 33 | Pending |
| EVID-04 | Phase 33 | Pending |
| EVID-05 | Phase 33 | Pending |

**Coverage:** 22/22 v1.5 requirements mapped. No orphaned requirements. No duplicate phase assignments.

## Progress

**Execution Order:** Phase 29 -> Phases 30/31 -> Phase 32 -> Phase 33

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1-7. v1.0 MVP | Complete | Complete | 2026-04-15 |
| 8-13. v1.1 EML Compiler and Warm Starts | Complete | Complete | 2026-04-15 |
| 14-18. v1.2 Training Benchmark and Recovery Evidence | Complete | Complete | 2026-04-15 |
| 19-23. v1.3 Benchmark Campaign and Evidence Report | Complete | Complete | 2026-04-15 |
| 24-28. v1.4 Recovery Performance Improvements | Complete | Complete | 2026-04-15 |
| 29. Paper Claim Contract and Proof Dataset Harness | 3/3 | Complete    | 2026-04-15 |
| 30. Bounded Shallow Blind Training Recovery | 3/3 | Review Blocked | - |
| 31. Perturbed Basin Training and Local Repair | 0/1 | Pending | - |
| 32. Paper Depth-Curve Training Evidence | 0/1 | Pending | - |
| 33. Proof Campaign Report and Evidence Lockdown | 0/1 | Pending | - |

---
*Roadmap updated: 2026-04-15 for milestone v1.5*
