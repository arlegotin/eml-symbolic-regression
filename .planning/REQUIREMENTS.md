# Requirements: EML Symbolic Regression

**Defined:** 2026-04-15
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## v1 Requirements

### Semantics

- [ ] **SEM-01**: User can evaluate `eml(x, y) = exp(x) - log(y)` with explicit canonical verification semantics and separate stabilized training semantics.
- [ ] **SEM-02**: User can represent exact EML formulas as immutable AST nodes for constants, variables, and ordered `eml(left, right)` expressions.
- [ ] **SEM-03**: User can serialize and deserialize exact EML ASTs as deterministic JSON with semantics metadata.
- [ ] **SEM-04**: User can reproduce paper-grounded identities such as `exp(x) = eml(x, 1)` and `ln(x) = eml(1, eml(eml(1, x), 1))` on safe domains.

### Master Trees

- [ ] **TREE-01**: User can create complete depth-bounded EML master-tree specs for univariate and small multivariate inputs.
- [ ] **TREE-02**: User can inspect slot choices where leaf slots choose constants/variables and internal slots may also choose previous subtree outputs.
- [ ] **TREE-03**: User can evaluate master trees in PyTorch `complex128` with soft categorical gates and per-node anomaly diagnostics.
- [ ] **TREE-04**: User can hand-set one-hot gates to prove known formulas are reachable before optimization is attempted.

### Optimization and Snapping

- [ ] **OPT-01**: User can run Adam-based optimization with deterministic seeds, multiple restarts, temperature annealing, entropy regularization, size penalty, and numerical-stability penalty.
- [ ] **OPT-02**: User can harden soft gates into exact one-hot choices with deterministic tie-breaking, snap margins, and post-snap loss reporting.
- [ ] **OPT-03**: User can distinguish result statuses such as `soft_fit`, `snapped_candidate`, `verified`, and `failed` so low loss is not mislabeled as recovery.
- [ ] **OPT-04**: User can write run manifests containing config, seed, depth, losses, anomaly counts, snap decisions, artifacts, and verification status.

### Verification

- [ ] **VER-01**: User can verify snapped formulas against training, held-out interpolation, extrapolation, and mpmath high-precision point sets.
- [ ] **VER-02**: User receives pass/fail reason codes for failed recovery attempts, including fit failure, unstable snap, held-out failure, extrapolation failure, and high-precision failure.
- [ ] **VER-03**: User can only receive `recovered` status from the verifier after post-snap exact AST evaluation passes configured tolerances.

### Cleanup and Export

- [ ] **CLEAN-01**: User can export snapped EML ASTs to SymPy expressions and readable strings.
- [ ] **CLEAN-02**: User can run targeted cleanup passes and bounded local candidate checks without relying on generic symbolic simplification as the sole oracle.
- [ ] **CLEAN-03**: User can compare tree size and verification results before and after cleanup.

### Demos and CLI

- [ ] **DEMO-01**: User can generate normalized synthetic datasets for the demo ladder in `sources/FOR_DEMO.md`.
- [ ] **DEMO-02**: User can run CLI commands that execute demo experiments, snap candidates, verify formulas, and write JSON reports.
- [ ] **DEMO-03**: User can run reliable smoke demos for paper-like `exp(x)` / `ln(x)` and simple exponential decay.
- [ ] **DEMO-04**: User can run showcase demos for Michaelis-Menten, logistic growth, Shockley diode, damped oscillator, and normalized Planck as feasible targets with honest success/failure diagnostics.

### Tests and Documentation

- [ ] **TEST-01**: User can run a pytest suite covering EML semantics, AST JSON, master-tree construction, soft evaluation, snapping, verification, cleanup, CLI, and demos.
- [ ] **TEST-02**: User can read documentation explaining the paper grounding, project limits, demo strategy, and how to reproduce tests/showcases.

## v2 Requirements

### Scaling

- **SCALE-01**: User can fit symbolic scaffolds with continuous coefficients after the discrete EML structure is discovered.
- **SCALE-02**: User can run Rust-accelerated local search or verification once Python profiling identifies a bottleneck.
- **SCALE-03**: User can run custom CUDA kernels for batched candidate scoring when standard PyTorch is insufficient.
- **SCALE-04**: User can benchmark noisy real-world datasets with priors and compare against conventional symbolic-regression baselines.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Blind arbitrary depth-6 recovery | The paper reports no blind depth-6 recovery in 448 attempts; v1 must not overpromise this. |
| Raw SI-unit Planck law as a first demo | Unit constants and scaling obscure the core EML idea; use normalized Planck instead. |
| GUI or web application | The north-star MVP is a package, CLI, tests, and reproducible demos. |
| Formal theorem-prover equivalence | v1 uses numeric, high-precision, and targeted symbolic verification. |
| Generic heterogeneous operator-menu search | This repo exists to test complete EML-tree search, not conventional operator-set symbolic regression. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SEM-01 | Phase 1 | Pending |
| SEM-02 | Phase 1 | Pending |
| SEM-03 | Phase 1 | Pending |
| SEM-04 | Phase 1 | Pending |
| TREE-01 | Phase 2 | Pending |
| TREE-02 | Phase 2 | Pending |
| TREE-03 | Phase 2 | Pending |
| TREE-04 | Phase 2 | Pending |
| OPT-01 | Phase 3 | Pending |
| OPT-02 | Phase 3 | Pending |
| OPT-03 | Phase 3 | Pending |
| OPT-04 | Phase 3 | Pending |
| VER-01 | Phase 4 | Pending |
| VER-02 | Phase 4 | Pending |
| VER-03 | Phase 4 | Pending |
| CLEAN-01 | Phase 5 | Pending |
| CLEAN-02 | Phase 5 | Pending |
| CLEAN-03 | Phase 5 | Pending |
| DEMO-01 | Phase 6 | Pending |
| DEMO-02 | Phase 6 | Pending |
| DEMO-03 | Phase 6 | Pending |
| DEMO-04 | Phase 6 | Pending |
| TEST-01 | Phase 7 | Pending |
| TEST-02 | Phase 7 | Pending |

**Coverage:**
- v1 requirements: 24 total
- Mapped to phases: 24
- Unmapped: 0

---
*Requirements defined: 2026-04-15*
*Last updated: 2026-04-15 after initial definition*
