# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-18
**Current milestone:** v1.10 Search-backed motif library and compiler shortening for logistic and Planck
**Phase numbering:** Continues from v1.9; v1.10 starts at Phase 54.

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
- **v1.10 Search-backed motif library and compiler shortening for logistic and Planck** - Phases 54-58 complete (completed 2026-04-18)

## Milestone Goal

Build a reusable, validation-gated motif library that makes logistic strict compile support and warm-start recovery realistic while materially reducing Planck compile depth under the existing honest recovery contract.

## Phases

- [x] **Phase 54: Compiler Baseline Locks** - Lock archived logistic, Planck, Michaelis-Menten, Arrhenius, and Shockley compiler behavior before motif changes.
- [x] **Phase 55: Generalized Structural Motif Matching** - Extend reciprocal and saturation matching to validated compilable subexpressions with diagnostics and fail-closed behavior.
- [x] **Phase 56: Logistic Exponential-Saturation Support** - Add structural logistic-like exponential-saturation shortening and attempt warm-start only under unchanged strict gates.
- [x] **Phase 57: Planck Motif Search and Power Compression** - Use bounded motif-search evidence and validation-backed square/cube compression to reduce Planck depth while preserving unsupported/stretch honesty.
- [x] **Phase 58: Focused Evidence and Artifact Contracts** - Add focused logistic/Planck suites, deterministic CLI artifact paths, and regression tests for milestone claims.

## Phase Details

### Phase 54: Compiler Baseline Locks

**Goal**: Maintainers can verify current compiler support and depth anchors before new motif behavior changes.
**Depends on**: Phase 53
**Requirements**: BASE-01, BASE-02, BASE-03, BASE-04, BASE-05
**Success Criteria** (what must be TRUE):
  1. Maintainer can run regression tests confirming logistic relaxed compile depth is 27 with no macro hits on the archived baseline path.
  2. Maintainer can run regression tests confirming Planck relaxed compile depth is 20 with `scaled_exp_minus_one_template` and `direct_division_template` hits.
  3. Maintainer can run regression tests confirming Michaelis-Menten strict depth 12 through `saturation_ratio_template`.
  4. Maintainer can run regression tests confirming Arrhenius and Shockley strict support still use `direct_division_template` and `scaled_exp_minus_one_template`.
**Plans**: TBD

### Phase 55: Generalized Structural Motif Matching

**Goal**: Compiler motifs can match reusable reciprocal and saturation structures over validated compiled subexpressions and expose fail-closed diagnostics.
**Depends on**: Phase 54
**Requirements**: MOTIF-01, MOTIF-05, MOTIF-06
**Success Criteria** (what must be TRUE):
  1. Maintainer can compile reciprocal and saturation forms around subexpressions such as `1/(g(x)+b)` and `c*g(x)/(g(x)+b)` when each subexpression validates.
  2. Compiler emits macro diagnostics for new motif attempts with template name, depth delta, node delta, validation status, and rejection reason.
  3. Malformed, unsupported, non-finite, or validation-failing variants are rejected without changing support gates or emitted ASTs.
  4. Motif matching remains structural and does not require formula-name or demo-name branches.
**Plans**: TBD

### Phase 56: Logistic Exponential-Saturation Support

**Goal**: Logistic-like laws can compile shorter through a structural exponential-saturation motif and receive honest warm-start evidence when strict support passes.
**Depends on**: Phase 55
**Requirements**: MOTIF-02, LOGI-01, LOGI-02, LOGI-03
**Success Criteria** (what must be TRUE):
  1. Maintainer can compile logistic-like structures such as `1/(1+c*exp(a))` or `exp(a)/(exp(a)+c)` with materially lower depth than archived relaxed depth 27.
  2. Compile diagnostics show the exponential-saturation motif in `macro_diagnostics["hits"]` when it is responsible for shortening.
  3. Logistic is marked strict-supported only when the existing shipped strict gate, or an explicitly comparable non-looser gate, passes.
  4. If strict support exists, logistic warm-start runs through the normal benchmark/verifier contract and records same-AST or verified-equivalent status with evidence class and verifier verdict.
**Plans**: TBD

### Phase 57: Planck Motif Search and Power Compression

**Goal**: Planck gets measurable compiler shortening from reusable power compression or bounded search-backed motifs while remaining unsupported unless full support and verification pass.
**Depends on**: Phase 56
**Requirements**: MOTIF-03, MOTIF-04, PLAN-01, PLAN-02, PLAN-03, PLAN-04, PLAN-05
**Success Criteria** (what must be TRUE):
  1. Maintainer can compile validated low-degree powers, at least `g(x)**2` and `g(x)**3`, only when the compressed path is shorter and independently validated.
  2. Any bounded motif-search helper records target family, candidate construction, independent numeric samples, validation verdict, and winning template before codification.
  3. Planck relaxed diagnostics report a compile depth materially below 20, or explicitly report why no accepted motif shortened it.
  4. Planck reports macro hits, depth, node count, support status, and unsupported/stretch reasons; it is promoted or warm-started only if strict support and verifier-owned recovery gates pass.
**Plans**: TBD

### Phase 58: Focused Evidence and Artifact Contracts

**Goal**: Focused suites and artifacts make v1.10 logistic and Planck claims reproducible without a broad paper package refresh.
**Depends on**: Phase 57
**Requirements**: LOGI-04, LOGI-05, EVID-01, EVID-02, EVID-03, EVID-04, EVID-05
**Success Criteria** (what must be TRUE):
  1. Maintainer can run `v1.10-logistic-evidence` for logistic compile diagnostics and logistic warm-start when strict support exists.
  2. Maintainer can run `v1.10-planck-diagnostics` for Planck compile diagnostics and optional warm-start only when strict support exists.
  3. CLI writes deterministic artifacts under `artifacts/campaigns/v1.10-logistic-evidence/` and `artifacts/campaigns/v1.10-planck-diagnostics/`.
  4. Artifacts record compile support, compile depth, node count, macro hits, warm-start status, verifier status, and unsupported/stretch reasons.
  5. Test coverage verifies focused suite contracts, CLI artifact paths, baseline preservation, logistic improvement, Planck diagnostic improvement, and motif fail-closed cases.
**Plans**: TBD

## Progress

**Execution Order:** Phase 54 -> Phase 55 -> Phase 56 -> Phase 57 -> Phase 58

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 54. Compiler Baseline Locks | 1/1 | Complete | 2026-04-18 |
| 55. Generalized Structural Motif Matching | 1/1 | Complete | 2026-04-18 |
| 56. Logistic Exponential-Saturation Support | 1/1 | Complete | 2026-04-18 |
| 57. Planck Motif Search and Power Compression | 1/1 | Complete | 2026-04-18 |
| 58. Focused Evidence and Artifact Contracts | 1/1 | Complete | 2026-04-18 |

## Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| BASE-01 | Phase 54 | Complete |
| BASE-02 | Phase 54 | Complete |
| BASE-03 | Phase 54 | Complete |
| BASE-04 | Phase 54 | Complete |
| BASE-05 | Phase 54 | Complete |
| MOTIF-01 | Phase 55 | Complete |
| MOTIF-02 | Phase 56 | Complete |
| MOTIF-03 | Phase 57 | Complete |
| MOTIF-04 | Phase 57 | Complete |
| MOTIF-05 | Phase 55 | Complete |
| MOTIF-06 | Phase 55 | Complete |
| LOGI-01 | Phase 56 | Complete |
| LOGI-02 | Phase 56 | Complete |
| LOGI-03 | Phase 56 | Complete |
| LOGI-04 | Phase 58 | Complete |
| LOGI-05 | Phase 58 | Complete |
| PLAN-01 | Phase 57 | Complete |
| PLAN-02 | Phase 57 | Complete |
| PLAN-03 | Phase 57 | Complete |
| PLAN-04 | Phase 57 | Complete |
| PLAN-05 | Phase 57 | Complete |
| EVID-01 | Phase 58 | Complete |
| EVID-02 | Phase 58 | Complete |
| EVID-03 | Phase 58 | Complete |
| EVID-04 | Phase 58 | Complete |
| EVID-05 | Phase 58 | Complete |

**Coverage summary:**
- v1.10 requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0

## Next Step

Run milestone audit and completion:

`$gsd-audit-milestone`

---
*Roadmap created: 2026-04-18 for milestone v1.10*
