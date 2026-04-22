# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-22
**Current milestone:** v1.17 Snap-First Exact Recovery and Candidate Neighborhood Search
**Phase numbering:** Continuing from v1.16 Phase 93.

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
- **v1.16 Paper-Strength GEML Recovery Evidence** - Phases 88-93 complete (completed 2026-04-22; archives: `.planning/milestones/v1.16-ROADMAP.md`, `.planning/milestones/v1.16-REQUIREMENTS.md`, `.planning/milestones/v1.16-MILESTONE-AUDIT.md`, `.planning/milestones/v1.16-phases/`)
- **v1.17 Snap-First Exact Recovery and Candidate Neighborhood Search** - Phases 94-98 active

## Current Status

v1.17 starts from the v1.16 final decision: `artifacts/paper/v1.16-geml/` is source-locked, claim-audited, and inconclusive. The pilot evidence has 12 paired rows across 2 unique seeds, 0 raw exact recoveries, 0 i*pi exact recoveries, and 12 loss-only outcomes. The full matched campaign was blocked fail-closed.

The next bottleneck is the hard candidate boundary. Before spending more compute on broad raw/i*pi campaigns, v1.17 will inspect snap margins, generate bounded exact-tree neighborhoods around near-miss snapped candidates, rank candidates by verifier status first, and run a tiny natural-bias recovery sandbox.

## Phase Status

- [x] Phase 94: Snap-Mismatch Diagnostics and Low-Margin Inventory (completed 2026-04-22)
- [x] Phase 95: Bounded Exact Neighborhood Generator (completed 2026-04-22)
- [x] Phase 96: Verifier-First Candidate Ranking and Promotion (completed 2026-04-22)
- [ ] Phase 97: Focused v1.17 Natural-Bias Recovery Sandbox
- [ ] Phase 98: v1.17 Evidence Package and Next-Campaign Gate

## Phase Overview

| Phase | Name | Goal | Requirements |
|-------|------|------|--------------|
| 94 | 1/1 | Complete    | 2026-04-22 |
| 95 | 1/1 | Complete    | 2026-04-22 |
| 96 | 1/1 | Complete    | 2026-04-22 |
| 97 | Focused v1.17 Natural-Bias Recovery Sandbox | Test whether snap-neighborhood search produces any exact signal on selected natural-bias targets and controls. | EVID-01, EVID-02, EVID-03 |
| 98 | v1.17 Evidence Package and Next-Campaign Gate | Package the result and decide whether broader campaigns are justified. | PACK-01, PACK-02, PACK-03 |

## Phase Details

### Phase 94: Snap-Mismatch Diagnostics and Low-Margin Inventory

**Goal:** Add the diagnostic layer needed to understand why v1.16 soft/loss-only candidates fail after snapping.

**Requirements:** SNAP-01, SNAP-02, SNAP-03

**Success criteria:**

1. Campaign rows expose per-slot probabilities, margins, selected alternatives, and low-confidence alternatives for selected/fallback/loss-only candidates.
2. Snap mismatch rows are classified by low-margin slots, active-node changes, soft-versus-hard error deltas, and branch/fidelity diagnostics.
3. Deterministic manifests identify the v1.16 failed/loss-only rows that should seed neighborhood search.
4. Regression tests cover raw EML and i*pi EML diagnostic emission without changing verifier recovery definitions.

### Phase 95: Bounded Exact Neighborhood Generator

**Goal:** Generate local exact-tree alternatives around snapped candidates while preserving target-agnostic behavior.

**Requirements:** NBR-01, NBR-03, NBR-04

**Success criteria:**

1. One-slot and two-slot alternatives are generated deterministically from low-margin candidate choices.
2. Candidate budgets, ordering, and pruning are source-locked and reproducible.
3. Original snapped candidates and fallback candidates remain present with provenance.
4. Tests reject formula-name recognizers, exact target-tree seeds, and hidden oracle promotion paths.

### Phase 96: Verifier-First Candidate Ranking and Promotion

**Goal:** Make exact verifier status the first-class promotion rule for all candidate pools.

**Requirements:** NBR-02, RANK-01, RANK-02, RANK-03

**Success criteria:**

1. Every neighborhood candidate is checked through the same verifier gates before promotion.
2. Ranking explains why the winner was selected and why lower-loss candidates failed.
3. Tables separate exact recovery, verified equivalence, repair-only, loss-only, compile-only, same-AST, fallback, and original-snap outcomes.
4. Existing recovery-accounting tests remain compatible with the new ranking fields.

### Phase 97: Focused v1.17 Natural-Bias Recovery Sandbox

**Goal:** Run the smallest useful matched experiment to see whether the snap-first workflow produces exact recovery signal.

**Requirements:** EVID-01, EVID-02, EVID-03

**Success criteria:**

1. Selected v1.16 natural-bias rows are rerun with snap-neighborhood search enabled.
2. Raw EML and i*pi EML use matched budgets, depth, splits, verifier gates, and negative controls.
3. The sandbox records whether at least one verifier-gated exact recovery appears.
4. The gate blocks broader pilot/full campaigns if exact signal remains absent.

### Phase 98: v1.17 Evidence Package and Next-Campaign Gate

**Goal:** Assemble the source-locked v1.17 answer and decide what work is justified next.

**Requirements:** PACK-01, PACK-02, PACK-03

**Success criteria:**

1. Package includes manifests, before/after tables, source locks, failure taxonomy, reproduction commands, and claim audit.
2. Final decision is `exact_signal_found`, `still_inconclusive`, or `negative` under the predefined gate.
3. The v1.16 package remains intact and any comparison is explicitly additive.
4. The package states whether broader i*pi/GEML paper campaigns are justified or still blocked.

## Dependency Notes

- Phase 94 comes first because neighborhood search needs actual low-margin and snap-mismatch evidence.
- Phase 95 depends on Phase 94's deterministic candidate inventories.
- Phase 96 depends on Phase 95's candidate generation and preserves verifier-owned claims.
- Phase 97 depends on Phase 96 so the smoke campaign can use the full ranking path.
- Phase 98 is last because it audits the result and decides whether a larger campaign is justified.

## Requirements Traceability

| Requirement Group | Covered By |
|-------------------|------------|
| SNAP-01..SNAP-03 | Phase 94 |
| NBR-01, NBR-03, NBR-04 | Phase 95 |
| NBR-02, RANK-01..RANK-03 | Phase 96 |
| EVID-01..EVID-03 | Phase 97 |
| PACK-01..PACK-03 | Phase 98 |

## Notes

- No new external domain research was run during initialization; v1.17 is scoped from the v1.16 final package and current project evidence.
- Larger matched raw/i*pi campaigns remain blocked until the tiny v1.17 sandbox produces verifier-gated exact signal.
- Loss-only improvements remain diagnostics. The recovery definition remains exact-candidate and verifier-owned.
- A still-inconclusive or negative v1.17 result is acceptable if it cleanly identifies the blocker and preserves the claim boundary.

---
*Roadmap created for v1.17 on 2026-04-22*
