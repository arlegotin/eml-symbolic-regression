# Requirements: EML Symbolic Regression Milestone v1.5

**Defined:** 2026-04-15
**Milestone:** v1.5 Training Proof and Recovery Guarantees
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Milestone v1.5 Requirements

Requirements for this milestone only. Completed v1, v1.1, v1.2, v1.3, and v1.4 requirements are recorded as validated capabilities in `.planning/PROJECT.md` and `.planning/milestones/`.

### Paper Claim Contract

- [ ] **CLAIM-01**: User can inspect a paper-claim matrix that maps each v1.5 experiment to the specific paper-grounded statement it tests: complete depth-bounded EML search, shallow blind recovery, perturbed-true-tree recovery, and blind depth degradation.
- [ ] **CLAIM-02**: User can generate deterministic proof datasets with seeds, train/held-out/extrapolation splits, normalization metadata, target formulas, and source provenance.
- [ ] **CLAIM-03**: User can distinguish blind training, compiler warm-start training, perturbed true-tree training, compile-only verification, catalog verification, unsupported cases, and failed cases in every proof artifact.
- [ ] **CLAIM-04**: User receives explicit pass/fail thresholds for every proof suite, including the bounded suites where 100% verifier-owned training recovery is required and the depth-curve suites where measured rates are reported.

### Shallow Training Claim Split

- [x] **SHAL-01**: User can run declared shallow training suites covering `exp`, `log`, `radioactive_decay`, Beer-Lambert-style scaled exponentials, and signed/scaled exponential variants with fixed seeds and budgets, split into measured pure random-initialized blind recovery and bounded scaffolded recovery.
- [x] **SHAL-02**: User receives separate evidence for measured pure random-initialized blind recovery and 100% verifier-owned scaffolded shallow recovery, with scaffolded starts never counted toward the pure-blind claim.
- [x] **SHAL-03**: User can inspect optimizer and snap diagnostics for any scaffolded shallow run, including scaffold source, best loss, post-snap loss, snap margin, active node count, and verifier status.
- [x] **SHAL-04**: User can run regression tests that fail if the scaffolded `radioactive_decay` or declared signed/scaled exponential suite regresses below the 100% bounded target, or if pure-blind and scaffolded claim semantics are mixed.

### Perturbed Basin Training

- [x] **BASN-01**: User can generate exact EML target trees at declared depths and perturb their active categorical slots under deterministic noise envelopes.
- [x] **BASN-02**: User receives 100% verifier-owned recovery for the declared perturbed-true-tree basin proof suite, with per-depth and per-noise thresholds documented before execution.
- [x] **BASN-03**: User can run Beer-Lambert perturbation repair experiments that either recover all declared high-noise cases or formally narrow the supported perturbation bound with evidence.
- [x] **BASN-04**: User can apply local snap/discrete repair around failed trained candidates and inspect which slots or subtrees changed.
- [x] **BASN-05**: User can verify that same-AST return, verified-equivalent AST, repaired AST, snapped-but-failed, soft-fit-only, and unsupported outcomes remain distinct.

### Depth-Curve Training Evidence

- [ ] **CURV-01**: User can run a depth-curve experiment for blind and perturbed training over EML depths 2 through 6 with deterministic seeds, budgets, and formula/tree inventories.
- [ ] **CURV-02**: User receives recovery rates, confidence intervals or seed counts, best-loss distributions, post-snap-loss distributions, runtime, and snap-distance metrics by depth and training mode.
- [ ] **CURV-03**: User can compare the implementation's measured depth curve against the paper's qualitative claims without presenting deeper blind failures as product regressions.
- [ ] **CURV-04**: User can preserve depth-curve raw artifacts so future optimizer changes can be compared against the v1.5 paper-proof baseline.

### Proof Evidence Report

- [ ] **EVID-01**: User can run one command that produces the v1.5 proof campaign artifacts: datasets, raw runs, aggregate JSON, CSV tables, plots, and a Markdown claim report.
- [ ] **EVID-02**: User receives a proof report that states which paper-grounded claims passed, which remain bounded, which failed, and which are out of scope.
- [ ] **EVID-03**: User can reproduce all proof artifacts from a clean checkout using documented commands and committed configuration.
- [ ] **EVID-04**: User can run tests that lock the claim matrix, dataset generation, training proof suites, local repair behavior, depth-curve aggregation, and proof report generation.
- [ ] **EVID-05**: User can compare v1.5 proof-suite results against v1.4 campaign evidence without mixing proof-suite success rates with showcase campaign success rates.

## Future Requirements

Deferred to later milestones.

### External Evidence and Baselines

- **FUT-20**: User can run external noisy real-world datasets after v1.5 establishes bounded synthetic/source-document training proof behavior.
- **FUT-21**: User can compare v1.5 training proof suites against PySR or another external symbolic-regression baseline.
- **FUT-22**: User can use GPU/profiling acceleration after proof-suite bottlenecks are measured.
- **FUT-23**: User can explore a web or notebook dashboard after proof artifacts and reports stabilize.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Universal 100% recovery for all elementary functions | The paper reports rapid blind recovery degradation beyond shallow depths; v1.5 proves bounded suites and reports measured limits. |
| Counting compile-only or catalog verification as training proof | The user's goal is real training; compiler/catalog paths remain useful but separate evidence classes. |
| Counting exact scaffold starts as pure blind recovery | Phase 30 review found scaffolded scaled-exponential starts recover verifier-owned candidates but are not random-initialized blind recovery under the paper/NORTH_STAR definition. |
| Redefining `recovered` by loosening verifier thresholds | v1.5 must improve training behavior and evidence, not change the claim contract. |
| External noisy datasets | The current gap is bounded synthetic/source-document training proof; external data should come after that is credible. |
| GPU or custom kernels | The milestone target is recovery correctness and evidence quality, not throughput-first optimization. |
| Formal theorem proving | Numeric, high-precision, and symbolic verification are sufficient for this training-evidence milestone. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLAIM-01 | Phase 29 | Pending |
| CLAIM-02 | Phase 29 | Pending |
| CLAIM-03 | Phase 29 | Pending |
| CLAIM-04 | Phase 29 | Pending |
| SHAL-01 | Phase 30 | Complete |
| SHAL-02 | Phase 30 | Complete |
| SHAL-03 | Phase 30 | Complete |
| SHAL-04 | Phase 30 | Complete |
| BASN-01 | Phase 31 | Complete |
| BASN-02 | Phase 31 | Complete |
| BASN-03 | Phase 31 | Complete |
| BASN-04 | Phase 31 | Complete |
| BASN-05 | Phase 31 | Complete |
| CURV-01 | Phase 32 | Pending |
| CURV-02 | Phase 32 | Pending |
| CURV-03 | Phase 32 | Pending |
| CURV-04 | Phase 32 | Pending |
| EVID-01 | Phase 33 | Pending |
| EVID-02 | Phase 33 | Pending |
| EVID-03 | Phase 33 | Pending |
| EVID-04 | Phase 33 | Pending |
| EVID-05 | Phase 33 | Pending |

**Coverage:**
- v1.5 requirements: 22 total
- Mapped to phases: 22
- Unmapped: 0

---
*Requirements defined: 2026-04-15*
*Last updated: 2026-04-15 after resolving Phase 30 with separate measured pure-blind and bounded scaffolded shallow claims*
