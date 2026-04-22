# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-22
**Current milestone:** v1.15 GEML family and i*pi EML exploration
**Phase numbering:** Continuing from v1.14 Phase 81.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)
- **v1.5 Training Proof and Recovery Guarantees** - Phases 29-33 complete (completed 2026-04-16; archive: `.planning/milestones/v1.5-ROADMAP.md`)
- **v1.6 Hybrid Search Pipeline and Exact Candidate Recovery** - Phases 34-38 complete (completed 2026-04-16; archive: `.planning/milestones/v1.6-ROADMAP.md`)
- **v1.7 Centered-Family Baseline and Paper Decision** - Phases 39-43 complete (completed 2026-04-16; archive: `.planning/milestones/v1.7-ROADMAP.md`)
- **v1.8 Centered-Family Viability and Full Evidence Run** - Phases 44-48 complete (completed 2026-04-17; archive: `.planning/milestones/v1.8-ROADMAP.md`)
- **v1.9 Raw-EML Hybrid Recovery and Paper Suite** - Phases 49-53 complete (completed 2026-04-17; archive: `.planning/milestones/v1.9-ROADMAP.md`)
- **v1.10 Search-backed motif library and compiler shortening for logistic and Planck** - Phases 54-58 complete (completed 2026-04-18; archive: `.planning/milestones/v1.10-ROADMAP.md`)
- **v1.11 Paper-strength evidence and figure package** - Phases 59-63 complete (completed 2026-04-19; archive: `.planning/milestones/v1.11-ROADMAP.md`)
- **v1.12 Paper draft skeleton and refreshed shallow evidence** - Phases 64-68 complete (completed 2026-04-19; archive: `.planning/milestones/v1.12-ROADMAP.md`)
- **v1.13 Publication-grade reproduction and validation** - Phases 69-76 complete (completed 2026-04-20; archives: `.planning/milestones/v1.13-ROADMAP.md`, `.planning/milestones/v1.13-REQUIREMENTS.md`, `.planning/milestones/v1.13-MILESTONE-AUDIT.md`, `.planning/milestones/v1.13-phases/`)
- **v1.14 Evidence claim integrity and audit hardening** - Phases 77-81 complete (completed 2026-04-21; archives: `.planning/milestones/v1.14-ROADMAP.md`, `.planning/milestones/v1.14-REQUIREMENTS.md`, `.planning/milestones/v1.14-phases/`)

## Current Status

v1.15 is open. It reframes the proposed i*pi EML operator as the `a = i*pi` specialization of the broader `GEML_a(x, y) = exp(a*x) - log(y)/a` family. The milestone first builds the exact family semantics and restricted theory, then integrates i*pi EML into the existing training/snap/verification pipeline, then runs matched EML versus i*pi EML comparisons on oscillatory targets and negative controls.

## Phase Status

- [ ] Phase 82: GEML Family Semantics and Structural Identity
- [ ] Phase 83: i*pi EML Restricted Theory and Branch Contract
- [ ] Phase 84: Family-Aware Training and Snapping Integration
- [ ] Phase 85: Oscillatory Benchmark Pack and Negative Controls
- [ ] Phase 86: Matched EML versus i*pi EML Campaign Runner
- [ ] Phase 87: GEML Evidence Package and Claim Boundary

## Phase Overview

| Phase | Name | Goal | Requirements |
|-------|------|------|--------------|
| 82 | GEML Family Semantics and Structural Identity | Add exact `GEML_a` semantics, named EML/i*pi EML specializations, serialization, evaluator support, and the central structural identity. | GEML-01, GEML-02, GEML-03, GEML-04, GEML-05 |
| 83 | i*pi EML Restricted Theory and Branch Contract | Prove/test the controlled i*pi identities and make branch behavior an explicit operator contract. | THRY-01, THRY-02, THRY-03, THRY-04, THRY-05, BRAN-01, BRAN-02, BRAN-03, BRAN-04 |
| 84 | Family-Aware Training and Snapping Integration | Thread fixed GEML specializations through master-tree training, snapping, cleanup, metrics, and raw-EML regressions. | TRN-01, TRN-02, TRN-03, TRN-04 |
| 85 | Oscillatory Benchmark Pack and Negative Controls | Add target suites for i*pi EML's natural bias plus negative controls and matched campaign manifests. | BENCH-01, BENCH-02, BENCH-03, BENCH-04, BENCH-05 |
| 86 | Matched EML versus i*pi EML Campaign Runner | Execute paired comparison rows and aggregate matched recovery, loss, numerical, branch, and runtime metrics. | EVID-01, EVID-02 |
| 87 | GEML Evidence Package and Claim Boundary | Package theory, benchmark evidence, tables, and claim-audit checks into a paper-decision artifact. | EVID-03, EVID-04, EVID-05 |

## Phase Details

### Phase 82: GEML Family Semantics and Structural Identity

**Goal:** The codebase can represent, evaluate, serialize, and document `GEML_a`, with raw EML and i*pi EML as explicit named specializations.

**Requirements:** GEML-01, GEML-02, GEML-03, GEML-04, GEML-05

**Success criteria:**
1. `GEML_a(x, y) = exp(a*x) - log(y)/a` is implemented for explicit nonzero complex `a` across the exact AST and supported evaluators.
2. Raw EML resolves to the named `a = 1` specialization and i*pi EML resolves to the named `a = i*pi` specialization.
3. JSON/SymPy export preserves the family parameter and named specialization metadata without breaking existing EML artifacts.
4. Tests or theory docs verify `exp(a*GEML_a(u, v)) = exp(a*exp(a*u))/v` for representative cases.

### Phase 83: i*pi EML Restricted Theory and Branch Contract

**Goal:** i*pi EML has explicit restricted-domain theorems and branch diagnostics before it enters broader experiments.

**Requirements:** THRY-01, THRY-02, THRY-03, THRY-04, THRY-05, BRAN-01, BRAN-02, BRAN-03, BRAN-04

**Success criteria:**
1. The reciprocal and identity constructions are proven or executable-checked on `y > 0`, with branch assumptions stated.
2. The real-axis derivative and one-step composition magnitude bound are derived in a checked theory artifact.
3. Closure language is restricted to exactly what the milestone proves or tests.
4. Training, verification, and reports expose branch convention, branch-cut proximity, branch crossings, invalid-domain skips, and branch-related candidate failures.
5. Optional branch-safety training guards are manifest-visible and do not change faithful verification semantics.

### Phase 84: Family-Aware Training and Snapping Integration

**Goal:** Fixed GEML specializations can run through the existing differentiable search pipeline without silently borrowing invalid raw-family witnesses.

**Requirements:** TRN-01, TRN-02, TRN-03, TRN-04

**Success criteria:**
1. The complete soft master tree accepts a fixed operator specialization while preserving raw EML as the default.
2. Optimizer, hardening, snapping, exact-candidate pooling, cleanup, and refit paths operate on i*pi EML artifacts.
3. Candidate artifacts report gradient norms, overflow/NaN counts, branch diagnostics, pre-snap MSE, post-snap MSE, and wall-clock metadata.
4. Raw EML regression tests and v1.14 claim-accounting tests still pass.

### Phase 85: Oscillatory Benchmark Pack and Negative Controls

**Goal:** The comparison suite tests i*pi EML where it should plausibly help and where it should not.

**Requirements:** BENCH-01, BENCH-02, BENCH-03, BENCH-04, BENCH-05

**Success criteria:**
1. Periodic, harmonic, damped oscillation, wave/standing-wave, and log-periodic target manifests are registered with normalized safe domains.
2. Negative controls include `exp`, `log`, polynomial, and rational targets.
3. Campaign manifests lock matched depths, optimizer settings, initialization budgets, snapping rules, verifier gates, and split policies for both operators.
4. Suite validation fails closed if an i*pi target crosses an undeclared unsafe branch domain.

### Phase 86: Matched EML versus i*pi EML Campaign Runner

**Goal:** The project can produce paired comparison evidence under a single protocol.

**Requirements:** EVID-01, EVID-02

**Success criteria:**
1. A campaign runner emits paired EML and i*pi EML rows for every declared target.
2. Aggregates include blind exact-recovery after snapping, MSE before and after snapping, gradient statistics, overflow/NaN counts, branch counts, wall-clock time, and available resource metadata.
3. The paired output preserves v1.14 recovery-accounting fields so compile-only or unsupported rows cannot contaminate trained recovery rates.

### Phase 87: GEML Evidence Package and Claim Boundary

**Goal:** The milestone ends with a claim-safe decision package for whether i*pi EML deserves a paper section.

**Requirements:** EVID-03, EVID-04, EVID-05

**Success criteria:**
1. Reports classify wins, losses, and neutral results by target family, including negative controls.
2. Claim-audit checks block global-superiority, broad blind-recovery, and full-universality language unless proof/evidence supports it.
3. The final package includes the theory note, benchmark manifests, aggregate tables, source locks, reproduction commands, and a claim-boundary summary.
4. The package explicitly states whether i*pi EML is promising, negative, or inconclusive under the matched protocol.

## Dependency Notes

- Phase 82 comes first because all later work depends on exact family semantics and serialization.
- Phase 83 follows before training campaigns so branch behavior and theory claims are clear before artifacts exist.
- Phase 84 must precede benchmark execution because the training and snap pipeline needs family-aware metrics and guards.
- Phase 85 can be planned with Phase 84 context but should run after operator integration is stable.
- Phase 86 depends on Phase 85 manifests and Phase 84 pipeline support.
- Phase 87 is last because it packages evidence and claim boundaries from all prior phases.

## Notes

- No new external domain research was run during initialization; the milestone brief and existing operator-family history are sufficient to scope the first pass.
- The milestone intentionally avoids learning arbitrary `a` values. Fixed `a = 1` versus `a = i*pi` is the controlled comparison.
- Positive results should be framed as structural bias on declared oscillatory/phase-log targets, not as global symbolic-regression superiority.

---
*Roadmap created for v1.15 on 2026-04-22*
