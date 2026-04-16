# Requirements: EML Symbolic Regression Milestone v1.6

**Defined:** 2026-04-16
**Milestone:** v1.6 Hybrid Search Pipeline and Exact Candidate Recovery
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Milestone v1.6 Requirements

Requirements for this milestone only. Completed v1 through v1.5 requirements are recorded as validated capabilities in `.planning/PROJECT.md` and archived milestone files under `.planning/milestones/`.

### Hardening and Exact Candidate Selection

- [ ] **HARD-01**: User can run an explicit late hardening stage that sharpens categorical slots and emits exact snapped candidates at selected checkpoints instead of snapping only once at the end.
- [ ] **HARD-02**: User can retain exact candidates from every restart and late hardening checkpoint, rather than selecting the final answer solely from the minimum soft fit loss.
- [ ] **HARD-03**: User receives a verifier-gated exact-candidate ranking that prioritizes verifier status, extrapolation and high-precision error, held-out error, train post-snap loss, and complexity before soft-loss ties.
- [ ] **HARD-04**: User can inspect candidate provenance for the selected exact tree, including source restart/checkpoint, snap margins, active-slot diagnostics, and the fallback candidate that would have been chosen by the old selector.

### Snap-Neighborhood Discrete Cleanup

- [ ] **DISC-01**: User can run bounded low-margin beam expansion over ambiguous active snap slots using top-k categorical alternatives and exact AST deduplication.
- [ ] **DISC-02**: User can apply target-free local discrete repair to a failed snapped candidate without access to a known target AST or embedding.
- [ ] **DISC-03**: User can inspect which slots or subtrees were varied during beam or repair search, along with their margins and resulting exact-candidate deltas.
- [ ] **DISC-04**: User retains the original snapped exact candidate as fallback whenever beam search or local repair fails to improve the verifier-owned ranking.

### Post-Snap Constant Refit

- [ ] **REFI-01**: User can freeze a snapped exact tree, expose its literal constants, and optimize those coefficients post-snap without changing the discrete structure.
- [ ] **REFI-02**: User receives both pre-refit and post-refit exact-candidate artifacts, and the refit candidate is accepted only when it improves or matches the fallback under verifier-owned ranking.

### Numerical Stability and Domain Control

- [ ] **STAB-01**: User can inspect training diagnostics for `exp` overflow, `log`-domain violations, non-finite intermediates, clamp counts, and other branch or domain anomalies rather than only `exp` clamping.
- [ ] **STAB-02**: User can enable positive-domain-safe parameterizations or penalties for log-feeding branches during training without changing faithful verification semantics after snapping.

### Compiler Macro Shortening and Warm Starts

- [ ] **COMP-01**: User can compile supported small primitives and canonical motifs through a validated short-macro library before falling back to the existing generic compiler rules.
- [ ] **COMP-02**: User can inspect compiler diagnostics that report macro hits, missed shortcut opportunities, and depth/node deltas against the old compiler output.
- [ ] **COMP-03**: User gets expanded warm-start coverage for currently depth-limited formulas while preserving the existing fail-closed compiler behavior when no validated short macro applies.

### Evaluation Integrity and Regression Evidence

- [ ] **EVAL-01**: User can run proof and campaign suites that keep pure blind, scaffolded blind, compile-only, warm-start, and perturbed-basin modes explicitly separate in run artifacts and aggregate reports.
- [ ] **EVAL-02**: User can compare v1.6 recovery results against archived v1.5 proof artifacts and archived v1.4 campaign baselines without overwriting those prior milestone outputs.
- [ ] **EVAL-03**: User can run regression tests that fail if the new candidate-pool, cleanup, refit, or macro stages regress below the fallback exact-candidate performance on declared benchmark cases.
- [ ] **EVAL-04**: User receives reports and docs that state weak-dominance claims separately from likely-improvement claims and do not overstate blind-discovery capability.

## Future Requirements

Deferred to later milestones.

### External Baselines and Publication

- **FUT-24**: User can run matched-budget external symbolic-regression baselines such as PySR, AI Feynman, PhySO, or ParFam once the v1.6 hybrid recovery pipeline stabilizes.
- **FUT-25**: User can run family-guided or parametric EML subsearch for scientific-law families if the generic hybrid pipeline still underperforms on coefficiented showcase formulas.
- **FUT-26**: User can evaluate noisy external datasets or units-aware benchmarks after synthetic proof and hybrid search behavior are stable.
- **FUT-27**: User can assemble a publication-grade benchmark and paper package after the hybrid recovery pipeline and external baselines are in place.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Guaranteed improvement on every unseen formula | The honest guarantee for this milestone is weak dominance on declared benchmark selection, not universal success. |
| Claiming full blind recovery of arbitrary deeper formulas | The paper and v1.5 proof bundle both show strong blind degradation beyond shallow depths. |
| Counting scaffolded or warm-start evidence as pure blind discovery | Regime separation is part of the scientific contract and cannot be relaxed. |
| Replacing archived v1.5 proof artifacts or v1.4 campaign outputs | Those artifacts are preserved as baseline anchors for v1.6 comparisons. |
| Matched-budget external baseline competitions | Important, but deferred until the hybrid pipeline is materially stronger. |
| GPU or custom kernels | The current priority is recovery quality and exact-candidate handling, not throughput-first optimization. |
| Formal theorem proving | Numeric, high-precision, and symbolic verification remain sufficient for this milestone. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| HARD-01 | Phase 34 | Pending |
| HARD-02 | Phase 34 | Pending |
| HARD-03 | Phase 34 | Pending |
| HARD-04 | Phase 34 | Pending |
| DISC-01 | Phase 35 | Pending |
| DISC-02 | Phase 35 | Pending |
| DISC-03 | Phase 35 | Pending |
| DISC-04 | Phase 35 | Pending |
| REFI-01 | Phase 36 | Pending |
| REFI-02 | Phase 36 | Pending |
| STAB-01 | Phase 36 | Pending |
| STAB-02 | Phase 36 | Pending |
| COMP-01 | Phase 37 | Pending |
| COMP-02 | Phase 37 | Pending |
| COMP-03 | Phase 37 | Pending |
| EVAL-01 | Phase 38 | Pending |
| EVAL-02 | Phase 38 | Pending |
| EVAL-03 | Phase 38 | Pending |
| EVAL-04 | Phase 38 | Pending |

**Coverage:**
- v1.6 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---
*Requirements defined: 2026-04-16*
*Last updated: 2026-04-16 after defining milestone v1.6*
