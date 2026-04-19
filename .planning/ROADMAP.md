# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-19  
**Current milestone:** v1.11 Paper-strength evidence and figure package  
**Phase numbering:** Continuing from v1.10 Phase 58.

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
- **v1.11 Paper-strength evidence and figure package** - Phases 59-63 active

## Current Status

v1.11 has started. The milestone will produce a paper-ready evidence package by refreshing stale scientific-law paper rows, running real claim-safe training, adding low-hanging ablations and baseline diagnostics, generating plot-ready assets, and auditing all claims against source artifacts.

## Active Phases

### Phase 59: Evidence Contracts and Source Locks

**Goal:** Define the v1.11 evidence contract before running new campaigns.

**Scope:**
- Create package source inventory and output-root contract for `artifacts/paper/v1.11/`.
- Define claim ledger fields, evidence classes, denominator rules, figure/table schemas, and source-lock requirements.
- Add v1.11 smoke/package tests that prevent stale logistic/Planck table rows and mixed-regime recovery claims.

**Requirements:** PAPER-01, PAPER-02, PAPER-03, CLAIM-01, CLAIM-03

**Success criteria:**
- v1.11 package inputs and outputs are specified in code or test fixtures.
- Logistic and Planck source rows are required to come from v1.10 focused artifacts.
- The paper package cannot compute recovery from loss-only fields.

### Phase 60: Claim-Safe Training Campaigns

**Goal:** Run real current-code training in bounded regimes that can be honestly reported.

**Scope:**
- Add or reuse v1.11 suites for shallow pure-blind, scaffolded, warm-start/same-AST, perturbed-basin, and logistic/Planck probes.
- Execute the suites and commit focused artifacts under `artifacts/campaigns/v1.11-*`.
- Record commands, budgets, seeds, start modes, verifier status, and failure classes.

**Requirements:** TRAIN-01, TRAIN-02, TRAIN-03, CLAIM-01

**Success criteria:**
- New v1.11 campaign artifacts include real training runs, not only compile diagnostics.
- Unsupported logistic and Planck probes are reported honestly unless full strict/verifier support passes.
- Aggregates expose enough lifecycle fields for later figures.

### Phase 61: Ablation and Baseline Diagnostics

**Goal:** Add low-hanging diagnostics that explain which hybrid pieces matter.

**Scope:**
- Generate motif-depth deltas for logistic, Planck, and currently supported scientific laws where metadata is available.
- Generate regime comparison rows for blind/scaffolded/warm-start/perturbed outcomes.
- Add repair/refit or candidate-pool diagnostic rows from archived or current evidence.
- Add scoped local conventional baseline diagnostics when feasible, clearly separated from EML recovery.

**Requirements:** ABL-01, ABL-02, ABL-03, BASE-01, CLAIM-02

**Success criteria:**
- Ablation rows identify changed variable, held constants, source artifacts, and limitations.
- Baseline rows are diagnostic-only and do not affect recovery denominators.
- Tests cover schema and fail-closed status labels.

### Phase 62: Paper Figure and Table Data Pipeline

**Goal:** Generate deterministic, plot-ready paper assets from locked evidence.

**Scope:**
- Add a paper asset generator for machine-readable source tables and deterministic SVG figures.
- Emit regime recovery, depth degradation, scientific-law support, motif delta, training outcome/lifecycle, failure taxonomy, and baseline diagnostic assets.
- Include figure metadata with denominators, included statuses, source tables, and claim boundaries.

**Requirements:** FIG-01, FIG-02, PAPER-03

**Success criteria:**
- Every figure has adjacent source data and a manifest entry.
- Figures are generated from artifact fields, not recomputed claim logic.
- Tests verify representative figure/table generation and non-empty SVG output.

### Phase 63: Paper Package Assembly and Claim Audit

**Goal:** Assemble the final v1.11 paper evidence package and verify it is claim-safe.

**Scope:**
- Generate `artifacts/paper/v1.11/` with manifest, source locks, tables, figures, claim ledger, claim boundaries, scientific-law table, and reproduction commands.
- Audit logistic/Planck status, mixed-regime denominators, figure source coverage, and unsupported/failure visibility.
- Update docs and planning state with actual results.

**Requirements:** PAPER-01, PAPER-02, PAPER-03, FIG-01, FIG-02, CLAIM-01, CLAIM-02, CLAIM-03

**Success criteria:**
- Final package is reproducible from recorded commands.
- Scientific-law table reflects current evidence.
- Claim audit passes without hiding unsupported rows or non-blind evidence classes.

## Execution Order

1. Phase 59
2. Phase 60
3. Phase 61
4. Phase 62
5. Phase 63

## Notes

- Keep v1.6, v1.9, and v1.10 artifacts immutable and use them as source-locked anchors.
- Prefer small current-code reruns over broad compute-heavy campaigns.
- Logistic and Planck remain unsupported unless the full existing strict contract passes.

---
*Roadmap opened for v1.11 on 2026-04-19*
