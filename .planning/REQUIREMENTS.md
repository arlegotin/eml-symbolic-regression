# Requirements: EML Symbolic Regression Milestone v1.2

**Defined:** 2026-04-15
**Milestone:** v1.2 Training Benchmark and Recovery Evidence
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Milestone v1.2 Requirements

Requirements for this milestone only. Completed v1 and v1.1 requirements are recorded as validated capabilities in `.planning/PROJECT.md`.

### Benchmark Contract

- [ ] **BENC-01**: User can define deterministic benchmark suite files containing formula IDs, dataset specs, variable ranges, sample counts, start modes, seeds, perturbation levels, optimizer budgets, verifier settings, and artifact paths.
- [ ] **BENC-02**: User can select built-in suites for fast smoke checks, the full v1.2 evidence matrix, and `sources/FOR_DEMO.md` diagnostics.
- [ ] **BENC-03**: User receives fail-closed validation errors for unknown formulas, invalid start modes, unsafe budgets, missing constants, unsupported compiler gates, or malformed suite files.
- [ ] **BENC-04**: User gets stable run IDs and deterministic artifact locations for every formula/start-mode/seed/perturbation combination.

### Run Execution

- [ ] **RUN-01**: User can run a full benchmark suite or filtered subset from the CLI without hand-writing per-demo commands.
- [ ] **RUN-02**: User can execute blind-start training through the existing optimizer across multiple seeds for shallow supported formulas.
- [ ] **RUN-03**: User can execute compiler warm-start training with perturbation sweeps through the existing compile, embed, train, snap, and verify path.
- [ ] **RUN-04**: User can run suites that contain unsupported, skipped, or failed cases without aborting the entire suite, while preserving those outcomes in artifacts.

### Experiment Matrix

- [ ] **MATR-01**: User can run blind-start baselines for shallow formulas such as `exp`, `log`, radioactive decay, and other low-depth formulas supported by current gates.
- [ ] **MATR-02**: User can run Beer-Lambert perturbation sweeps that include same-basin, mild perturbation, and stronger slot-changing perturbation settings.
- [ ] **MATR-03**: User can run Michaelis-Menten diagnostics that record compiler depth, embedding eligibility, unsupported reasons, and training attempts only when current gates allow them.
- [ ] **MATR-04**: User can run normalized Planck and selected `sources/FOR_DEMO.md` formulas as honest stretch or diagnostic cases without requiring recovery.

### Evidence Reporting

- [ ] **EVID-01**: User receives a per-run JSON artifact containing suite ID, run ID, formula, dataset spec, start mode, seed, perturbation config, optimizer config, losses, snap outcome, active slot changes, verifier status, timing, and errors.
- [ ] **EVID-02**: User receives aggregate JSON and Markdown reports with recovery rates by formula, start mode, perturbation level, depth, and seed group.
- [ ] **EVID-03**: User can distinguish blind recovery, same-AST warm-start return, verified-equivalent warm-start recovery, snapped-but-failed candidates, soft-fit-only attempts, unsupported cases, and execution failures.
- [ ] **EVID-04**: User can compare benchmark runs without losing provenance for suite config, code version, environment summary, and artifact paths.

### Tests and Documentation

- [ ] **TEST-05**: User can run focused pytest coverage for suite parsing, validation, run ID stability, aggregation math, and claim taxonomy.
- [ ] **TEST-06**: User can run a small benchmark smoke test in CI-scale time that exercises at least one blind-start run, one warm-start run, one unsupported/stretch diagnostic, and one aggregate report.
- [ ] **TEST-07**: User can read documentation that explains how to run benchmark suites, how to interpret recovery evidence, and why failures or same-AST returns are not hidden.

## Future Requirements

Deferred to later milestones.

### Optimization and Scaling

- **FUT-06**: User can improve optimizer robustness for slot-changing perturbations after v1.2 measures the failure modes.
- **FUT-07**: User can reduce compiled arithmetic tree depth so Michaelis-Menten can promote under practical warm-start gates.
- **FUT-08**: User can synthesize or fit numeric constants instead of relying on fixed literal constant catalogs.
- **FUT-09**: User can add richer plots or dashboards for benchmark results after the JSON/Markdown evidence contract stabilizes.
- **FUT-10**: User can run long benchmark campaigns with parallel workers, caching, and resumable distributed execution.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Claiming general symbolic-regression success | v1.2 measures current behavior; it does not solve robust deep blind recovery. |
| Hiding failed or unsupported cases | The milestone value is honest evidence, including failures. |
| Optimizer redesign | Algorithm changes should follow measured failure modes, not precede them. |
| Large external real-world datasets | The milestone focuses on reproducible synthetic and source-document demos first. |
| Guaranteed Michaelis-Menten or Planck recovery | Current evidence says these remain gated/stretch until depth and optimizer behavior improve. |
| Heavy visualization stack | JSON and Markdown reports are enough until the evidence schema stabilizes. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| BENC-01 | Phase 14 | Pending |
| BENC-02 | Phase 14 | Pending |
| BENC-03 | Phase 14 | Pending |
| BENC-04 | Phase 14 | Pending |
| RUN-01 | Phase 15 | Pending |
| RUN-02 | Phase 15 | Pending |
| RUN-03 | Phase 15 | Pending |
| RUN-04 | Phase 15 | Pending |
| MATR-01 | Phase 16 | Pending |
| MATR-02 | Phase 16 | Pending |
| MATR-03 | Phase 16 | Pending |
| MATR-04 | Phase 16 | Pending |
| EVID-01 | Phase 17 | Pending |
| EVID-02 | Phase 17 | Pending |
| EVID-03 | Phase 17 | Pending |
| EVID-04 | Phase 17 | Pending |
| TEST-05 | Phase 18 | Pending |
| TEST-06 | Phase 18 | Pending |
| TEST-07 | Phase 18 | Pending |

**Coverage:**
- v1.2 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---
*Requirements defined: 2026-04-15*
*Last updated: 2026-04-15 after milestone v1.2 roadmap creation*
