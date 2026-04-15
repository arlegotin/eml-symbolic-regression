# Roadmap: EML Symbolic Regression

**Created:** 2026-04-15
**Updated:** 2026-04-15
**Granularity:** Coarse
**Mode:** YOLO
**Current milestone:** v1.4 Recovery Performance Improvements
**Coverage:** 21 v1.4 requirements mapped, 0 unmapped

## Overview

v1.3 produced the evidence scoreboard: committed `smoke`, `standard`, and `showcase` campaign bundles with raw run artifacts, CSV tables, SVG figures, and reports. The measured baseline is clear: warm-start training is promising, blind recovery is weak, high Beer-Lambert perturbations fail, and several FOR_DEMO formulas are blocked by compiler depth/operator gates.

v1.4 improves the system against those committed baselines. The milestone should not change the meaning of `recovered`; it should improve optimizer/compiler behavior, then rerun the same standard/showcase campaigns and report before/after deltas.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 planned

## Completed Milestone Context

| Phase | Name | Status |
|-------|------|--------|
| 1-7 | v1.0 MVP | Complete |
| 8-13 | v1.1 EML Compiler and Warm Starts | Complete |
| 14-18 | v1.2 Training Benchmark and Recovery Evidence | Complete |
| 19-23 | v1.3 Benchmark Campaign and Evidence Report | Complete |

## Phases

**Phase Numbering:**
- v1.4 continues from completed Phase 23 and starts at Phase 24.
- Integer phases are planned milestone work.
- Decimal phases can be inserted later for urgent gap closure.

- [x] **Phase 24: Baseline Failure Triage and Diagnostic Harness** - Turn v1.3 standard/showcase failures into focused reproducible diagnostics. (requirements: DIAG-01, DIAG-02, DIAG-03, DIAG-04) (completed 2026-04-15)
- [x] **Phase 25: Blind Optimizer Recovery Improvements** - Improve blind optimizer behavior for shallow formulas and preserve verifier-owned recovery semantics. (requirements: BLIND-01, BLIND-02, BLIND-03, BLIND-04) (completed 2026-04-15)
- [ ] **Phase 26: Warm-Start Perturbation Robustness** - Improve or precisely diagnose Beer-Lambert warm-start failures at stronger perturbations. (requirements: PERT-01, PERT-02, PERT-03, PERT-04)
- [ ] **Phase 27: Compiler Coverage and Depth Reduction** - Reduce unsupported/depth-gated FOR_DEMO cases while keeping compiler behavior fail-closed. (requirements: COV-01, COV-02, COV-03, COV-04)
- [ ] **Phase 28: Before/After Campaign Evaluation** - Rerun standard/showcase campaigns and report deltas against v1.3 baselines. (requirements: EVAL-01, EVAL-02, EVAL-03, EVAL-04, EVAL-05)

## Phase Details

### Phase 24: Baseline Failure Triage and Diagnostic Harness
**Goal**: Users can inspect and rerun focused diagnostics for the exact v1.3 failure modes before changing optimizer/compiler behavior.
**Depends on**: Phase 23
**Requirements**: DIAG-01, DIAG-02, DIAG-03, DIAG-04
**Success Criteria** (what must be TRUE):
  1. Baseline triage summarizes v1.3 standard/showcase failures by formula, start mode, perturbation, and recovery class.
  2. Each target failure class links to representative raw run artifacts and relevant optimizer/verifier metrics.
  3. Focused diagnostic commands can rerun blind failures, Beer-Lambert perturbation failures, and compiler/depth gates without full campaigns.
  4. v1.3 baseline metrics remain immutable comparison inputs for later phases.
**Plans**: TBD

### Phase 25: Blind Optimizer Recovery Improvements
**Goal**: Users get a measured improvement path for blind recovery on shallow baseline formulas without weakening the verifier contract.
**Depends on**: Phase 24
**Requirements**: BLIND-01, BLIND-02, BLIND-03, BLIND-04
**Success Criteria** (what must be TRUE):
  1. Blind optimizer experiments are reproducible across `exp`, `log`, and `radioactive_decay` with explicit seeds and budgets.
  2. Optimizer variants compare against v1.3 baseline metrics using the same verifier-owned recovery status.
  3. The selected default improves recovery or materially improves post-snap loss on at least one v1.3 blind failure family without regressing existing recovered cases.
  4. Remaining blind failures include diagnostics that separate soft loss, snap instability, expression depth, and verifier mismatch.
**Plans**: TBD

### Phase 26: Warm-Start Perturbation Robustness
**Goal**: Users can improve or precisely explain Beer-Lambert warm-start failures under stronger perturbations.
**Depends on**: Phase 24
**Requirements**: PERT-01, PERT-02, PERT-03, PERT-04
**Success Criteria** (what must be TRUE):
  1. Beer-Lambert perturbation diagnostics cover v1.3 noise levels with changed-slot counts and verifier status.
  2. Training or snapping changes improve high-perturbation recovery, or the failure mechanism is narrowed with reproducible evidence.
  3. Same-AST return, verified-equivalent recovery, snapped-but-failed, and soft-fit-only remain distinct outcomes.
  4. Literal-constant provenance and verifier-owned recovery semantics remain unchanged.
**Plans**: TBD

### Phase 27: Compiler Coverage and Depth Reduction
**Goal**: Users can move at least one v1.3 unsupported/depth-gated FOR_DEMO formula closer to verified EML coverage while preserving fail-closed compiler behavior.
**Depends on**: Phase 24
**Requirements**: COV-01, COV-02, COV-03, COV-04
**Success Criteria** (what must be TRUE):
  1. Compiler diagnostics expose depth, node count, rule trace, and unsupported reasons for the targeted FOR_DEMO formulas.
  2. At least one v1.3 unsupported/depth-gated formula moves to a verified compiled EML AST or a documented lower-depth candidate.
  3. Damped oscillator's unsupported operator path is either transformed into supported form or explicitly deferred with tests.
  4. Unsupported formulas continue to emit structured reasons instead of invalid EML trees.
**Plans**: TBD

### Phase 28: Before/After Campaign Evaluation
**Goal**: Users can see whether v1.4 improved real end-to-end performance by rerunning the same campaign contracts and comparing against v1.3 baselines.
**Depends on**: Phase 25, Phase 26, Phase 27
**Requirements**: EVAL-01, EVAL-02, EVAL-03, EVAL-04, EVAL-05
**Success Criteria** (what must be TRUE):
  1. v1.4-labeled standard and showcase campaign folders are generated after optimizer/compiler changes.
  2. Before/after reports compute deltas for recovery, unsupported rate, failure rate, losses, and runtime against v1.3 baselines.
  3. The report classifies each target category as improved, regressed, or unchanged.
  4. A single documented command can reproduce the comparison from a clean checkout.
  5. Tests cover diagnostics, optimizer/comparison outputs, compiler changes, and campaign comparison behavior.
**Plans**: TBD

## Dependency Order

```text
Phase 24 -> Phase 25 -> Phase 28
Phase 24 -> Phase 26 -> Phase 28
Phase 24 -> Phase 27 -> Phase 28
```

Phase 24 creates a shared diagnostic baseline. Phases 25-27 can be executed independently after triage because they target distinct performance bottlenecks. Phase 28 must run last so it evaluates the combined result.

## Requirement Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| DIAG-01 | Phase 24 | Pending |
| DIAG-02 | Phase 24 | Pending |
| DIAG-03 | Phase 24 | Pending |
| DIAG-04 | Phase 24 | Pending |
| BLIND-01 | Phase 25 | Complete |
| BLIND-02 | Phase 25 | Complete |
| BLIND-03 | Phase 25 | Complete |
| BLIND-04 | Phase 25 | Complete |
| PERT-01 | Phase 26 | Pending |
| PERT-02 | Phase 26 | Pending |
| PERT-03 | Phase 26 | Pending |
| PERT-04 | Phase 26 | Pending |
| COV-01 | Phase 27 | Pending |
| COV-02 | Phase 27 | Pending |
| COV-03 | Phase 27 | Pending |
| COV-04 | Phase 27 | Pending |
| EVAL-01 | Phase 28 | Pending |
| EVAL-02 | Phase 28 | Pending |
| EVAL-03 | Phase 28 | Pending |
| EVAL-04 | Phase 28 | Pending |
| EVAL-05 | Phase 28 | Pending |

**Coverage:** 21/21 v1.4 requirements mapped. No orphaned requirements. No duplicate phase assignments.

## Progress

**Execution Order:** Phase 24 -> Phases 25/26/27 -> Phase 28

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1-7. v1.0 MVP | Complete | Complete | 2026-04-15 |
| 8-13. v1.1 EML Compiler and Warm Starts | Complete | Complete | 2026-04-15 |
| 14-18. v1.2 Training Benchmark and Recovery Evidence | Complete | Complete | 2026-04-15 |
| 19-23. v1.3 Benchmark Campaign and Evidence Report | Complete | Complete | 2026-04-15 |
| 24. Baseline Failure Triage and Diagnostic Harness | 1/1 | Complete    | 2026-04-15 |
| 25. Blind Optimizer Recovery Improvements | 1/1 | Complete    | 2026-04-15 |
| 26. Warm-Start Perturbation Robustness | 0/1 | Pending | - |
| 27. Compiler Coverage and Depth Reduction | 0/1 | Pending | - |
| 28. Before/After Campaign Evaluation | 0/1 | Pending | - |

---
*Roadmap updated: 2026-04-15 for milestone v1.4*
