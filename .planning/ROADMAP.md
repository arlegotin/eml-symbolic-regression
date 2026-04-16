# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-16
**Current milestone:** v1.8 Centered-Family Viability and Full Evidence Run
**Phase numbering:** Continues from v1.7; v1.8 starts at Phase 44.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)
- **v1.5 Training Proof and Recovery Guarantees** - Phases 29-33 complete (completed 2026-04-16; archive: `.planning/milestones/v1.5-ROADMAP.md`)
- **v1.6 Hybrid Search Pipeline and Exact Candidate Recovery** - Phases 34-38 complete (completed 2026-04-16; archive: `.planning/milestones/v1.6-ROADMAP.md`)
- **v1.7 Centered-Family Baseline and Paper Decision** - Phases 39-43 complete (completed 2026-04-16; archive: `.planning/milestones/v1.7-ROADMAP.md`)
- **v1.8 Centered-Family Viability and Full Evidence Run** - Phases 44-48 planned

## Milestone Goal

Determine whether centered/scaled operator families are actually viable improvements over raw EML after fixing missing integration support, calibrating the family grid, running full evidence campaigns, and regenerating the paper decision artifacts.

## Planned Phases

| Phase | Name | Goal | Requirements | Status |
|-------|------|------|--------------|--------|
| 44 | Centered-Family Smoke Triage and Full-Run Gate | Turn the quick smoke failure signal into an artifact-backed blocker map and go/no-go gate for expensive campaigns. | TRI-01, TRI-02, TRI-03, TRI-04 | Pending |
| 45 | Centered Integration Fixes | Fix or explicitly gate centered warm-start, compiler-seed, initializer, schedule, repair, and refit paths. | FIX-01, FIX-02, FIX-03, FIX-04, FIX-05 | Pending |
| 46 | Family Matrix Calibration | Expand and calibrate the fixed-`s` and continuation experiment matrix before full evidence runs. | MAT-01, MAT-02, MAT-03, MAT-04, MAT-05 | Pending |
| 47 | Full Family Evidence Campaigns | Run and archive the raw-vs-centered family evidence campaigns with comparison artifacts and locks. | RUN-01, RUN-02, RUN-03, RUN-04, RUN-05 | Pending |
| 48 | Paper Decision Refresh and Milestone Audit | Regenerate the paper decision package from v1.8 aggregates and audit the claim boundary. | PAP-01, PAP-02, PAP-03, PAP-04, PAP-05 | Pending |

## Phase Details

### Phase 44: Centered-Family Smoke Triage and Full-Run Gate

**Goal:** Convert the observed `family-smoke` result into a reproducible blocker analysis and full-run gate.

**Why first:** The quick smoke check showed centered blind `exp` failures and unsupported centered warm-start paths. Running full campaigns before classifying these would mostly spend time producing known low-information failures.

**Success criteria:**
1. A reproducible smoke command and artifact path are documented for raw-vs-centered comparison.
2. Every centered smoke failure and unsupported path is classified with an artifact-backed reason.
3. Focused `exp`/`log` shallow calibration probes are available for the centered variants that matter.
4. A go/no-go memo states what must be fixed, what can remain fail-closed, and what evidence can be trusted in the next phases.

**Requirements:** TRI-01, TRI-02, TRI-03, TRI-04

### Phase 45: Centered Integration Fixes

**Goal:** Make centered-family training paths real where needed and explicitly fail-closed where not supported.

**Why now:** The family matrix must distinguish genuine centered operator behavior from missing warm-start, initializer, embedding, continuation, repair, or refit support.

**Success criteria:**
1. Centered warm-start either executes supported verified attempts or emits explicit unsupported reasons that stay in denominators.
2. Compiler-seed and exact-AST embedding paths preserve operator-family metadata and reject incompatible exact-return comparisons.
3. Centered scaffold and initializer choices are compatible or excluded with visible reason codes.
4. Continuation schedules switch operators as declared and record schedule state in manifests.
5. Repair/refit/neighborhood logic preserves family semantics under regression tests.

**Requirements:** FIX-01, FIX-02, FIX-03, FIX-04, FIX-05

### Phase 46: Family Matrix Calibration

**Goal:** Build the defensible experiment grid and calibration artifacts for fixed centered families and continuation schedules.

**Why now:** The v1.7 grid was intentionally small. The paper-relevant comparison needs fixed `s` variants, scheduled variants, clear filters, and budget/exclusion records.

**Success criteria:**
1. Built-in family suites cover raw EML, `CEML_1/2/4/8`, `ZEML_1/2/4/8`, and declared continuation schedules where supported.
2. Campaign presets separate calibration, shallow pure-blind, scaffolded shallow, basin, depth-curve, standard, and optional showcase evidence.
3. Run IDs, manifests, filters, and tables expose formula, start mode, training mode, depth, seed, operator family, and schedule.
4. Calibration outputs record chosen budgets, exclusions, and recommended full-run scope.

**Requirements:** MAT-01, MAT-02, MAT-03, MAT-04, MAT-05

### Phase 47: Full Family Evidence Campaigns

**Goal:** Execute and archive the full raw-vs-centered evidence matrix needed to answer centered-family viability.

**Why now:** After triage, fixes, and calibration, full campaigns can produce evidence rather than restating known missing support.

**Success criteria:**
1. `family-shallow-pure-blind` is run or deliberately scoped with a reproducible reason and artifact trail.
2. `family-shallow`, `family-basin`, and `family-depth-curve` are run or deliberately scoped with reproducible reasons and artifact trails.
3. `family-standard` is run after calibration; `family-showcase` runs only if earlier evidence shows a meaningful centered-family signal.
4. Campaign reports include recovery, depth, anomaly, shifted-singularity, repair/refit, post-snap verifier, unsupported, and formula-complexity comparisons.
5. Regression-lock artifacts compare centered and raw families while preserving archived historical anchors.

**Requirements:** RUN-01, RUN-02, RUN-03, RUN-04, RUN-05

### Phase 48: Paper Decision Refresh and Milestone Audit

**Goal:** Regenerate the paper decision package from v1.8 evidence and close the milestone with an explicit claim boundary.

**Why last:** Paper claims must follow the actual v1.8 aggregates, not the original centered-family hypothesis.

**Success criteria:**
1. `artifacts/paper/v1.8/` is generated from the new centered-family aggregates.
2. The decision memo chooses publish centered geometry paper, publish raw-EML searchability note, continue completeness search, or abandon/pivot centered-family work.
3. Safe/unsafe claim artifacts cite actual aggregate paths and preserve regime separation.
4. Negative centered results, if present, are reported directly rather than reframed as success.
5. The milestone audit verifies requirement coverage, evidence integrity, and absence of centered-family overclaims.

**Requirements:** PAP-01, PAP-02, PAP-03, PAP-04, PAP-05

## Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| TRI-01 | Phase 44 | Pending |
| TRI-02 | Phase 44 | Pending |
| TRI-03 | Phase 44 | Pending |
| TRI-04 | Phase 44 | Pending |
| FIX-01 | Phase 45 | Pending |
| FIX-02 | Phase 45 | Pending |
| FIX-03 | Phase 45 | Pending |
| FIX-04 | Phase 45 | Pending |
| FIX-05 | Phase 45 | Pending |
| MAT-01 | Phase 46 | Pending |
| MAT-02 | Phase 46 | Pending |
| MAT-03 | Phase 46 | Pending |
| MAT-04 | Phase 46 | Pending |
| MAT-05 | Phase 46 | Pending |
| RUN-01 | Phase 47 | Pending |
| RUN-02 | Phase 47 | Pending |
| RUN-03 | Phase 47 | Pending |
| RUN-04 | Phase 47 | Pending |
| RUN-05 | Phase 47 | Pending |
| PAP-01 | Phase 48 | Pending |
| PAP-02 | Phase 48 | Pending |
| PAP-03 | Phase 48 | Pending |
| PAP-04 | Phase 48 | Pending |
| PAP-05 | Phase 48 | Pending |

**Coverage summary:**
- v1.8 requirements: 24 total
- Mapped to phases: 24
- Unmapped: 0

## Next Step

Start Phase 44 with:

```bash
$gsd-plan-phase 44
```

---
*Roadmap created: 2026-04-16 for milestone v1.8*
