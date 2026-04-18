# Requirements: EML Symbolic Regression v1.10

**Defined:** 2026-04-18
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Milestone:** v1.10 Search-backed motif library and compiler shortening for logistic and Planck

## v1.10 Requirements

### Baseline Locks

- [x] **BASE-01**: Maintainer can run regression tests that pin archived logistic relaxed compile depth at 27 with no macro hits before motif changes.
- [x] **BASE-02**: Maintainer can run regression tests that pin archived Planck relaxed compile depth at 20 with `scaled_exp_minus_one_template` and `direct_division_template` hits before motif changes.
- [x] **BASE-03**: Maintainer can run regression tests that preserve Michaelis-Menten strict compile depth 12 with `saturation_ratio_template`.
- [x] **BASE-04**: Maintainer can run regression tests that preserve Arrhenius strict compile support through `direct_division_template`.
- [x] **BASE-05**: Maintainer can run regression tests that preserve Shockley strict compile support through `scaled_exp_minus_one_template`.

### Structural Motif Library

- [ ] **MOTIF-01**: Compiler motif matching can operate on validated compilable subexpressions, not only raw symbols, for reciprocal and saturation forms such as `1/(g(x)+b)` and `c*g(x)/(g(x)+b)`.
- [ ] **MOTIF-02**: Compiler exposes a structural exponential-saturation motif for logistic-like laws such as `1/(1+c*exp(a))` or `exp(a)/(exp(a)+c)` without matching formula names or exact demo constants.
- [ ] **MOTIF-03**: Compiler exposes validation-backed low-degree positive-integer power compression, at minimum for `g(x)**2` and `g(x)**3`, and rejects the path when it is not shorter or not validated.
- [ ] **MOTIF-04**: Any bounded motif-search helper records the target family, candidate construction, independent numeric samples, validation verdict, and codified winning template without acting as a general theorem prover.
- [ ] **MOTIF-05**: Every new motif emits macro diagnostics with template name, depth delta, node delta, validation status, and fail-closed reason when rejected.
- [ ] **MOTIF-06**: Compiler fail-closed behavior rejects malformed, unsupported, non-finite, or validation-failing motif variants without mutating support gates.

### Logistic Evidence

- [ ] **LOGI-01**: Logistic strict or relaxed compile depth is materially lower than the archived relaxed depth 27 through a structural macro-backed path.
- [ ] **LOGI-02**: Logistic compile diagnostics include the new exponential-saturation motif in `macro_diagnostics["hits"]` when the motif is responsible for shortening.
- [ ] **LOGI-03**: Logistic is promoted to strict-supported only under the existing shipped gate or an explicitly declared gate that is not silently looser than the shipped one.
- [ ] **LOGI-04**: Logistic warm-start is attempted through the normal benchmark/verifier contract when strict compile support exists.
- [ ] **LOGI-05**: Logistic warm-start evidence records same-AST or verified-equivalent recovery honestly, including verifier status and evidence class.

### Planck Diagnostics

- [ ] **PLAN-01**: Planck relaxed compile depth is materially lower than the archived relaxed depth 20, primarily through reusable motif compression such as low-degree power support.
- [ ] **PLAN-02**: Planck diagnostics report macro hits, compile depth, node count, support status, and reasons for any remaining unsupported/stretch classification.
- [ ] **PLAN-03**: Planck is promoted to strict-supported only if the full compile gate passes without silent relaxation.
- [ ] **PLAN-04**: Planck warm-start is attempted only if strict compile support exists, and verifier-owned recovery remains the promotion gate.
- [ ] **PLAN-05**: Planck remains an unsupported or stretch row if it only improves depth but does not pass the full support and verification contract.

### Benchmarks, CLI, and Artifacts

- [ ] **EVID-01**: Benchmark registry includes focused `v1.10-logistic-evidence` cases for logistic compile and logistic warm-start when strict compile support exists.
- [ ] **EVID-02**: Benchmark registry includes focused `v1.10-planck-diagnostics` cases for Planck compile diagnostics and optional warm-start only when strict support exists.
- [ ] **EVID-03**: CLI can run the focused logistic and Planck suites and writes deterministic artifacts under `artifacts/campaigns/v1.10-logistic-evidence/` and `artifacts/campaigns/v1.10-planck-diagnostics/`.
- [ ] **EVID-04**: Benchmark artifacts record compile support, compile depth, node count, macro hits, warm-start status, verifier status, and unsupported/stretch reasons.
- [ ] **EVID-05**: Test coverage verifies focused suite contracts, CLI artifact paths, baseline preservation, logistic improvement, Planck diagnostic improvement, and motif fail-closed cases.

## Future Requirements

### Search and Recovery

- **FUT-01**: Compare motif-library improvements against matched-budget external symbolic-regression baselines after the compiler-supported law set is stronger.
- **FUT-02**: Add broader motif families beyond the v1.10 short list only after bounded search evidence shows reusable benefit.
- **FUT-03**: Revisit Planck recovery through curriculum or optimizer work if compile-depth reduction is not enough for warm-start verification.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Formula-name recognizers | The milestone must improve reusable structure, not special-case `logistic` or `planck`. |
| Exact-constant recognizers | Matching only constants such as `1.3` and `2` would not be a reusable motif. |
| Silent gate relaxation | Support claims must remain comparable with shipped v1.9 evidence. |
| Calling Planck solved from depth reduction alone | Planck promotion requires strict support and verifier-owned recovery. |
| General theorem proving | Bounded motif search is allowed only as evidence for specific reusable templates. |
| Broad paper/reporting package refresh | This milestone is compiler science; reporting updates should be focused evidence only. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BASE-01 | Phase 54 | Complete |
| BASE-02 | Phase 54 | Complete |
| BASE-03 | Phase 54 | Complete |
| BASE-04 | Phase 54 | Complete |
| BASE-05 | Phase 54 | Complete |
| MOTIF-01 | Phase 55 | Pending |
| MOTIF-02 | Phase 56 | Pending |
| MOTIF-03 | Phase 57 | Pending |
| MOTIF-04 | Phase 57 | Pending |
| MOTIF-05 | Phase 55 | Pending |
| MOTIF-06 | Phase 55 | Pending |
| LOGI-01 | Phase 56 | Pending |
| LOGI-02 | Phase 56 | Pending |
| LOGI-03 | Phase 56 | Pending |
| LOGI-04 | Phase 56 | Pending |
| LOGI-05 | Phase 56 | Pending |
| PLAN-01 | Phase 57 | Pending |
| PLAN-02 | Phase 57 | Pending |
| PLAN-03 | Phase 57 | Pending |
| PLAN-04 | Phase 57 | Pending |
| PLAN-05 | Phase 57 | Pending |
| EVID-01 | Phase 58 | Pending |
| EVID-02 | Phase 58 | Pending |
| EVID-03 | Phase 58 | Pending |
| EVID-04 | Phase 58 | Pending |
| EVID-05 | Phase 58 | Pending |

**Coverage:**
- v1.10 requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0

---
*Requirements defined: 2026-04-18*
*Last updated: 2026-04-18 after Phase 54*
