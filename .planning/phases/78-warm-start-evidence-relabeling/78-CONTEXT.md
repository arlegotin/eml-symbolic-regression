# Phase 78 Context: Warm-Start Evidence Relabeling

## Goal

Publication-track warm starts must be labeled by the evidence they actually provide. Existing zero-perturbation same-AST rows should read as exact seed round-trips or same-AST retention, not robust warm-start basin evidence.

## Relevant Requirements

- WARM-01: Zero-perturbation same-AST warm-start positives are labeled exact seed round-trip or same-AST retention.
- WARM-02: Warm-start tables expose perturbation noise, warm steps, warm restarts, total restarts, return kind, and same/equivalent AST status.
- WARM-03: Robustness or basin wording is absent unless backed by nonzero perturbation, multiple seeds, and more than one optimization step.
- WARM-04: README, reports, aggregates, and paper-facing text use exact seed round-trip language for the current publication rows.

## Current State

- Phase 77 already split `verification_outcome`, `evidence_regime`, and `discovery_class`.
- Warm-start rows already expose `perturbation_noise`, `warm_steps`, `warm_restarts`, `return_kind`, and changed-slot metrics in campaign CSV.
- The remaining gap is semantic: same-AST warm-start rows still appear under generic basin wording in README/report prose, and CSV rows do not carry a single explicit evidence label or total-restart count.

## Constraints

- Do not weaken verifier gates or promote compile-only rows.
- Do not regenerate committed publication artifacts in this phase; Phase 81 owns artifact rebuild.
- Preserve backward-compatible classifications such as `same_ast_warm_start_return` and `same_ast`.
- Keep tests focused on report/table semantics rather than long campaign execution.

