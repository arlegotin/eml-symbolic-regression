# Roadmap: EML Symbolic Regression

**Created:** 2026-04-15
**Granularity:** Coarse
**Mode:** YOLO
**Coverage:** 24 v1 requirements mapped, 0 unmapped

## Phase Summary

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Semantics, AST, and Deterministic Artifacts | Establish exact EML meaning and formula artifacts before training. | SEM-01, SEM-02, SEM-03, SEM-04 | 5 |
| 2 | Complete Master Trees and Soft Evaluation | Prove complete depth-bounded trees are reachable and differentiable. | TREE-01, TREE-02, TREE-03, TREE-04 | 5 |
| 3 | Optimizer, Restarts, Hardening, and Recovery Statuses | Turn soft search into exact snapped candidates with honest statuses. | OPT-01, OPT-02, OPT-03, OPT-04 | 5 |
| 4 | Verifier and Acceptance Contract | Make `recovered` a verifier-owned post-snap status. | VER-01, VER-02, VER-03 | 4 |
| 5 | Local Cleanup, SymPy Export, and Reports | Improve readability while preserving verifier authority. | CLEAN-01, CLEAN-02, CLEAN-03 | 4 |
| 6 | Demo Harness and Public Showcase | Run reproducible demos from `sources/FOR_DEMO.md`. | DEMO-01, DEMO-02, DEMO-03, DEMO-04 | 5 |
| 7 | Tests and Documentation | Lock the implementation down with tests and usage docs. | TEST-01, TEST-02 | 4 |

## Phase Details

### Phase 1: Semantics, AST, and Deterministic Artifacts

**Goal:** Build the exact EML foundation that all search, cleanup, and verification depends on.

**Requirements:** SEM-01, SEM-02, SEM-03, SEM-04

**UI hint:** no

**Success criteria:**
1. `eml(x, y) = exp(x) - log(y)` is available in canonical verification mode and stabilized training mode.
2. Exact AST nodes for constants, variables, and ordered EML calls can evaluate with torch, NumPy-style arrays, and mpmath-compatible values.
3. AST JSON serialization is deterministic and round-trips without losing semantics metadata.
4. Paper identities for `exp(x)` and `ln(x)` evaluate correctly on safe positive domains.
5. Tests document branch-sensitive and non-finite behavior rather than hiding it.

### Phase 2: Complete Master Trees and Soft Evaluation

**Goal:** Implement the complete depth-bounded master tree scaffold and prove formulas are reachable before optimizing.

**Requirements:** TREE-01, TREE-02, TREE-03, TREE-04

**UI hint:** no

**Success criteria:**
1. Users can construct univariate and small multivariate master trees at a chosen depth.
2. Slot catalogs expose legal choices for leaf and internal inputs.
3. The univariate parameter count follows the paper's `5 * 2^n - 6` result for one variable.
4. PyTorch `complex128` soft evaluation returns batched predictions and anomaly diagnostics.
5. Hand-set hard gates reproduce at least `exp(x)` and `ln(x)` through exact snapped ASTs.

### Phase 3: Optimizer, Restarts, Hardening, and Recovery Statuses

**Goal:** Add search mechanics that produce exact candidates without claiming recovery prematurely.

**Requirements:** OPT-01, OPT-02, OPT-03, OPT-04

**UI hint:** no

**Success criteria:**
1. Adam-based optimization supports seeds, restarts, temperature annealing, entropy penalty, size penalty, and stability penalty.
2. Training records loss terms, gate entropy, anomaly counts, and best restart metadata.
3. Hardening snaps active gates deterministically with snap margins and post-snap loss.
4. Result statuses distinguish soft fits, snapped candidates, verified recoveries, and failures.
5. Run manifests capture enough metadata to reproduce a search attempt.

### Phase 4: Verifier and Acceptance Contract

**Goal:** Ensure no formula is called recovered until exact post-snap verification passes.

**Requirements:** VER-01, VER-02, VER-03

**UI hint:** no

**Success criteria:**
1. Snapped formulas are evaluated on training, held-out interpolation, extrapolation, and high-precision point sets.
2. Verification reports include tolerances, max errors, imaginary residue, and pass/fail by split.
3. Failure reason codes are machine-readable and CLI-visible.
4. Only the verifier can emit `recovered` status.

### Phase 5: Local Cleanup, SymPy Export, and Reports

**Goal:** Make formulas readable and smaller without letting symbolic presentation bypass verification.

**Requirements:** CLEAN-01, CLEAN-02, CLEAN-03

**UI hint:** no

**Success criteria:**
1. Exact EML ASTs export to SymPy expressions and readable strings.
2. Targeted cleanup passes can reduce inert or duplicate structure.
3. Cleanup candidates are accepted only after verification remains valid.
4. Reports show tree size and verification status before and after cleanup.

### Phase 6: Demo Harness and Public Showcase

**Goal:** Provide reproducible demo runs for the examples and sequence in `sources/FOR_DEMO.md`.

**Requirements:** DEMO-01, DEMO-02, DEMO-03, DEMO-04

**UI hint:** no

**Success criteria:**
1. Demo specs generate normalized synthetic data with train, held-out, and extrapolation splits.
2. CLI commands run demo pipelines and write JSON reports.
3. Smoke demos cover paper-like `exp(x)` / `ln(x)` and simple exponential decay.
4. Showcase specs exist for Michaelis-Menten, logistic growth, Shockley diode, damped oscillator, and normalized Planck.
5. Reports clearly distinguish verified exact EML recoveries from warm-start/catalog showcase candidates and unsupported/harder targets.

### Phase 7: Tests and Documentation

**Goal:** Make the project usable and defensible as a paper-grounded implementation.

**Requirements:** TEST-01, TEST-02

**UI hint:** no

**Success criteria:**
1. `python -m pytest` covers semantics, AST JSON, master-tree construction, snapping, verification, cleanup, CLI, and demos.
2. Documentation explains the paper grounding, the hybrid pipeline, and the limits on blind deep recovery.
3. Demo instructions use examples from `sources/FOR_DEMO.md`.
4. The repository can be inspected from a clean checkout without needing external services.

## Dependency Order

```text
Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6 -> Phase 7
```

The order is intentionally linear. Semantics and exact artifacts define what the system means; master-tree construction proves reachability; optimization generates candidates; verification owns recovery claims; cleanup improves readability; demos exercise the verified pipeline; tests and docs lock the result down.

## Requirement Coverage

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

**Coverage:** 24/24 v1 requirements mapped.

---
*Roadmap created: 2026-04-15*
