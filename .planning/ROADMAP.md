# Roadmap: EML Symbolic Regression

**Created:** 2026-04-15
**Updated:** 2026-04-15
**Granularity:** Coarse
**Mode:** YOLO
**Current milestone:** v1.1 EML Compiler and Warm Starts
**Coverage:** 22 v1.1 requirements mapped, 0 unmapped

## Overview

v1.0 established the exact EML semantics, soft master trees, optimizer, verifier, cleanup, demos, tests, and documentation. v1.1 turns those verified reference capabilities into compiler-driven warm-start recovery workflows: compile supported SymPy expressions into exact EML ASTs, validate them independently, embed them into compatible soft trees, perturb and train through the existing optimizer, and let the verifier decide which demos can be promoted as trained exact recoveries.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 planned

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

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (8.1, 8.2): Urgent insertions, if needed later
- v1.1 continues from completed Phase 7 and starts at Phase 8

- [x] **Phase 8: Compiler Contract and Direct Rules** - Establish a fail-closed compiler contract that emits exact EML ASTs, metadata, and validation evidence. (completed 2026-04-15)
- [x] **Phase 9: Constant Catalog and AST Embedding** - Make compiled literal constants representable in soft trees and prove compiled ASTs can embed and snap back safely. (completed 2026-04-15)
- [x] **Phase 10: Arithmetic Rule Corpus and Depth Gates** - Add the arithmetic rule subset needed for Beer-Lambert and Michaelis-Menten under explicit budgets and assumptions. (completed 2026-04-15)
- [x] **Phase 11: Perturbed Warm-Start Training** - Perturb compiled embeddings, train through the existing optimizer, and classify post-snap outcomes honestly. (completed 2026-04-15)
- [x] **Phase 12: Demo Promotion and Claim Reporting** - Promote Beer-Lambert and conditionally Michaelis-Menten through verifier-gated reports while keeping Planck as stretch evidence. (completed 2026-04-15)
- [x] **Phase 13: Regression Tests and Documentation Lockdown** - Lock the compiler, warm-start, demo-claim, and documentation contracts with tests and public wording. (completed 2026-04-15)

## Phase Details

### Phase 8: Compiler Contract and Direct Rules
**Goal**: Users can compile a trusted SymPy subset into exact EML ASTs and know when compilation is unsupported.
**Depends on**: Phase 7
**Requirements**: COMP-01, COMP-02, COMP-03, COMP-04
**Success Criteria** (what must be TRUE):
  1. User can compile a whitelisted SymPy expression into the existing exact EML `Expr` AST type without creating a parallel tree representation.
  2. User receives structured compiler metadata containing source expression, normalized expression, rule trace, variables, constants, depth, node count, domain assumptions, and unsupported reason codes.
  3. User can validate compiled AST output against independent ordinary-expression evaluation before the result becomes eligible for warm-start training.
  4. Unsupported operators, unsupported powers, unknown variables, unsafe constants, and depth or node budget excesses fail closed with machine-readable errors.
**Plans**: TBD

### Phase 9: Constant Catalog and AST Embedding
**Goal**: Users can represent compiled literal constants in soft master trees and embed compiled ASTs safely before training.
**Depends on**: Phase 8
**Requirements**: CONST-01, CONST-02, EMBED-01, EMBED-02, EMBED-03
**Success Criteria** (what must be TRUE):
  1. User can choose an explicit constant policy, with `literal_constants` available while the default pure `const:1` behavior remains unchanged.
  2. User can construct `SoftEMLTree` instances with a finite constant catalog derived from a compiled expression.
  3. User can embed a compiled exact EML AST into a compatible soft master tree by mapping AST nodes to slot logits.
  4. User sees immediate embed-to-snap validation proving a high-strength warm start snaps back to the compiled AST before perturbation.
  5. User receives actionable diagnostics for depth-too-small, missing-constant, missing-variable, and incompatible-tree failures before training starts.
**Plans**: TBD

### Phase 10: Arithmetic Rule Corpus and Depth Gates
**Goal**: Users can compile the arithmetic needed for v1.1 demo formulas under explicit assumptions, max-power limits, and depth budgets.
**Depends on**: Phase 9
**Requirements**: ARITH-01, ARITH-02, ARITH-03
**Success Criteria** (what must be TRUE):
  1. User can compile direct `exp` and `log` rules over arbitrary supported subexpressions.
  2. User can compile unary negation, subtraction, addition, multiplication, reciprocal, and division through tested EML rule templates or receive explicit unsupported/depth failure reasons.
  3. User can compile small integer powers only when explicit max-power and depth gates allow them.
  4. User can inspect rule-level domain assumptions, depth, and node counts before arithmetic compiler output is embedded or trained.
**Plans**: TBD

### Phase 11: Perturbed Warm-Start Training
**Goal**: Users can perturb compiled warm-start logits, train through the existing optimizer path, and understand the exact post-training outcome.
**Depends on**: Phase 10
**Requirements**: WARM-01, WARM-02, WARM-03, WARM-04
**Success Criteria** (what must be TRUE):
  1. User can run deterministic perturbation of compiled warm-start logits with recorded strength, noise scale, seed, active slot changes, and pre/post perturbation snap summaries.
  2. User can train from compiled warm starts through the existing optimizer path without allowing the optimizer to label a result `recovered`.
  3. User receives a warm-start manifest containing compiler metadata, terminal bank, embedding assignments, perturbation config, optimizer config, snap decisions, anomaly stats, and verification outcome.
  4. User can distinguish same-AST return, verified-equivalent AST, snapped-but-failed candidate, soft-fit-only, and failed warm-start attempts.
**Plans**: TBD

### Phase 12: Demo Promotion and Claim Reporting
**Goal**: Users can run v1.1 compiler/warm-start demos and see claim statuses separated by evidence stage.
**Depends on**: Phase 11
**Requirements**: DEMO-05, DEMO-06, DEMO-07, DEMO-08
**Success Criteria** (what must be TRUE):
  1. User can run Beer-Lambert as a compiler-driven warm-start recovery demo and see it promoted only when the final trained exact EML AST verifies.
  2. User can run Michaelis-Menten as a compiler-driven warm-start recovery demo when arithmetic rules and depth gates pass, or receive honest unsupported/depth diagnostics otherwise.
  3. User can run normalized Planck as a stretch compile/warm-start report without a milestone guarantee of trained recovery.
  4. User-facing reports separate catalog showcase, compiled seed, warm-start attempt, trained exact recovery, blind baseline, stretch, unsupported, and failed statuses.
**Plans**: TBD

### Phase 13: Regression Tests and Documentation Lockdown
**Goal**: Users can rely on tests and documentation that protect compiler correctness, warm-start provenance, and public recovery claims.
**Depends on**: Phase 12
**Requirements**: TEST-03, TEST-04
**Success Criteria** (what must be TRUE):
  1. User can run pytest coverage for compiler rules, negative compiler cases, constant policy, constant catalog labels, embedding round trips, perturbation determinism, warm-start manifests, and demo promotion gates.
  2. User can read documentation explaining fixed literal constants, compile-only versus warm-start recovery, demo claim statuses, depth limits, and why v1.1 is not blind symbolic discovery.
  3. User can see regression coverage that keeps `recovered` verifier-owned across CLI and report outputs.
  4. User can identify unsupported and failed cases from docs and reports without mistaking them for catalog fallback success.
**Plans**: TBD

## Dependency Order

```text
Phase 8 -> Phase 9 -> Phase 10 -> Phase 11 -> Phase 12 -> Phase 13
```

The order is intentionally linear. The compiler contract is the trust boundary; constants and embedding must be representable before perturbation; arithmetic rules determine which scientific demos are feasible; warm-start training produces post-snap candidates; demo reporting translates verifier outcomes into public claims; tests and docs lock the contract.

## Requirement Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| COMP-01 | Phase 8 | Pending |
| COMP-02 | Phase 8 | Pending |
| COMP-03 | Phase 8 | Pending |
| COMP-04 | Phase 8 | Pending |
| CONST-01 | Phase 9 | Pending |
| CONST-02 | Phase 9 | Pending |
| EMBED-01 | Phase 9 | Pending |
| EMBED-02 | Phase 9 | Pending |
| EMBED-03 | Phase 9 | Pending |
| ARITH-01 | Phase 10 | Pending |
| ARITH-02 | Phase 10 | Pending |
| ARITH-03 | Phase 10 | Pending |
| WARM-01 | Phase 11 | Pending |
| WARM-02 | Phase 11 | Pending |
| WARM-03 | Phase 11 | Pending |
| WARM-04 | Phase 11 | Pending |
| DEMO-05 | Phase 12 | Pending |
| DEMO-06 | Phase 12 | Pending |
| DEMO-07 | Phase 12 | Pending |
| DEMO-08 | Phase 12 | Pending |
| TEST-03 | Phase 13 | Pending |
| TEST-04 | Phase 13 | Pending |

**Coverage:** 22/22 v1.1 requirements mapped. No orphaned requirements. No duplicate phase assignments.

## Progress

**Execution Order:** Phase 8 -> Phase 9 -> Phase 10 -> Phase 11 -> Phase 12 -> Phase 13

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Semantics, AST, and Deterministic Artifacts | Complete | Complete | 2026-04-15 |
| 2. Complete Master Trees and Soft Evaluation | Complete | Complete | 2026-04-15 |
| 3. Optimizer, Restarts, Hardening, and Recovery Statuses | Complete | Complete | 2026-04-15 |
| 4. Verifier and Acceptance Contract | Complete | Complete | 2026-04-15 |
| 5. Local Cleanup, SymPy Export, and Reports | Complete | Complete | 2026-04-15 |
| 6. Demo Harness and Public Showcase | Complete | Complete | 2026-04-15 |
| 7. Tests and Documentation | Complete | Complete | 2026-04-15 |
| 8. Compiler Contract and Direct Rules | 1/1 | Complete    | 2026-04-15 |
| 9. Constant Catalog and AST Embedding | 1/1 | Complete    | 2026-04-15 |
| 10. Arithmetic Rule Corpus and Depth Gates | 1/1 | Complete    | 2026-04-15 |
| 11. Perturbed Warm-Start Training | 1/1 | Complete    | 2026-04-15 |
| 12. Demo Promotion and Claim Reporting | 1/1 | Complete    | 2026-04-15 |
| 13. Regression Tests and Documentation Lockdown | 1/1 | Complete    | 2026-04-15 |

---
*Roadmap updated: 2026-04-15 for milestone v1.1*
