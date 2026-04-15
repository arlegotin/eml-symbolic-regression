# Requirements: EML Symbolic Regression Milestone v1.1

**Defined:** 2026-04-15
**Milestone:** v1.1 EML Compiler and Warm Starts
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Milestone v1.1 Requirements

Requirements for this milestone only. Completed v1 requirements are recorded as validated capabilities in `.planning/PROJECT.md`.

### Compiler Contract

- [ ] **COMP-01**: User can compile a whitelisted SymPy subset into the existing exact EML `Expr` AST type without introducing a parallel AST.
- [ ] **COMP-02**: User receives structured compiler metadata including source expression, normalized expression, rule trace, variables, constants, depth, node count, domain assumptions, and unsupported reason codes.
- [ ] **COMP-03**: User can validate compiled AST output against independent ordinary-expression evaluation before the output is eligible for warm-start training.
- [ ] **COMP-04**: User receives fail-closed errors for unsupported operators, unsupported powers, unknown variables, unsafe constants, or expressions that exceed configured depth/node budgets.

### Constants and Embedding

- [ ] **CONST-01**: User can choose an explicit constant policy, with v1.1 supporting `literal_constants` while preserving the default pure `const:1` behavior.
- [ ] **CONST-02**: User can construct `SoftEMLTree` instances with a finite constant catalog derived from a compiled expression.
- [ ] **EMBED-01**: User can embed a compiled exact EML AST into a compatible soft master tree by mapping AST nodes to slot logits.
- [ ] **EMBED-02**: User gets immediate embed-to-snap validation that proves the high-strength warm start snaps back to the compiled AST before perturbation.
- [ ] **EMBED-03**: User receives actionable diagnostics for depth-too-small, missing-constant, missing-variable, and incompatible-tree failures before training starts.

### Arithmetic Rules

- [ ] **ARITH-01**: User can compile direct `exp` and `log` rules over arbitrary supported subexpressions.
- [ ] **ARITH-02**: User can compile unary negation, subtraction, addition, multiplication, reciprocal, and division through tested EML rule templates or receive explicit unsupported/depth failure reasons.
- [ ] **ARITH-03**: User can compile small integer powers only when implemented behind explicit max-power and depth gates.

### Warm-Start Recovery

- [ ] **WARM-01**: User can run deterministic perturbation of compiled warm-start logits with recorded strength, noise scale, seed, active slot changes, and pre/post perturbation snap summaries.
- [ ] **WARM-02**: User can train from compiled warm starts through the existing optimizer path without allowing the optimizer to label a result `recovered`.
- [ ] **WARM-03**: User receives a warm-start manifest containing compiler metadata, terminal bank, embedding assignments, perturbation config, optimizer config, snap decisions, anomaly stats, and verification outcome.
- [ ] **WARM-04**: User can distinguish same-AST return, verified-equivalent AST, snapped-but-failed candidate, soft-fit-only, and failed warm-start attempts.

### Demo Promotion and Reporting

- [ ] **DEMO-05**: User can run Beer-Lambert as a compiler-driven warm-start recovery demo and promote it only when the final trained exact EML AST verifies.
- [ ] **DEMO-06**: User can run Michaelis-Menten as a compiler-driven warm-start recovery demo when arithmetic rules and depth gates pass, and otherwise receive honest unsupported/depth diagnostics.
- [ ] **DEMO-07**: User can run normalized Planck as a stretch compile/warm-start report without making its trained recovery a milestone guarantee.
- [ ] **DEMO-08**: User-facing reports separate catalog showcase, compiled seed, warm-start attempt, trained exact recovery, blind baseline, stretch, unsupported, and failed statuses.

### Tests and Documentation

- [ ] **TEST-03**: User can run pytest coverage for compiler rules, negative compiler cases, constant policy, constant catalog labels, embedding round trips, perturbation determinism, warm-start manifests, and demo promotion gates.
- [ ] **TEST-04**: User can read documentation explaining fixed literal constants, compile-only versus warm-start recovery, demo claim statuses, depth limits, and why this is not blind symbolic discovery.

## Future Requirements

Deferred to later milestones.

### Compiler and Scaling

- **FUT-01**: User can synthesize common numeric constants from the pure `{1, eml}` basis rather than using fixed literal constants.
- **FUT-02**: User can fit continuous coefficients around discovered symbolic scaffolds.
- **FUT-03**: User can compile trig identities and promote damped oscillator to trained EML recovery.
- **FUT-04**: User can run shortest-form or local-search compression of compiled EML trees.
- **FUT-05**: User can use Rust or GPU acceleration after profiling proves a bottleneck.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Claiming warm-start recovery as blind discovery | Warm starts encode the target scaffold; reports must be explicit about provenance. |
| Full SymPy-to-EML coverage | v1.1 needs a tested subset, not broad best-effort compilation. |
| Pure `{1, eml}` synthesis for arbitrary constants | Important later, but v1.1 uses fixed literal constants for practical demos. |
| Learned coefficients | Would change the problem into semi-parametric fitting and blur recovery claims. |
| Guaranteed Planck trained recovery | Planck is a useful stretch target but too risky to promise in this milestone. |
| Trig/oscillator trained recovery | Damped oscillator needs trig identities and phase handling; defer until compiler basics are stable. |

## Traceability

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

**Coverage:**
- v1.1 requirements: 22 total
- Mapped to phases: 22
- Unmapped: 0

---
*Requirements defined: 2026-04-15*
*Last updated: 2026-04-15 after milestone v1.1 definition*
