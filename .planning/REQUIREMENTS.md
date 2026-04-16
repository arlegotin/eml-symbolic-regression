# Requirements: EML Symbolic Regression Milestone v1.7

**Defined:** 2026-04-16
**Milestone:** v1.7 Centered-Family Baseline and Paper Decision
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Milestone v1.7 Requirements

Requirements for this milestone only. Completed v1 through v1.6 requirements are recorded as validated capabilities in `.planning/PROJECT.md` and archived milestone files under `.planning/milestones/`.

### Operator Family Semantics and Exact Forms

- [x] **OPF-01**: User can evaluate `raw_eml`, `cEML_{s,t}`, `CEML_s`, and `ZEML_s` through explicit training and verification semantics that preserve the existing PyTorch `complex128` default.
- [x] **OPF-02**: User can rely on `expm1` and `log1p` implementations for centered-family nodes, with faithful verification behavior separated from any training-mode clamps or guards.
- [x] **OPF-03**: User can serialize, deserialize, snap, and inspect exact AST nodes that record operator family, scale `s`, shift `t`, terminal convention, and child structure.
- [x] **OPF-04**: User can evaluate centered-family exact ASTs through SymPy and high-precision mpmath paths without collapsing them into raw-EML-only reporting.
- [x] **OPF-05**: User can inspect anomaly diagnostics for centered nodes, including non-finite intermediates, `expm1` overflow pressure, `log1p` branch or domain events, and distance to the shifted singularity.

### Family-Aware Training and Recovery

- [x] **TRN-01**: User can run the soft master tree with a fixed operator family selected per run, including raw EML, `CEML_s`, and `ZEML_s` for declared `s` values.
- [x] **TRN-02**: User can snap and rank exact centered-family candidates with the same verifier-owned candidate-pool, fallback, cleanup, repair, and refit discipline used for raw EML.
- [x] **TRN-03**: User can use compiler or warm-start support for centered-family trees where validated rules exist, while unsupported transforms fail closed with explicit diagnostics.
- [x] **TRN-04**: User can run scheduled `s` continuation experiments, such as `8 -> 4 -> 2 -> 1` and `8 -> 4`, with schedule metadata preserved in run artifacts.
- [x] **TRN-05**: User can compare centered-family runs against raw EML without changing existing raw-EML defaults or regressing archived v1.6 proof behavior.

### Comparative Experiment Matrix and Evidence

- [ ] **EVD-01**: User can rerun `proof-shallow-pure-blind`, `proof-shallow`, `proof-basin`, and `proof-depth-curve` under selected raw, `CEML_s`, `ZEML_s`, and continuation variants.
- [ ] **EVD-02**: User can run v1.6-standard and v1.6-showcase style campaigns for operator-family comparisons without overwriting archived v1.6 artifacts.
- [ ] **EVD-03**: User receives aggregate tables for exact recovery rate by regime, depth, operator family, scale, continuation schedule, and target formula.
- [ ] **EVD-04**: User receives aggregate diagnostics for anomaly rates, post-snap verifier pass rates, repair/refit usage, and formula depth or length overhead.
- [ ] **EVD-05**: User can run regression and smoke tests that prove family-aware changes preserve raw EML semantics, existing benchmark commands, and reporting contracts.

### Paper Decision and Claim Boundaries

- [ ] **PAP-01**: User receives a decision memo that chooses between publishing a robustness/geometry paper now or waiting for a stronger successor-family paper.
- [ ] **PAP-02**: User receives safe claim language for the centered/scaled family, including centering, normalized local Jacobian, curvature control, shifted singularity, and subtraction-limit behavior.
- [ ] **PAP-03**: User receives explicit unsafe-claim warnings for unproved `CEML_s` completeness, `ZEML_s` terminal-0 limitations, universal recovery, and pocket-calculator replacement claims.
- [ ] **PAP-04**: User receives a figure and table inventory centered on exact recovery versus depth, supported by anomaly, repair/refit, verifier, and overhead evidence.
- [ ] **PAP-05**: User can inspect any constructive completeness or interdefinability search outputs for `CEML_s` as experimental evidence, with incomplete results labeled as such.

## Future Requirements

Deferred to later milestones.

### Publication and External Comparison

- **FUT-28**: User can run matched-budget external symbolic-regression baselines such as PySR, AI Feynman, PhySO, or ParFam against the finalized centered-family benchmark matrix.
- **FUT-29**: User can produce a full manuscript draft, response-paper package, or arXiv submission after the v1.7 evidence and decision memo are reviewed.
- **FUT-30**: User can run a broader constructive completeness search or formal interdefinability proof attempt for selected `CEML_s` values.
- **FUT-31**: User can evaluate noisy external datasets, unit-heavy scientific formulas, or non-synthetic datasets after synthetic proof behavior is stable.
- **FUT-32**: User can investigate learnable or per-node operator-family parameters after fixed-family and scheduled-family baselines are understood.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Claiming `CEML_s` is complete for all `s > 0` | This requires proof or constructive witnesses beyond implementation support. |
| Treating `ZEML_s` as a terminal-1 completeness replacement | Closed zero-terminal `ZEML_s` trees do not generate new constants. |
| Collapsing pure-blind, scaffolded, compile-only, warm-start, repaired, and perturbed-basin evidence into one recovery metric | Regime separation is required for honest publication claims. |
| Replacing archived v1.6 proof artifacts | v1.6 remains the raw-EML baseline anchor for this milestone. |
| Matched-budget external baseline competitions | Useful for publication, but deferred until the operator-family comparison is implemented and measured. |
| Custom CUDA kernels or throughput-first acceleration | v1.7 is about training geometry and exact recovery evidence, not hardware optimization. |
| Full manuscript drafting | This milestone produces the evidence-backed paper decision and claim inventory, not the final paper. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

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
| EVD-01 | Phase 41 | Pending |
| EVD-02 | Phase 41 | Pending |
| EVD-03 | Phase 42 | Pending |
| EVD-04 | Phase 42 | Pending |
| EVD-05 | Phase 42 | Pending |
| PAP-01 | Phase 43 | Pending |
| PAP-02 | Phase 43 | Pending |
| PAP-03 | Phase 43 | Pending |
| PAP-04 | Phase 43 | Pending |
| PAP-05 | Phase 43 | Pending |

**Coverage:**
- v1.7 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-04-16*
*Last updated: 2026-04-16 after completing Phase 40 family-aware training pipeline*
