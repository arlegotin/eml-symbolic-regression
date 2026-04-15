# Requirements: EML Symbolic Regression

**Defined:** 2026-04-15
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## v1 Requirements

### Semantics

- [x] **SEM-01**: User can evaluate `eml(x, y) = exp(x) - log(y)` with explicit canonical verification semantics and separate stabilized training semantics.
- [x] **SEM-02**: User can represent exact EML formulas as immutable AST nodes for constants, variables, and ordered `eml(left, right)` expressions.
- [x] **SEM-03**: User can serialize and deserialize exact EML ASTs as deterministic JSON with semantics metadata.
- [x] **SEM-04**: User can reproduce paper-grounded identities such as `exp(x) = eml(x, 1)` and `ln(x) = eml(1, eml(eml(1, x), 1))` on safe domains.

### Master Trees

- [x] **TREE-01**: User can create complete depth-bounded EML master-tree specs for univariate and small multivariate inputs.
- [x] **TREE-02**: User can inspect slot choices where leaf slots choose constants/variables and internal slots may also choose previous subtree outputs.
- [x] **TREE-03**: User can evaluate master trees in PyTorch `complex128` with soft categorical gates and per-node anomaly diagnostics.
- [x] **TREE-04**: User can hand-set one-hot gates to prove known formulas are reachable before optimization is attempted.

### Optimization and Snapping

- [x] **OPT-01**: User can run Adam-based optimization with deterministic seeds, multiple restarts, temperature annealing, entropy regularization, size penalty, and numerical-stability penalty.
- [x] **OPT-02**: User can harden soft gates into exact one-hot choices with deterministic tie-breaking, snap margins, and post-snap loss reporting.
- [x] **OPT-03**: User can distinguish result statuses such as `soft_fit`, `snapped_candidate`, `verified`, and `failed` so low loss is not mislabeled as recovery.
- [x] **OPT-04**: User can write run manifests containing config, seed, depth, losses, anomaly counts, snap decisions, artifacts, and verification status.

### Verification

- [x] **VER-01**: User can verify snapped formulas against training, held-out interpolation, extrapolation, and mpmath high-precision point sets.
- [x] **VER-02**: User receives pass/fail reason codes for failed recovery attempts, including fit failure, unstable snap, held-out failure, extrapolation failure, and high-precision failure.
- [x] **VER-03**: User can only receive `recovered` status from the verifier after post-snap exact AST evaluation passes configured tolerances.

### Cleanup and Export

- [x] **CLEAN-01**: User can export snapped EML ASTs to SymPy expressions and readable strings.
- [x] **CLEAN-02**: User can run targeted cleanup passes and bounded local candidate checks without relying on generic symbolic simplification as the sole oracle.
- [x] **CLEAN-03**: User can compare tree size and verification results before and after cleanup.

### Demos and CLI

- [x] **DEMO-01**: User can generate normalized synthetic datasets for the demo ladder in `sources/FOR_DEMO.md`.
- [x] **DEMO-02**: User can run CLI commands that execute demo experiments, snap candidates, verify formulas, and write JSON reports.
- [x] **DEMO-03**: User can run reliable smoke demos for paper-like `exp(x)` / `ln(x)` and simple exponential decay.
- [x] **DEMO-04**: User can run showcase demos for Michaelis-Menten, logistic growth, Shockley diode, damped oscillator, and normalized Planck as feasible targets with honest success/failure diagnostics.

### Tests and Documentation

- [x] **TEST-01**: User can run a pytest suite covering EML semantics, AST JSON, master-tree construction, soft evaluation, snapping, verification, cleanup, CLI, and demos.
- [x] **TEST-02**: User can read documentation explaining the paper grounding, project limits, demo strategy, and how to reproduce tests/showcases.

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
| SEM-01 | Phase 1 | Complete |
| SEM-02 | Phase 1 | Complete |
| SEM-03 | Phase 1 | Complete |
| SEM-04 | Phase 1 | Complete |
| TREE-01 | Phase 2 | Complete |
| TREE-02 | Phase 2 | Complete |
| TREE-03 | Phase 2 | Complete |
| TREE-04 | Phase 2 | Complete |
| OPT-01 | Phase 3 | Complete |
| OPT-02 | Phase 3 | Complete |
| OPT-03 | Phase 3 | Complete |
| OPT-04 | Phase 3 | Complete |
| VER-01 | Phase 4 | Complete |
| VER-02 | Phase 4 | Complete |
| VER-03 | Phase 4 | Complete |
| CLEAN-01 | Phase 5 | Complete |
| CLEAN-02 | Phase 5 | Complete |
| CLEAN-03 | Phase 5 | Complete |
| DEMO-01 | Phase 6 | Complete |
| DEMO-02 | Phase 6 | Complete |
| DEMO-03 | Phase 6 | Complete |
| DEMO-04 | Phase 6 | Complete |
| TEST-01 | Phase 7 | Complete |
| TEST-02 | Phase 7 | Complete |

**Coverage:**
- v1 requirements: 24 total
- Mapped to phases: 24
- Unmapped: 0

---
*Requirements defined: 2026-04-15*
*Last updated: 2026-04-15 after implementation and verification*
