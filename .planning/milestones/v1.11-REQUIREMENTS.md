# Requirements: v1.11 Paper-strength evidence and figure package

**Milestone:** v1.11  
**Status:** Active  
**Created:** 2026-04-19  
**Goal:** Produce a stronger paper-ready evidence package by running real training where it is honest, adding low-hanging empirical comparisons and ablations, and generating plot-rich artifacts that clearly illustrate the EML hybrid pipeline.

## Evidence Contracts

### PAPER-01: v1.11 paper package source locks

The v1.11 paper package MUST include file-level source locks for every evidence input used by tables, figures, and claim ledgers.

Acceptance:
- `artifacts/paper/v1.11/` contains `manifest.json` and `source-locks.json`.
- Source locks include archived v1.6/v1.9 proof or paper sources when reused.
- Source locks include v1.10 logistic and Planck focused campaign artifacts.
- Source locks include all new v1.11 campaign, ablation, baseline, table, and figure sources.

### PAPER-02: Current scientific-law table

The paper-facing scientific-law table MUST use current v1.10 logistic and Planck diagnostics instead of stale relaxed-depth rows.

Acceptance:
- Logistic is reported as unsupported unless a new strict verifier-owned artifact passes.
- Planck is reported as unsupported unless a new strict verifier-owned artifact passes.
- Logistic relaxed depth, strict gate, macro hits, validation status, and artifact path are present.
- Planck relaxed depth, strict gate, macro hits, validation status, and artifact path are present.
- Shockley, Arrhenius, and Michaelis-Menten supported/warm-start rows remain present and regime-labeled.

### PAPER-03: Claim-class ledger

The final package MUST include a machine-readable claim ledger that separates pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed evidence.

Acceptance:
- Every paper claim row has `claim_id`, `evidence_class`, `eligible_denominator`, `source_ids`, and `public_claim`.
- No recovery rate is computed from loss-only fields.
- Unsupported and failed rows remain visible in denominators where eligible.

## Real Training Evidence

### TRAIN-01: Claim-safe training reruns

v1.11 MUST run real training under current code for bounded, claim-safe regimes.

Acceptance:
- At least one shallow pure-blind suite is run and aggregated.
- At least one scaffolded or compiler-seeded suite is run and aggregated separately from pure blind.
- At least one warm-start or same-AST scientific-law suite is run and aggregated.
- At least one perturbed-basin suite is run and aggregated.
- Each run records seed, budget, start mode, verifier status, artifact path, and evidence class.

### TRAIN-02: Logistic and Planck probes

Logistic and Planck MUST receive current-code focused probe artifacts, but they MUST remain unsupported unless the strict support and verifier contract pass.

Acceptance:
- Compile diagnostics are included for logistic and Planck.
- Any training or warm-start probe records status and failure/unsupported reason.
- The package does not promote either law from relaxed compile depth alone.

### TRAIN-03: Training lifecycle diagnostics

Training artifacts MUST preserve the optimizer-to-verifier lifecycle needed for paper figures.

Acceptance:
- Run artifacts expose best soft loss, post-snap loss when available, selected candidate status, repair/refit status when used, and verifier result.
- Aggregate tables include failure/unsupported reason codes.
- Figure source tables can link back to raw run artifacts.

## Ablations and Baselines

### ABL-01: Motif-depth ablation

The package MUST include a motif-depth diagnostic showing the effect of reusable compiler motifs on at least logistic and Planck, and ideally supported scientific laws.

Acceptance:
- Rows include baseline depth/nodes, motif depth/nodes, deltas, macro hits, validation status, and artifact path.
- The ablation does not change gates, datasets, or verifier criteria while attributing motif effects.

### ABL-02: Regime comparison ablation

The package MUST compare pure blind, scaffolded, warm-start/same-AST, and perturbed-basin regimes without merging denominators.

Acceptance:
- Rows include formula, start mode, seed count, verifier recovery count, same-AST count, unsupported count, failed count, and recovery rate.
- Figure captions or metadata declare eligible evidence classes.

### ABL-03: Repair/refit and candidate-pool diagnostics

The package SHOULD include low-hanging repair/refit or candidate-pool diagnostics from archived or newly generated evidence.

Acceptance:
- Rows distinguish raw selected candidate, repaired candidate, refit result, fallback preservation, and final verifier status.
- No repair/refit row is counted as pure blind discovery.

### BASE-01: Scoped conventional baseline diagnostics

v1.11 SHOULD include lightweight local or conventional baseline diagnostics if feasible without creating a broad benchmark competition.

Acceptance:
- Baseline rows are labeled as diagnostic, prediction-only, unavailable, or deferred.
- Baseline rows record dataset split, method, parameters or model summary, metrics, status, and limitation text.
- Baseline results do not enter EML recovery denominators.

## Figures and Tables

### FIG-01: Plot-ready source tables

Every v1.11 paper figure MUST have a machine-readable source table or JSON file next to it.

Acceptance:
- Source tables cover regime recovery, depth degradation, scientific-law support, motif deltas, training outcomes, failure taxonomy, and baseline diagnostics where available.
- Tables include source IDs or artifact paths.

### FIG-02: Deterministic publication figures

The package MUST generate deterministic SVG figures suitable for paper drafting.

Acceptance:
- Figures include regime recovery, depth degradation, scientific-law support, motif depth deltas, training outcomes or lifecycle, and failure taxonomy.
- Figure metadata records source table, included statuses, excluded statuses, denominator, and claim boundary.
- Figure generation is test-covered with small fixtures or generated smoke artifacts.

## Claim Boundaries

### CLAIM-01: No silent gate relaxation

No v1.11 code or artifact may silently loosen strict support gates.

Acceptance:
- Strict and relaxed gates are reported separately.
- Any next-milestone or exploratory gate is named explicitly and compared against the existing strict gate.

### CLAIM-02: No formula-name recognizers

Compiler or paper-package changes MUST NOT introduce formula-name or exact-constant special cases.

Acceptance:
- New diagnostics are structural, artifact-derived, or source-locked.
- Tests cover fail-closed behavior for unsupported rows where applicable.

### CLAIM-03: Package audit

The final v1.11 package MUST pass an automated or scripted claim audit before the milestone can be archived.

Acceptance:
- Logistic and Planck statuses are audited against source artifacts.
- Recovery-rate denominators are audited for mixed evidence classes.
- Every figure has source data and a manifest entry.
- Reproduction commands are included.
