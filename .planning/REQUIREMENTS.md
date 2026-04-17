# Requirements: EML Symbolic Regression v1.8

**Defined:** 2026-04-16
**Completed:** 2026-04-17
**Milestone:** v1.8 Centered-Family Viability and Full Evidence Run
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## v1.8 Requirements

### Smoke Triage and Blocker Classification

- [x] **TRI-01**: Developer can reproduce a raw-vs-centered `family-smoke` run and inspect per-family recovery, failure, unsupported, and anomaly summaries.
- [x] **TRI-02**: Developer can classify every centered-family smoke failure as missing integration, budget/initializer/schedule behavior, or likely operator behavior with artifact-backed evidence.
- [x] **TRI-03**: Developer can run focused shallow `exp` and `log` calibration probes across centered variants before launching full campaigns.
- [x] **TRI-04**: Developer can see a pre-full-run go/no-go memo that lists fixed blockers, accepted exclusions, and remaining risks.

### Centered Integration Fixes

- [x] **FIX-01**: Centered warm-start paths either run verified training attempts for supported formulas or emit explicit fail-closed unsupported reasons that remain in the denominator.
- [x] **FIX-02**: Compiler-seed and exact-AST embedding paths preserve operator-family metadata and never silently treat raw EML seeds as centered-family exact returns.
- [x] **FIX-03**: Centered blind initializers and scaffold choices are compatible with `CEML_s` and `ZEML_s`, or are explicitly excluded with reason codes in manifests.
- [x] **FIX-04**: Scheduled continuation changes operator families during training according to the declared schedule and records the schedule in artifacts.
- [x] **FIX-05**: Repair, refit, and snap-neighborhood paths preserve operator-family semantics and do not compare incompatible raw and centered ASTs as same-family exact returns.

### Experiment Matrix Calibration

- [x] **MAT-01**: Built-in family suites cover raw EML plus fixed `CEML_s` and `ZEML_s` variants for `s in {1, 2, 4, 8}` where the run type is supported.
- [x] **MAT-02**: Built-in family suites include continuation schedules at least for `8 -> 4` and `8 -> 4 -> 2 -> 1` where budgets and support gates allow.
- [x] **MAT-03**: Campaign presets separate calibration, shallow pure-blind, scaffolded shallow, perturbed basin, depth-curve, standard, and optional showcase evidence.
- [x] **MAT-04**: Run IDs, filters, manifests, and tables identify formula, start mode, training mode, depth, seed, operator family, and operator schedule.
- [x] **MAT-05**: Calibration artifacts record chosen budgets, supported variants, and exclusions before full family campaigns run.

### Full Evidence Execution and Artifacts

- [x] **RUN-01**: Full `family-shallow-pure-blind` evidence is run or deliberately scoped with a reproducible reason and artifact trail.
- [x] **RUN-02**: Full `family-shallow`, `family-basin`, and `family-depth-curve` evidence is run or deliberately scoped with reproducible reasons and artifact trails.
- [x] **RUN-03**: `family-standard` evidence is run after calibration, while `family-showcase` is run only if earlier campaigns show a meaningful centered-family signal.
- [x] **RUN-04**: Campaign outputs include operator-family recovery, depth behavior, anomaly rates, shifted-singularity diagnostics, repair/refit usage, post-snap verifier pass rate, unsupported rates, and formula-complexity overhead.
- [x] **RUN-05**: Regression-lock artifacts compare raw and centered families without overwriting archived v1.4, v1.5, v1.6, or v1.7 anchors.

### Paper Decision and Claim Boundary

- [x] **PAP-01**: The paper decision package is regenerated under `artifacts/paper/v1.8/` from the new centered-family aggregates.
- [x] **PAP-02**: The decision memo chooses one of: publish centered robustness/geometry paper, publish raw-EML searchability note, continue toward constructive completeness search, or abandon/pivot centered-family work.
- [x] **PAP-03**: Safe and unsafe claim artifacts cite the actual v1.8 aggregate paths and keep pure blind, scaffolded, warm-start, compile-only, repaired, and perturbed-basin regimes separate.
- [x] **PAP-04**: If centered variants do not improve the declared evidence criteria, the artifacts say so directly and do not frame unsupported or scaffolded paths as blind centered discovery.
- [x] **PAP-05**: The v1.8 milestone audit verifies requirement coverage, evidence integrity, and absence of centered-family overclaims.

## Future Requirements

Deferred to later milestones.

### Completeness and External Baselines

- **COMP-01**: Researcher can search for constructive `CEML_s` interdefinability or successor-family witnesses for selected `s` values.
- **COMP-02**: Researcher can compare against matched-budget external symbolic-regression baselines after the internal centered-family evidence is stable.
- **COMP-03**: Researcher can run larger campaign matrices on accelerated hardware after local budget and artifact contracts are proven.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Proving `CEML_s` completeness | This milestone is about viability and evidence; constructive completeness search is a separate research track. |
| Guaranteeing centered-family superiority | The milestone must measure whether centered variants help, not assume the answer. |
| Treating unsupported centered runs as failures to hide missing implementation | Unsupported paths must remain explicit with reason codes and denominator accounting. |
| Running expensive showcase campaigns before calibration | Showcase runs are only useful if shallow, basin, or depth-curve evidence shows a signal. |
| Overwriting archived proof/campaign anchors | Historical v1.4-v1.7 artifacts remain comparison anchors. |
| Matched external baseline paper claims | External comparisons are deferred until the centered/raw internal decision is evidence-backed. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| TRI-01 | Phase 44 | Complete |
| TRI-02 | Phase 44 | Complete |
| TRI-03 | Phase 44 | Complete |
| TRI-04 | Phase 44 | Complete |
| FIX-01 | Phase 45 | Complete |
| FIX-02 | Phase 45 | Complete |
| FIX-03 | Phase 45 | Complete |
| FIX-04 | Phase 45 | Complete |
| FIX-05 | Phase 45 | Complete |
| MAT-01 | Phase 46 | Complete |
| MAT-02 | Phase 46 | Complete |
| MAT-03 | Phase 46 | Complete |
| MAT-04 | Phase 46 | Complete |
| MAT-05 | Phase 46 | Complete |
| RUN-01 | Phase 47 | Complete |
| RUN-02 | Phase 47 | Complete |
| RUN-03 | Phase 47 | Complete |
| RUN-04 | Phase 47 | Complete |
| RUN-05 | Phase 47 | Complete |
| PAP-01 | Phase 48 | Complete |
| PAP-02 | Phase 48 | Complete |
| PAP-03 | Phase 48 | Complete |
| PAP-04 | Phase 48 | Complete |
| PAP-05 | Phase 48 | Complete |

**Coverage:**
- v1.8 requirements: 24 total
- Mapped to phases: 24
- Unmapped: 0

---
*Requirements defined: 2026-04-16*
*Last updated: 2026-04-17 after completing v1.8*
