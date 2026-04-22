# Requirements: EML Symbolic Regression v1.14

**Defined:** 2026-04-21
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## v1.14 Requirements

This milestone repairs evidence accounting and claim surfaces before manuscript or release work continues.

### Recovery Accounting

- [ ] **REC-01**: Run and aggregate schemas separate `verification_outcome` from `evidence_regime` or `discovery_class` so one status field cannot conflate verified support with trained recovery.
- [ ] **REC-02**: Compile-only rows with `start_mode=compile` are classified as verified support when verification passes and cannot increment trained recovery headline numerators.
- [ ] **REC-03**: Package-level aggregate, claim-audit, paper-table, README, and report outputs show the corrected current evidence numbers: 8 trained exact recoveries, 1 compile-only verified support row, 15 unsupported rows, and 0 failed rows.
- [ ] **REC-04**: Regression tests and claim-audit checks fail if any compile-only row contributes to trained recovery headlines.

### Warm-Start Evidence

- [ ] **WARM-01**: Publication-track zero-perturbation same-AST warm-start positives are labeled as exact seed round-trips or same-AST retention, not robust warm-start basin evidence.
- [ ] **WARM-02**: Warm-start tables and reports expose the fields needed to interpret strength of evidence: perturbation noise, warm steps, warm restarts, total restarts, return kind, and same-AST or equivalent-AST status.
- [ ] **WARM-03**: Any robustness or perturbed-basin wording is backed by nonzero perturbation, multiple seeds, and more than one optimization step; otherwise the public text explicitly says robustness was not measured.
- [ ] **WARM-04**: README, report, aggregate, and paper-facing text use exact seed round-trip language for existing publication-track warm-start positives.

### Baseline Claim Surface

- [ ] **BASE-01**: Main README, report, and paper-facing summaries do not use unavailable, unsupported, or denominator-excluded baseline rows as contextual comparison evidence.
- [ ] **BASE-02**: Baseline artifacts clearly expose dependency status, denominator policy, unsupported reasons, and whether each adapter actually launched a fixed-budget run.
- [ ] **BASE-03**: If external baseline adapters remain unavailable or unsupported, baseline discussion is quarantined to appendix, scaffolding, or future-work language.
- [ ] **BASE-04**: Claim-audit checks reject main-surface baseline comparison language unless fixed-budget external baseline rows completed on the same target set and split contract.

### Verifier Correctness

- [ ] **VER-01**: High-precision verification for multivariate splits without `target_mpmath` no longer matches targets using only the first input variable.
- [ ] **VER-02**: Multivariate verification either requires `target_mpmath` or uses a full-row stable lookup key when reconstructing scalar targets.
- [ ] **VER-03**: Tests cover repeated first-coordinate multivariate rows with different remaining coordinates and different target values.
- [ ] **VER-04**: Existing univariate verification behavior remains unchanged while the multivariate bug is fixed.

### Integrated Evidence Rebuild

- [ ] **PUB-01**: The publication evidence package is regenerated after accounting, warm-start labeling, baseline surface, and verifier fixes land.
- [ ] **PUB-02**: README, campaign report, aggregate JSON/Markdown, claim-audit outputs, and paper-facing tables contain no stale 9-row recovered headline.
- [ ] **PUB-03**: CI or release-gate checks lock the corrected schema, corrected headline counts, and absence of compile-only recovery promotion.
- [ ] **PUB-04**: Historical v1.13 artifacts remain inspectable while the corrected package is written with traceable source locks and regeneration commands.

## Future Requirements

Deferred unless explicitly promoted into the active roadmap.

- **FUT-01**: Run a real publication-track perturbation study with nonzero noise grid, multiple seeds, more than one optimization step, retention rates, and equivalence rates.
- **FUT-02**: Install and run fixed-budget PySR plus at least one GP baseline on the same target set and split contracts.
- **FUT-03**: Add venue-specific manuscript prose after v1.14 claim accounting and evidence-surface checks pass.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Counting compile-only verification as trained recovery | This is the primary bug v1.14 exists to prevent. |
| Calling zero-perturbation same-AST warm starts robust basin evidence | Existing rows do not have the perturbation/noise/seed budget needed for that claim. |
| Making optional external baseline installation a milestone blocker | Missing dependencies should be quarantined honestly rather than blocking the accounting repair. |
| Changing the optimizer to improve recovery rates | v1.14 is about claim integrity and verifier correctness, not new discovery performance. |
| Treating Hubble as exact symbolic recovery evidence | It is a real-data fixture and baseline-harness check without a clean symbolic candidate. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| REC-01 | Phase 77 | Pending |
| REC-02 | Phase 77 | Pending |
| REC-03 | Phase 77 | Pending |
| REC-04 | Phase 77 | Pending |
| WARM-01 | Phase 78 | Pending |
| WARM-02 | Phase 78 | Pending |
| WARM-03 | Phase 78 | Pending |
| WARM-04 | Phase 78 | Pending |
| BASE-01 | Phase 79 | Pending |
| BASE-02 | Phase 79 | Pending |
| BASE-03 | Phase 79 | Pending |
| BASE-04 | Phase 79 | Pending |
| VER-01 | Phase 80 | Pending |
| VER-02 | Phase 80 | Pending |
| VER-03 | Phase 80 | Pending |
| VER-04 | Phase 80 | Pending |
| PUB-01 | Phase 81 | Pending |
| PUB-02 | Phase 81 | Pending |
| PUB-03 | Phase 81 | Pending |
| PUB-04 | Phase 81 | Pending |

**Coverage:**
- v1.14 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-04-21*
*Last updated: 2026-04-21 after v1.14 roadmap creation*
