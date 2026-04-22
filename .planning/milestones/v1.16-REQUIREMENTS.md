# Requirements: EML Symbolic Regression v1.16

**Milestone:** v1.16 Paper-Strength GEML Recovery Evidence
**Created:** 2026-04-22
**Source context:** v1.15 GEML evidence package decision `inconclusive_smoke_only`

## Goal

Address the problems surfaced by v1.15: no verifier-gated exact recoveries, only smoke-scale paired evidence, loss-only i*pi signals, branch-sensitive optimization, and no paper-positive claim. v1.16 must either produce paper-strength i*pi/GEML recovery evidence or a defensible negative/inconclusive result.

## Success Definition

A positive i*pi/GEML paper claim requires verifier-gated exact recovery under a matched raw EML versus i*pi EML protocol. Lower training or held-out loss is useful only as a diagnostic unless it snaps to exact candidates that pass the verifier. Negative controls, branch diagnostics, resource metadata, and source locks remain part of the evidence package even when they weaken the headline.

## Paper-Strength Success Contract

- **STRG-01**: Define paper-positive thresholds in terms of verifier-gated exact recovery, not loss-only improvement.
- **STRG-02**: Report i*pi EML natural-bias wins against raw EML under matched depth, budget, data split, snap rule, and verifier gates.
- **STRG-03**: Keep negative controls visible and prevent uncontrolled i*pi advantage from supporting paper-positive claims.
- **STRG-04**: Classify the final result as `paper_positive`, `promising_preliminary`, `negative`, or `inconclusive` using predefined criteria.

## i*pi-Aware Search Improvements

- **SRCH-01**: Add branch-safe periodic, phase-log, or related initialization/prior mechanisms that are generic to target families and do not embed exact formulas.
- **SRCH-02**: Improve optimizer schedules, hardening, and candidate pooling for fixed GEML operators so i*pi rows can produce verifier-gated exact candidates, not just lower losses.
- **SRCH-03**: Add branch-aware penalties, guards, schedules, or diagnostics while preserving the training-mode versus faithful-verification separation.
- **SRCH-04**: Add a budget ladder from smoke to pilot to paper campaign so expensive runs happen only after meaningful exact-recovery signal.
- **SRCH-05**: Preserve raw EML regressions and v1.14/v1.15 recovery-accounting fields under all search changes.

## Benchmark and Campaign Evidence

- **CAMP-01**: Run a multi-seed matched raw EML versus i*pi EML campaign over the full v1.15 target set or a justified paper subset.
- **CAMP-02**: Aggregate exact recovery, loss, branch, runtime/resource, and failure taxonomy metrics by target family and operator.
- **CAMP-03**: Include confidence intervals or seed-level variation summaries so one lucky run cannot carry the claim.
- **CAMP-04**: Store reproducible command manifests and source locks for all paper-candidate campaigns.

## Ablation and Failure Analysis

- **ABL-01**: Compare branch guards, initialization, constants, depth, budget, and candidate-pooling variants against the same target families.
- **ABL-02**: Separate exact recovery, verified-equivalent recovery, repaired candidate, same-AST/warm-start, and loss-only outcomes.
- **ABL-03**: Classify failures as optimization miss, snap mismatch, branch pathology, verifier mismatch, unsupported/over-depth, or numerical instability.
- **ABL-04**: Produce actionable next-step diagnostics if i*pi remains inconclusive or negative.

## Paper Evidence Package

- **PAPER-01**: Generate paper-grade figures and tables for family recovery, loss before/after snap, branch anomalies, runtime, and representative fitted curves.
- **PAPER-02**: Build a v1.16 evidence package with source locks, campaign manifests, aggregate tables, ablation tables, reproduction commands, and claim audit.
- **PAPER-03**: Block global superiority, broad blind-recovery, full universality, loss-only recovery, and negative-control cherry-picking claims.
- **PAPER-04**: State whether the result is paper-positive, promising-but-preliminary, negative, or inconclusive under the declared gate.

## Future Requirements

- **FUT-01**: Learn continuous `a` values after fixed i*pi evidence is meaningful.
- **FUT-02**: Add external symbolic-regression baselines once the internal raw/i*pi comparison is stable.
- **FUT-03**: Add formal theorem-prover certificates for restricted identities.
- **FUT-04**: Run larger standardized hardware campaigns after the smoke and pilot gates justify them.

## Out of Scope

- Weakening the verifier or counting loss-only improvement as recovery.
- Exact target seeding, formula-name recognizers, or hard-coded exact target trees.
- Dropping negative controls because they hurt the story.
- Claiming i*pi EML is globally better than raw EML.
- Claiming full `GEML_a` or i*pi EML universality without constructive proof.
- Large open-ended deep blind campaigns before smoke and pilot gates show exact-recovery signal.

## Milestone Gate

The milestone passes only if the final package is internally consistent with the predefined claim class. A positive result must satisfy the exact-recovery gate. A negative or inconclusive result passes only if it includes source-locked campaigns, ablations, failure taxonomy, and a clear explanation of what blocks a stronger paper claim.
