# Requirements: EML Symbolic Regression v1.9

**Defined:** 2026-04-17
**Milestone:** v1.9 Raw-EML Hybrid Recovery and Paper Suite
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## v1.9 Requirements

### Witness Registry and Centered Scaffold Correctness

- [x] **WIT-01**: Developer can inspect an explicit witness/initializer registry that declares scaffold availability by operator family.
- [x] **WIT-02**: Centered families no longer receive raw `exp`, `log`, or `scaled_exp` scaffold attempts unless a tested same-family witness is registered.
- [x] **WIT-03**: Raw-specific scaffold helpers fail closed or are only reachable through raw-family registry entries.
- [x] **WIT-04**: Benchmark and optimizer artifacts record centered scaffold exclusions with explicit reason codes such as `centered_family_same_family_witness_missing`.

### Arrhenius Exact Recovery

- [ ] **ARR-01**: Developer can generate a normalized Arrhenius demo dataset for `exp(-0.8/x)` over positive domains safely away from zero.
- [ ] **ARR-02**: Developer can strictly compile the Arrhenius target within the supported depth gate and inspect macro diagnostics including `direct_division_template`.
- [ ] **ARR-03**: Developer can run a zero-noise Arrhenius compiler warm start that returns the same exact AST and verifier status `recovered`.
- [ ] **ARR-04**: Developer can reproduce an Arrhenius benchmark or report artifact with compile depth, warm-start status, verifier status, and regime labeling.

### Michaelis-Menten Compiler Motifs

- [ ] **MIC-01**: Developer can compile reciprocal-shift motifs such as `1/(x + b)` or inspect a fail-closed diagnostic explaining remaining unsupported structure.
- [ ] **MIC-02**: Developer can compile or rewrite saturation-ratio motifs such as `(a*x)/(b + x)` through reusable compiler logic rather than a one-off formula recognizer.
- [ ] **MIC-03**: Developer can compare before/after compiler diagnostics for `1/(x+0.5)` and `2*x/(x+0.5)`, including depth, node count, rule trace, and macro hits.
- [ ] **MIC-04**: Developer can run Michaelis-Menten warm-start recovery if strict support reaches the gate, or see an honest unsupported artifact if the macro work only reduces depth.

### Exact Cleanup Expansion

- [ ] **REP-01**: Developer can repair from more than the selected snapped candidate, including fallback and retained exact candidates where available.
- [ ] **REP-02**: Exact cleanup uses AST deduplication and verifier-gated ranking while allowing a larger configurable neighborhood than the v1.6/v1.8 defaults.
- [ ] **REP-03**: Cleanup can consider subtree-level alternatives where candidate provenance exposes them, not only single-slot leaf flips.
- [ ] **REP-04**: Developer can inspect targeted before/after evidence showing whether the expanded cleanup improves declared near-miss subsets without weakening fallback behavior.

### Raw-Hybrid Paper Evidence

- [ ] **RHY-01**: Developer can run a paper-facing raw-hybrid suite or campaign preset that includes shallow blind boundaries, perturbed basin evidence, Beer-Lambert, Shockley, Arrhenius, and Michaelis diagnostics.
- [ ] **RHY-02**: Generated reports keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate.
- [ ] **RHY-03**: Generated scientific-law tables include formula, compile support, compile depth, macro hits, warm-start status, verifier status, and artifact path.
- [ ] **RHY-04**: Centered-family results are reported only as negative diagnostics with the same-family witness caveat, not as an intrinsic impossibility claim.
- [ ] **RHY-05**: README or implementation docs are updated only after successful artifacts exist, with claim language that avoids presenting warm-start recovery as blind discovery.

## Future Requirements

Deferred to later milestones.

### Stretch Recovery Targets

- **LOGI-01**: Researcher can attempt logistic exact recovery after reciprocal/saturation motifs and cleanup improvements are working.
- **PLAN-01**: Researcher can revisit Planck only after compile depth drops materially below the current relaxed-depth stretch result.
- **CURR-01**: Researcher can add a verified growth/curriculum mode that grows exact motifs stage by stage without labeling the result as blind discovery.

### Centered-Family Theory Track

- **CENT-01**: Researcher can construct exact same-family centered witnesses for terminal handling, `exp`, `log`, addition/subtraction, and multiplication/division.
- **CENT-02**: Researcher can build same-family centered compiler seeds before running matched centered empirical comparisons.
- **CENT-03**: Researcher can revisit constructive completeness or interdefinability claims only after witness outputs exist.

### External Comparisons

- **BASE-01**: Researcher can run matched-budget external symbolic-regression baselines after the raw-hybrid internal evidence package is stronger.

## Out of Scope

Explicitly excluded for v1.9.

| Feature | Reason |
|---------|--------|
| More large centered-family campaigns | v1.8 showed zero positive centered signal and same-family witnesses are still missing. |
| Claiming centered families are intrinsically impossible | The current evidence is negative but theory-incomplete. |
| Planck as a flagship solved result | Current compile diagnostics place Planck materially deeper than Michaelis and Arrhenius. |
| Logistic as a must-have result | Logistic is worth attempting only after Michaelis and motif cleanup are stronger. |
| Relaxing depth gates silently | Gate changes must be explicit and cannot substitute for genuine compile shortening. |
| Formula-specific hardcoded recognizers | Motif macros must be reusable structures, not one-off shortcuts for paper rows. |
| Presenting warm-start as blind discovery | Evidence regimes remain separate by design. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| WIT-01 | Phase 49 | Complete |
| WIT-02 | Phase 49 | Complete |
| WIT-03 | Phase 49 | Complete |
| WIT-04 | Phase 49 | Complete |
| ARR-01 | Phase 50 | Pending |
| ARR-02 | Phase 50 | Pending |
| ARR-03 | Phase 50 | Pending |
| ARR-04 | Phase 50 | Pending |
| MIC-01 | Phase 51 | Pending |
| MIC-02 | Phase 51 | Pending |
| MIC-03 | Phase 51 | Pending |
| MIC-04 | Phase 51 | Pending |
| REP-01 | Phase 52 | Pending |
| REP-02 | Phase 52 | Pending |
| REP-03 | Phase 52 | Pending |
| REP-04 | Phase 52 | Pending |
| RHY-01 | Phase 53 | Pending |
| RHY-02 | Phase 53 | Pending |
| RHY-03 | Phase 53 | Pending |
| RHY-04 | Phase 53 | Pending |
| RHY-05 | Phase 53 | Pending |

**Coverage:**
- v1.9 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

---
*Requirements defined: 2026-04-17*
*Last updated: 2026-04-17 after roadmap creation*
