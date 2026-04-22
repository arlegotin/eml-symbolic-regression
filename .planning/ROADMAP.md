# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-22
**Current milestone:** v1.16 Paper-Strength GEML Recovery Evidence
**Phase numbering:** Continuing from v1.15 Phase 87.

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
- **v1.14 Evidence claim integrity and audit hardening** - Phases 77-81 complete (completed 2026-04-21; archives: `.planning/milestones/v1.14-ROADMAP.md`, `.planning/milestones/v1.14-REQUIREMENTS.md`, `.planning/milestones/v1.14-phases/`)
- **v1.15 GEML family and i*pi EML exploration** - Phases 82-87 complete (completed 2026-04-22; archives: `.planning/milestones/v1.15-ROADMAP.md`, `.planning/milestones/v1.15-REQUIREMENTS.md`, `.planning/milestones/v1.15-MILESTONE-AUDIT.md`, `.planning/milestones/v1.15-phases/`)
- **v1.16 Paper-Strength GEML Recovery Evidence** - Phases 88-93 active

## Current Status

v1.16 is active. It starts from the v1.15 result: `artifacts/paper/v1.15-geml/` is claim-safe but inconclusive because the checked-in smoke campaign has two paired rows, no verifier-gated exact recovery, one periodic i*pi loss-only signal, and one negative-control raw loss-only signal.

The v1.16 objective is intentionally evidence-gated. The milestone should produce a strong i*pi/GEML paper section only if exact verifier-gated recovery improves under a matched raw/i*pi protocol. If that does not happen, the milestone still succeeds by producing a source-locked negative or inconclusive package with ablations, failure taxonomy, and clear next-step diagnostics.

## Phase Status

- [ ] Phase 88: Paper-Strength Success Gate and Campaign Contract
- [ ] Phase 89: i*pi-Aware Search and Branch-Safe Initialization
- [ ] Phase 90: Budget Ladder and Pilot Recovery Runs
- [ ] Phase 91: Full Matched GEML Paper Campaign
- [ ] Phase 92: Ablations, Failure Taxonomy, and Paper Figures
- [ ] Phase 93: v1.16 Paper Decision Package and Claim Audit

## Phase Overview

| Phase | Name | Goal | Requirements |
|-------|------|------|--------------|
| 88 | Paper-Strength Success Gate and Campaign Contract | Define the exact evidence gate for a paper-positive i*pi/GEML result and lock matched campaign denominators before optimizer changes. | STRG-01, STRG-02, STRG-03, STRG-04, CAMP-04 |
| 89 | i*pi-Aware Search and Branch-Safe Initialization | Improve i*pi/GEML search enough to produce exact candidates on natural targets without exact formula leakage. | SRCH-01, SRCH-02, SRCH-03, SRCH-04, SRCH-05 |
| 90 | Budget Ladder and Pilot Recovery Runs | Run cheap smoke and pilot campaigns to decide whether search improvements merit the full paper campaign. | SRCH-04, CAMP-02, CAMP-03, CAMP-04, ABL-01, ABL-03 |
| 91 | Full Matched GEML Paper Campaign | Produce the full matched multi-seed raw EML versus i*pi EML evidence set if pilot gates pass; otherwise produce locked negative evidence. | CAMP-01, CAMP-02, CAMP-03, CAMP-04, ABL-02 |
| 92 | Ablations, Failure Taxonomy, and Paper Figures | Explain why the result is strong or not strong enough, with ablations and reviewer-facing visuals. | ABL-01, ABL-02, ABL-03, ABL-04, PAPER-01 |
| 93 | v1.16 Paper Decision Package and Claim Audit | Assemble final paper-strength evidence package and decide whether i*pi/GEML deserves a positive paper section. | STRG-04, PAPER-02, PAPER-03, PAPER-04 |

## Phase Details

### Phase 88: Paper-Strength Success Gate and Campaign Contract

**Goal:** Define the exact evidence gate for a paper-positive i*pi/GEML result and lock matched campaign denominators before optimizer changes.

**Requirements:** STRG-01, STRG-02, STRG-03, STRG-04, CAMP-04

**Success criteria:**

1. Machine-readable gate config defines `paper_positive`, `promising_preliminary`, `negative`, and `inconclusive` outcomes.
2. Claim audit rejects loss-only recovery, same-AST seed promotion, formula leakage, and negative-control cherry-picking.
3. Campaign contract locks target families, seeds, budgets, depths, splits, verifier gates, branch metrics, and resource metadata.
4. The package can fail closed when the exact-recovery gate is not met.

### Phase 89: i*pi-Aware Search and Branch-Safe Initialization

**Goal:** Improve i*pi/GEML search enough to produce exact candidates on natural targets without exact formula leakage.

**Requirements:** SRCH-01, SRCH-02, SRCH-03, SRCH-04, SRCH-05

**Success criteria:**

1. Periodic, phase-log, or related initializers/priors are generic to target families and not formula-name exact seeds.
2. Optimizer schedules, candidate pooling, and hardening changes preserve verifier-owned exact-candidate selection.
3. Branch guard metrics are surfaced while faithful verification semantics remain unchanged.
4. Raw EML regression tests and recovery-accounting tests still pass.

### Phase 90: Budget Ladder and Pilot Recovery Runs

**Goal:** Run cheap smoke and pilot campaigns to decide whether search improvements merit the full paper campaign.

**Requirements:** SRCH-04, CAMP-02, CAMP-03, CAMP-04, ABL-01, ABL-03

**Success criteria:**

1. Smoke and pilot outputs compare raw EML versus i*pi EML by target family and seed.
2. Pilot gate prevents an expensive full run if no exact-recovery signal appears.
3. Failure taxonomy identifies optimization miss, snap mismatch, branch pathology, verifier mismatch, unsupported/over-depth, and numerical instability.
4. Reproducible commands and source locks are written for every pilot run.

### Phase 91: Full Matched GEML Paper Campaign

**Goal:** Produce the full matched multi-seed raw EML versus i*pi EML evidence set if pilot gates pass; otherwise produce locked negative evidence.

**Requirements:** CAMP-01, CAMP-02, CAMP-03, CAMP-04, ABL-02

**Success criteria:**

1. A full paper campaign or fail-closed negative package exists.
2. Aggregates include exact recovery, loss, branch diagnostics, runtime/resource metadata, and seed-level variation.
3. Loss-only, repaired, compile-only, and same-AST rows cannot contaminate trained exact-recovery denominators.
4. Results are grouped by natural-bias families and negative controls.

### Phase 92: Ablations, Failure Taxonomy, and Paper Figures

**Goal:** Explain why the result is strong or not strong enough, with ablations and reviewer-facing visuals.

**Requirements:** ABL-01, ABL-02, ABL-03, ABL-04, PAPER-01

**Success criteria:**

1. Ablation tables show the contribution of initialization, branch guards, constants, depth, budget, and candidate pooling.
2. Failure taxonomy is source-locked and maps failures to representative examples.
3. Figures and tables are generated deterministically from campaign data.
4. Representative curves show verified fits and failures honestly.

### Phase 93: v1.16 Paper Decision Package and Claim Audit

**Goal:** Assemble final paper-strength evidence package and decide whether i*pi/GEML deserves a positive paper section.

**Requirements:** STRG-04, PAPER-02, PAPER-03, PAPER-04

**Success criteria:**

1. Package includes manifests, source locks, campaign tables, ablation tables, figure metadata, and reproduction commands.
2. Claim audit blocks global superiority, broad blind-recovery, full universality, loss-only recovery, and negative-control cherry-picking.
3. Final decision is `paper_positive`, `promising_preliminary`, `negative`, or `inconclusive` under the Phase 88 gate.
4. README or paper-draft guidance is updated to match the decision.

## Dependency Notes

- Phase 88 comes first because it defines the evidence standard before any optimizer work can move the goalposts.
- Phase 89 depends on Phase 88's leakage and accounting rules.
- Phase 90 depends on Phase 89 and protects local time by requiring exact-recovery signal before full campaigns.
- Phase 91 depends on Phase 90's pilot gate; if the gate fails, Phase 91 should produce a locked negative package rather than a full expensive run.
- Phase 92 depends on pilot/full campaign outputs.
- Phase 93 is last because it audits claims against the predefined gate.

## Requirements Traceability

| Requirement Group | Covered By |
|-------------------|------------|
| STRG-01..STRG-04 | Phases 88, 93 |
| SRCH-01..SRCH-05 | Phases 89, 90 |
| CAMP-01..CAMP-04 | Phases 88, 90, 91 |
| ABL-01..ABL-04 | Phases 90, 91, 92 |
| PAPER-01..PAPER-04 | Phases 92, 93 |

## Notes

- No new external domain research was run during initialization; v1.16 is scoped from the v1.15 audit and current project evidence.
- The milestone optimizes for strong paper results, but the recovery definition remains verifier-owned and exact-candidate based.
- Full campaigns should not launch blindly. The milestone uses a smoke/pilot/full ladder because v1.15 already showed that loss-only signals are not enough.
- A negative or inconclusive v1.16 result is acceptable only if it is source-locked, reproducible, and explains the blocker clearly enough to guide the next paper strategy.

---
*Roadmap created for v1.16 on 2026-04-22*
