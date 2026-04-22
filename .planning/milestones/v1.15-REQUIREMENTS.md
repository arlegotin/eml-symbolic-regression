# Requirements: EML Symbolic Regression v1.15

**Defined:** 2026-04-22
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## v1.15 Requirements

This milestone introduces the parameterized `GEML_a` family, specializes `a = i*pi` as the primary oscillatory example, proves restricted-domain identities, and compares i*pi EML against raw EML under matched symbolic-regression protocols.

### GEML Family Semantics

- [x] **GEML-01**: The system can represent `GEML_a(x, y) = exp(a*x) - log(y)/a` for explicit nonzero complex `a`.
- [x] **GEML-02**: EML is available as the named `GEML_a` specialization `a = 1`, and i*pi EML is available as the named specialization `a = i*pi`.
- [x] **GEML-03**: PyTorch, NumPy, and mpmath evaluators agree on `GEML_a` semantics within their existing training and verification contracts.
- [x] **GEML-04**: Exact AST, JSON, and SymPy export preserve the operator family parameter and named specialization metadata.
- [x] **GEML-05**: Tests and theory docs center the identity `exp(a*GEML_a(u, v)) = exp(a*exp(a*u))/v` for representative complex `a` values.

### Restricted i*pi EML Theory

- [x] **THRY-01**: Theory artifacts prove or executable-check `i*pi EML(i*pi EML(1, y), 1) = -1/y` on the declared positive-real domain `y > 0`.
- [x] **THRY-02**: Theory artifacts prove or executable-check the nested identity that recovers `y` from the i*pi EML reciprocal construction on `y > 0`, with branch assumptions stated.
- [x] **THRY-03**: Theory artifacts derive real-axis sensitivity `d/dx i*pi EML(x, y) = i*pi*exp(i*pi*x)` and `|d/dx| = pi` for real `x`.
- [x] **THRY-04**: Theory artifacts derive the one-step composition identity and magnitude bound `exp(-pi)/v <= |i*pi EML(i*pi EML(u, v), 1)| <= exp(pi)/v` for real `u` and `v > 0`.
- [x] **THRY-05**: Any closure or completeness language is restricted to the exact class actually proven or tested, and explicitly avoids claiming full scientific-calculator universality.

### Branch and Numerics

- [x] **BRAN-01**: i*pi EML implementation and docs specify the complex-log branch convention used by training, snapping, and verification.
- [x] **BRAN-02**: Evaluators record branch-cut proximity and branch-crossing diagnostics for second-slot inputs, especially near the negative real axis.
- [x] **BRAN-03**: Training supports an optional branch-safety penalty or guard that discourages invalid second-slot paths without changing faithful verification semantics.
- [x] **BRAN-04**: Verification and reports expose branch anomalies, invalid-domain skips, and branch-related candidate failures as first-class artifact fields.

### Training and Snapping Integration

- [x] **TRN-01**: The complete soft master tree can run with fixed `GEML_a` specializations while preserving the raw EML default behavior.
- [x] **TRN-02**: Optimizer, hardening, snapping, exact-candidate pooling, cleanup, and refit paths work for i*pi EML without reusing raw EML-only witnesses silently.
- [x] **TRN-03**: Training artifacts include gradient-norm statistics, overflow counts, NaN counts, branch diagnostics, pre-snap MSE, post-snap MSE, and wall-clock metadata.
- [x] **TRN-04**: Regression tests prove existing raw EML semantics, raw benchmark contracts, and v1.14 claim-accounting checks remain unchanged.

### Benchmark Protocol

- [x] **BENCH-01**: The benchmark registry includes periodic targets such as `sin(pi*x)`, `cos(pi*x)`, and simple harmonic sums with normalized domains.
- [x] **BENCH-02**: The benchmark registry includes damped oscillation, wave, Helmholtz-style, or standing-wave targets that match i*pi EML's phase bias.
- [x] **BENCH-03**: The benchmark registry includes log-periodic or amplitude/phase targets such as `x^beta*cos(omega*log(x)+phi)` on safe positive domains.
- [x] **BENCH-04**: The benchmark registry includes negative controls such as `exp(x)`, `log(x)`, polynomials, and rational functions.
- [x] **BENCH-05**: Campaign manifests lock the same tree depths, optimizer, initialization budget, snapping rule, verifier gates, and split policy for EML and i*pi EML comparisons.

### Evidence and Claims

- [x] **EVID-01**: A paired campaign runner emits matched EML and i*pi EML rows for each benchmark target under the same protocol.
- [x] **EVID-02**: Aggregate artifacts compute blind exact-recovery rate after snapping, MSE before and after snapping, gradient statistics, overflow/NaN counts, branch counts, wall-clock time, and available resource metadata.
- [x] **EVID-03**: Reports classify i*pi EML wins, losses, and neutral results by target family, including natural-bias targets and negative controls.
- [x] **EVID-04**: Claim-audit checks reject global superiority, broad blind-recovery, or full-universality language unless backed by the appropriate proof or evidence.
- [x] **EVID-05**: The final milestone package includes a theory note, benchmark manifests, aggregate tables, and a claim-boundary summary suitable for deciding whether i*pi EML deserves a paper section.

## Future Requirements

Deferred unless explicitly promoted into the active roadmap.

- **FUT-01**: Search or learn the continuous `a` parameter instead of comparing fixed hand-picked specializations.
- **FUT-02**: Prove a full constructive completeness theorem for some `GEML_a` subfamily if a real proof path emerges.
- **FUT-03**: Add formal theorem-prover certificates for the restricted identities.
- **FUT-04**: Run larger energy/resource benchmark campaigns with standardized hardware metadata.
- **FUT-05**: Extend comparison to external symbolic-regression baselines after the EML versus i*pi EML internal comparison is stable.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Claiming i*pi EML is globally better than EML | The milestone tests a structural bias, not universal superiority. |
| Claiming full scientific-calculator universality for i*pi EML | The user explicitly asked for restricted-domain theorems unless a full proof exists. |
| Optimizing or learning arbitrary `a` values | v1.15 first validates the family contract and the `a = i*pi` specialization. |
| Large blind deep-recovery campaigns | Existing evidence shows depth degradation; v1.15 should start with controlled, matched, shallow-to-moderate comparisons. |
| Reusing raw EML scaffold witnesses under i*pi EML without same-family proof | Prior centered-family work showed witness-family leakage can invalidate claims. |
| Treating branch-cut behavior as a footnote | Branch handling is part of the i*pi EML operator contract. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| GEML-01 | Phase 82 | Complete |
| GEML-02 | Phase 82 | Complete |
| GEML-03 | Phase 82 | Complete |
| GEML-04 | Phase 82 | Complete |
| GEML-05 | Phase 82 | Complete |
| THRY-01 | Phase 83 | Complete |
| THRY-02 | Phase 83 | Complete |
| THRY-03 | Phase 83 | Complete |
| THRY-04 | Phase 83 | Complete |
| THRY-05 | Phase 83 | Complete |
| BRAN-01 | Phase 83 | Complete |
| BRAN-02 | Phase 83 | Complete |
| BRAN-03 | Phase 83 | Complete |
| BRAN-04 | Phase 83 | Complete |
| TRN-01 | Phase 84 | Complete |
| TRN-02 | Phase 84 | Complete |
| TRN-03 | Phase 84 | Complete |
| TRN-04 | Phase 84 | Complete |
| BENCH-01 | Phase 85 | Complete |
| BENCH-02 | Phase 85 | Complete |
| BENCH-03 | Phase 85 | Complete |
| BENCH-04 | Phase 85 | Complete |
| BENCH-05 | Phase 85 | Complete |
| EVID-01 | Phase 86 | Complete |
| EVID-02 | Phase 86 | Complete |
| EVID-03 | Phase 87 | Complete |
| EVID-04 | Phase 87 | Complete |
| EVID-05 | Phase 87 | Complete |

**Coverage:**
- v1.15 requirements: 28 total
- Mapped to phases: 28
- Unmapped: 0

---
*Requirements defined: 2026-04-22*
*Last updated: 2026-04-22 after v1.15 milestone audit*
