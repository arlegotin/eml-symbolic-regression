# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-21
**Current milestone:** v1.14 Evidence claim integrity and audit hardening
**Phase numbering:** Continuing from v1.13 Phase 76.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)
- **v1.5 Training Proof and Recovery Guarantees** - Phases 29-33 complete (completed 2026-04-16; archive: `.planning/milestones/v1.5-ROADMAP.md`)
- **v1.6 Hybrid Search Pipeline and Exact Candidate Recovery** - Phases 34-38 complete (completed 2026-04-16; archive: `.planning/milestones/v1.6-ROADMAP.md`)
- **v1.7 Centered-Family Baseline and Paper Decision** - Phases 39-43 complete (completed 2026-04-16; archive: `.planning/milestones/v1.7-ROADMAP.md`)
- **v1.8 Centered-Family Viability and Full Evidence Run** - Phases 44-48 complete (completed 2026-04-17; archive: `.planning/milestones/v1.8-ROADMAP.md`)
- **v1.9 Raw-EML Hybrid Recovery and Paper Suite** - Phases 49-53 complete (completed 2026-04-17; archive: `.planning/milestones/v1.9-ROADMAP.md`)
- **v1.10 Search-backed motif library and compiler shortening for logistic and Planck** - Phases 54-58 complete (completed 2026-04-18; archive: `.planning/milestones/v1.10-ROADMAP.md`)
- **v1.11 Paper-strength evidence and figure package** - Phases 59-63 complete (completed 2026-04-19; archive: `.planning/milestones/v1.11-ROADMAP.md`)
- **v1.12 Paper draft skeleton and refreshed shallow evidence** - Phases 64-68 complete (completed 2026-04-19; archive: `.planning/milestones/v1.12-ROADMAP.md`)
- **v1.13 Publication-grade reproduction and validation** - Phases 69-76 complete (completed 2026-04-20; archives: `.planning/milestones/v1.13-ROADMAP.md`, `.planning/milestones/v1.13-REQUIREMENTS.md`, `.planning/milestones/v1.13-MILESTONE-AUDIT.md`, `.planning/milestones/v1.13-phases/`)

## Current Status

v1.14 is open. It repairs a post-v1.13 claim-integrity audit finding: compile-only verified support must not count as trained recovery. The same milestone tightens warm-start evidence labels, quarantines weak baseline rows from the main claim surface, fixes a latent multivariate verifier target-matching bug, and regenerates the public evidence package from the corrected contracts.

## Phase Status

- [ ] Phase 77: Two-Axis Recovery Accounting and Headline Rebuild
- [ ] Phase 78: Warm-Start Evidence Relabeling
- [ ] Phase 79: Baseline Claim Surface Quarantine
- [ ] Phase 80: Multivariate Verifier Target Matching
- [ ] Phase 81: Corrected Evidence Rebuild and Claim Audit

## Phase Overview

| Phase | Name | Goal | Requirements |
|-------|------|------|--------------|
| 77 | Two-Axis Recovery Accounting and Headline Rebuild | Separate verification from discovery regime and make compile-only support impossible to count as trained recovery. | REC-01, REC-02, REC-03, REC-04 |
| 78 | Warm-Start Evidence Relabeling | Reframe zero-perturbation same-AST warm-start rows as exact seed round-trips unless robustness evidence exists. | WARM-01, WARM-02, WARM-03, WARM-04 |
| 79 | Baseline Claim Surface Quarantine | Keep unavailable, unsupported, and denominator-excluded baseline rows out of main comparison claims. | BASE-01, BASE-02, BASE-03, BASE-04 |
| 80 | Multivariate Verifier Target Matching | Fix high-precision target lookup for multivariate splits without changing univariate verifier behavior. | VER-01, VER-02, VER-03, VER-04 |
| 81 | Corrected Evidence Rebuild and Claim Audit | Regenerate the publication package, README/report surfaces, and release checks from the corrected contracts. | PUB-01, PUB-02, PUB-03, PUB-04 |

## Phase Details

### Phase 77: Two-Axis Recovery Accounting and Headline Rebuild

**Goal:** Evidence rows carry separate verification and discovery labels, and compile-only support cannot inflate trained recovery counts.

**Requirements:** REC-01, REC-02, REC-03, REC-04

**Success criteria:**
1. Run-level and aggregate artifacts expose separate `verification_outcome` and `evidence_regime` or `discovery_class` fields.
2. `start_mode=compile` rows are classified as compile-only verified support when appropriate, never trained recovery.
3. Headline package numbers become 8 trained exact recoveries, 1 compile-only verified support row, 15 unsupported rows, and 0 failed rows.
4. Claim audit and regression tests fail if compile-only rows contribute to trained recovery numerator or headline copy.

### Phase 78: Warm-Start Evidence Relabeling

**Goal:** Publication-track warm starts are labeled by the evidence they actually provide.

**Requirements:** WARM-01, WARM-02, WARM-03, WARM-04

**Success criteria:**
1. Existing zero-perturbation same-AST publication rows are labeled exact seed round-trip or same-AST retention.
2. Warm-start tables surface perturbation noise, warm steps, warm restarts, total restarts, return kind, and AST-return status.
3. Robustness or basin language is absent unless backed by nonzero perturbation, multiple seeds, and more than one optimization step.
4. README, reports, aggregates, and paper-facing text use the new wording consistently.

### Phase 79: Baseline Claim Surface Quarantine

**Goal:** Baseline scaffolding remains useful internally without carrying unsupported public comparison weight.

**Requirements:** BASE-01, BASE-02, BASE-03, BASE-04

**Success criteria:**
1. Main README/report/paper surfaces no longer cite unavailable or unsupported baseline rows as comparison evidence.
2. Baseline artifacts show dependency status, denominator policy, unsupported reasons, and whether an adapter actually launched.
3. Missing external dependencies are reported as scaffolding or future work, not contextual comparison.
4. Claim audit blocks main-surface baseline comparison copy unless fixed-budget external rows completed on the same targets and splits.

### Phase 80: Multivariate Verifier Target Matching

**Goal:** High-precision verifier target lookup is correct for multivariate data.

**Requirements:** VER-01, VER-02, VER-03, VER-04

**Success criteria:**
1. Multivariate splits without `target_mpmath` no longer match scalar targets using only the first input variable.
2. The verifier either requires `target_mpmath` for multivariate high-precision checks or uses a stable full-row key.
3. Tests cover repeated first-coordinate rows with different remaining coordinates and target values.
4. Existing univariate verifier tests and behavior remain unchanged.

### Phase 81: Corrected Evidence Rebuild and Claim Audit

**Goal:** All public package artifacts reflect the corrected accounting, labels, baseline framing, and verifier behavior.

**Requirements:** PUB-01, PUB-02, PUB-03, PUB-04

**Success criteria:**
1. The publication evidence package is regenerated from source commands after Phases 77-80 land.
2. README, campaign report, aggregate JSON/Markdown, claim-audit outputs, and paper-facing tables contain no stale 9-row recovered headline.
3. CI or release-gate checks lock the corrected schema, corrected headline counts, and compile-only exclusion.
4. Historical v1.13 artifacts remain inspectable, while corrected artifacts have source locks and regeneration commands.

## Dependency Notes

- Phase 77 comes first because later wording, tables, and claim-audit gates depend on the corrected status model.
- Phase 78 should follow Phase 77 so warm-start rows use the same discovery-regime vocabulary.
- Phase 79 can run after Phase 77 and before the final rebuild because baseline wording affects public claim surfaces but not verifier mechanics.
- Phase 80 can run independently of narrative cleanup, but must finish before Phase 81 so the regenerated package carries the verifier bug fix.
- Phase 81 is last and verifies the milestone end to end.

## Notes

- v1.14 intentionally chooses relabeling/quarantine over large new experiments. A real perturbation grid and real external baseline runs are tracked as future requirements.
- Work remains on `dev`; public `main` publication still requires the validated release workflow after corrected evidence passes.

---
*Roadmap created for v1.14 on 2026-04-21*
