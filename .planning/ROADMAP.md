# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-20
**Current milestone:** v1.13 Publication-grade reproduction and validation
**Phase numbering:** Continuing from v1.12 Phase 68.

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
- **v1.13 Publication-grade reproduction and validation** - Phases 69-76 planned

## Current Status

v1.13 is active. The milestone responds to a publication-readiness audit: the repo must support a true clean-room rebuild, stronger verifier and split discipline, semantic-mismatch evidence, full tests/CI, theorem-faithful versus convenience benchmark tracks, real matched baselines, broader datasets, and final `main` publication after the evidence package is regenerated.

## Phase Status

- [x] Phase 69: Clean-Room Reproduction Path and Provenance (completed 2026-04-20)
- [x] Phase 70: Layered Verifier and Split Isolation (completed 2026-04-20)
- [x] Phase 71: Training and Verification Semantics Alignment (completed 2026-04-20)
- [x] Phase 72: Automated Test Suite and CI Hardening (completed 2026-04-20)
- [ ] Phase 73: Basis-Only and Literal-Constants Benchmark Tracks
- [ ] Phase 74: Expanded Dataset and Manifest Suite
- [ ] Phase 75: Matched Conventional Baseline Harness
- [ ] Phase 76: Full Evidence Rebuild, Claim Audit, and Public Main Sync

## Phase Overview

| Phase | Name | Goal | Requirements |
|-------|------|------|--------------|
| 69 | Clean-Room Reproduction Path and Provenance | Build the locked one-command rebuild path and remove publication placeholder provenance. | REPRO-01, REPRO-02, REPRO-03, REPRO-04, REPRO-05 |
| 70 | Layered Verifier and Split Isolation | Upgrade verifier evidence and eliminate selection/final-evaluation leakage. | VERIF-01, VERIF-02, VERIF-03, VERIF-04, VERIF-05, SPLIT-01, SPLIT-02, SPLIT-03 |
| 71 | Training and Verification Semantics Alignment | Match training to verified semantics where possible and quantify surrogate mismatch where not. | SEM-01, SEM-02, SEM-03, SEM-04 |
| 72 | Automated Test Suite and CI Hardening | Add algorithmic tests and CI gates for code, manifests, reproduction smoke, and public snapshots. | TEST-01, TEST-02, TEST-03, TEST-04 |
| 73 | Basis-Only and Literal-Constants Benchmark Tracks | Split theorem-faithful and convenience tracks across benchmark configs and reports. | TRACK-01, TRACK-02, TRACK-03 |
| 74 | Expanded Dataset and Manifest Suite | Add noisy, parameter, multivariable, unit-aware, and real-data evidence inputs with independent splits. | DATA-01, DATA-02 |
| 75 | Matched Conventional Baseline Harness | Run EML and external symbolic-regression baselines under one standardized budget contract. | BASE-01, BASE-02 |
| 76 | Full Evidence Rebuild, Claim Audit, and Public Main Sync | Run all publication training/artifact generation, block unsafe claims, and publish the validated public snapshot to `main`. | PUB-01, PUB-02, PUB-03, PUB-04 |

## Phase Details

### Phase 69: Clean-Room Reproduction Path and Provenance

**Goal:** A fresh checkout can rebuild the publication package in a locked environment without preexisting generated artifacts.

**Requirements:** REPRO-01, REPRO-02, REPRO-03, REPRO-04, REPRO-05

**Success criteria:**
1. A single documented command rebuilds all paper-facing figures, tables, aggregates, manifests, and source locks from source inputs.
2. Lockfile and container entrypoints are committed and wired into the reproduction command.
3. Paper-package generation no longer depends on `--require-existing` for the publication path.
4. Generated manifests contain real git, command, environment, input-hash, output-hash, and timestamp provenance.
5. Placeholder snapshot metadata is either gone from publication artifacts or explicitly confined to deterministic-test fixtures.

### Phase 70: Layered Verifier and Split Isolation

**Goal:** Recovery claims are verifier-owned, evidence-level labeled, and isolated from candidate-selection leakage.

**Requirements:** VERIF-01, VERIF-02, VERIF-03, VERIF-04, VERIF-05, SPLIT-01, SPLIT-02, SPLIT-03

**Success criteria:**
1. Verifier attempts symbolic equivalence or targeted simplification before falling back to numeric falsification.
2. Non-symbolic candidates are checked on fresh dense randomized points plus adversarial domain and branch-cut probes.
3. Interval/certificate status is reported for intended real domains, including explicit unsupported labels.
4. Candidate ranking uses only allowed training/selection data and cannot see final confirmation splits.
5. Artifacts label training, selection, diagnostic, verifier, and final-confirmation metrics separately.

### Phase 71: Training and Verification Semantics Alignment

**Goal:** The optimizer either searches verified semantics directly or publishes hard evidence about surrogate clamp/log-guard mismatch.

**Requirements:** SEM-01, SEM-02, SEM-03, SEM-04

**Success criteria:**
1. A faithful-semantics training mode exists for supported domains, or artifacts explain why a fallback is used.
2. Clamp/log-guard ablations quantify spurious-recovery risk across the publication benchmark matrix.
3. Every training artifact reports clamp, guard, NaN/Inf, branch, and post-snap mismatch diagnostics.
4. Scientific-law rows carry real-domain and branch-validity certificate status.

### Phase 72: Automated Test Suite and CI Hardening

**Goal:** The public repo has meaningful algorithmic tests and CI, not just packaging/framing checks.

**Requirements:** TEST-01, TEST-02, TEST-03, TEST-04

**Success criteria:**
1. Tests cover EML semantics, branch behavior, compiler contracts, verifier evidence levels, split isolation, and manifest validation.
2. A minimal evidence-regression test exercises train -> snap -> verify -> artifact generation.
3. GitHub Actions runs unit tests, selected integration smoke, clean-room reproduction smoke, and public snapshot validation.
4. CI validates branch discipline for `dev` and `main` without requiring local-only artifacts.

### Phase 73: Basis-Only and Literal-Constants Benchmark Tracks

**Goal:** Paper-faithful synthesis and applied literal-constant recovery are separate benchmark tracks with separate denominators.

**Requirements:** TRACK-01, TRACK-02, TRACK-03

**Success criteria:**
1. Every publication benchmark target has a basis-only configuration.
2. Every publication benchmark target has a literal-constant-augmented configuration with constants policy visible in artifacts.
3. Campaign aggregates and paper tables keep the two tracks separate.
4. CLI defaults and docs avoid presenting literal-constant runs as bare `{1, eml, variables}` synthesis.

### Phase 74: Expanded Dataset and Manifest Suite

**Goal:** Evidence extends beyond normalized noiseless synthetic demos and records split/domain provenance.

**Requirements:** DATA-01, DATA-02

**Success criteria:**
1. New dataset families cover noisy sweeps, parameter-identifiability stress, multivariable inputs, unit-aware formulas, and at least one real dataset path with independent splits.
2. Dataset manifests record source/generator, units, noise policy, split policy, domain constraints, and synthetic/semi-synthetic/real classification.
3. Expanded datasets feed the same verifier, split, benchmark-track, and baseline harness contracts.
4. Reports mark which conclusions are controlled synthetic evidence versus broader scientific-data evidence.

### Phase 75: Matched Conventional Baseline Harness

**Goal:** Conventional symbolic-regression systems run through the same datasets, seeds, budgets, constants policy, and blind/warm-start distinctions as EML.

**Requirements:** BASE-01, BASE-02

**Success criteria:**
1. A baseline harness can run EML and selected external SR baselines with shared dataset, seed, time-budget, constants-policy, and split definitions.
2. Baseline dependency checks are fail-closed and source-locked, with unavailable integrations reported explicitly.
3. Baseline outputs include the same manifest, metric, and final-confirmation fields needed for paper tables.
4. EML recovery denominators remain separate from baseline comparison tables.

### Phase 76: Full Evidence Rebuild, Claim Audit, and Public Main Sync

**Goal:** The final publication evidence package is regenerated, audited, committed on `dev`, and propagated to `main` only after passing release gates.

**Requirements:** PUB-01, PUB-02, PUB-03, PUB-04

**Success criteria:**
1. All necessary v1.13 training and evidence-generation commands complete and produce committed artifacts.
2. The publication root manifest links artifacts, source locks, claim audit, reproduction command, environment identity, and branch provenance.
3. Claim audit fails unsafe recovery claims lacking verifier evidence, final confirmation status, constants-track label, baseline context, or source lock.
4. `dev` contains the full validated implementation and artifact set.
5. `main` receives the intended public code, tests, CI, reproduction entrypoints, and selected artifacts after the full rebuild passes.

## Dependency Notes

- Phase 69 must land before Phase 76 because the final package needs the clean-room rebuild path.
- Phase 70 must land before Phases 73-76 because benchmark and publication claims depend on the new verifier/split contract.
- Phase 71 must land before full publication campaigns because training evidence must report faithful semantics or quantified mismatch.
- Phase 72 can run after Phases 69-71 so CI tests the final contracts rather than only legacy behavior.
- Phases 73-75 expand the evidence matrix; Phase 76 regenerates and publishes the locked package.

## Notes

- Current v1.12 paper draft artifacts remain at `artifacts/paper/v1.11/draft/`.
- Current v1.12 supplement remains at `artifacts/paper/v1.11/v1.12-supplement/`.
- v1.13 should create new source-locked artifacts rather than overwriting archived v1.4-v1.12 evidence anchors.

---
*Roadmap created for v1.13 on 2026-04-20*
