# Phase 31: Perturbed Basin Training and Local Repair - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, requirements, prior phase evidence, and Phase 30 review blocker

<domain>
## Phase Boundary

Phase 31 proves basin behavior, not blind discovery. It may start from an exact EML target tree, perturb that tree's active categorical logits under declared deterministic noise envelopes, train, snap, and verify whether the result returns to a verifier-owned recovered or equivalent expression.

This phase also owns local snap/discrete repair for near-miss perturbed candidates, especially Beer-Lambert high-noise failures diagnosed in v1.4 as active-slot perturbation. Repair may improve or explain failed candidates, but it must preserve provenance and remain distinct from raw perturbed-training recovery.

Phase 31 can proceed while Phase 30 remains review-blocked because the roadmap declares Phase 31 depends only on Phase 29. Later Phase 32/33 work must incorporate the Phase 30 blocker honestly.

</domain>

<decisions>
## Implementation Decisions

### Perturbed Basin Claim Scope

- **D-01:** Treat perturbed true-tree training as same-basin recovery evidence, not discovery evidence. Starting from the exact tree and perturbing its active categorical choices is valid for `paper-perturbed-true-tree-basin`.
- **D-02:** Declare all perturbation bounds before execution in the suite contract: target inventory, EML depth, active-slot noise values, seeds, optimizer budgets, and accepted evidence classes.
- **D-03:** Keep the first proof inventory small and deterministic. Prefer source-document formulas already compiled into exact EML plus a synthetic exact-tree set that covers multiple depths without creating an expensive random-tree campaign.
- **D-04:** Do not let Phase 30 scaffolded blind evidence satisfy Phase 31. Perturbed runs must use `training_mode == "perturbed_true_tree_training"` or an explicitly repaired evidence class.

### Beer-Lambert and Bound Narrowing

- **D-05:** Beer-Lambert high-noise cases are first-class Phase 31 targets because v1.4 showed failures at high perturbation noise from active-slot changes.
- **D-06:** If all declared Beer-Lambert noise levels recover after training and/or repair, record the bound as supported. If high noise still fails, narrow the supported bound to the largest noise envelope with committed evidence and leave the failing level visible as measured unsupported evidence.
- **D-07:** Do not hide a high-noise failure by dropping it silently from reports. Any narrowed bound must cite raw run artifacts, failure classification, and the exact reason the larger bound is not claimed.

### Local Repair Semantics

- **D-08:** Local repair may inspect snapped candidates, nearby slot alternatives, subtree replacements, or exact target-neighborhood moves, but it must serialize what changed and why.
- **D-09:** A repaired candidate must be classified separately as `repaired_candidate`; it must not be reported as same-AST return or raw perturbed true-tree recovery.
- **D-10:** Same-AST return, verified-equivalent AST, repaired AST, snapped-but-failed, soft-fit-only, unsupported, and execution failure must remain separate in artifacts and aggregates.

### Runtime and Verification

- **D-11:** Favor CI-scale deterministic bounds over broad campaigns. Use small seeds/noise grids that prove the claim while keeping tests practical.
- **D-12:** Verification remains verifier-owned: training loss, same-AST checks, or repair success alone cannot mark a candidate recovered without held-out, extrapolation, and high-precision checks.

### the agent's Discretion

- Choose exact synthetic tree inventory and noise grid after researching current compiler/master-tree/warm-start capabilities.
- Choose whether local repair lives in `warm_start.py`, a new `repair.py`, or benchmark orchestration, based on existing module boundaries.
- Choose the smallest deterministic Beer-Lambert bound that is supported by evidence if the current high-noise envelope is still too broad.

</decisions>

<specifics>
## Specific Ideas

- Existing v1.4 evidence: Beer-Lambert perturbation recovery remained incomplete at high noise, and diagnostics identified active-slot perturbation as the failure mechanism.
- Existing code already has `PerturbationConfig`, `perturb_tree_logits()`, compiler warm-start training, perturbation diagnostics in artifacts, and campaign/report grouping by perturbation noise.
- Existing proof claim `paper-perturbed-true-tree-basin` allows verifier-owned recovered or verified-equivalent candidates, while threshold policy also distinguishes `repaired_candidate`.
- Phase 30 review created `scaffolded_blind_training_recovered`; Phase 31 should not reuse that class.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase and Claim Context
- `.planning/REQUIREMENTS.md` - BASN-01 through BASN-05.
- `.planning/ROADMAP.md` - Phase 31 goal, success criteria, and dependency on Phase 29.
- `.planning/STATE.md` - v1.4 Beer-Lambert perturbation evidence and Phase 30 blocker.
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-VERIFICATION.md` - verified proof contract behavior.
- `.planning/phases/30-bounded-shallow-blind-training-recovery/30-REVIEW.md` - clean review plus unresolved SHAL-02 blocker.

### Existing Code
- `src/eml_symbolic_regression/warm_start.py` - perturbation config, active-slot perturbation, warm-start fit manifest, failure diagnosis.
- `src/eml_symbolic_regression/benchmark.py` - perturbation runs, training modes, artifacts, metrics, evidence classes, threshold aggregation.
- `src/eml_symbolic_regression/proof.py` - `paper-perturbed-true-tree-basin`, threshold policies, evidence classes.
- `src/eml_symbolic_regression/compiler.py` - exact EML compilation for source-document formulas.
- `src/eml_symbolic_regression/master_tree.py` - embedding, logits, snapping, active slots.
- `src/eml_symbolic_regression/diagnostics.py` - Beer-Lambert perturbation failure selection and reports.

### Tests and Evidence
- `tests/test_compiler_warm_start.py` - perturbation behavior and active-slot diagnosis.
- `tests/test_benchmark_contract.py` - perturbation run validation and proof metadata.
- `tests/test_benchmark_runner.py` - perturbation benchmark artifact smoke tests.
- `tests/test_benchmark_reports.py` - threshold aggregation behavior.
- `tests/test_diagnostics.py` - diagnostic selection for Beer-Lambert perturbation failures.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `fit_warm_started_eml_tree()` already compiles, embeds, perturbs, trains, snaps, and records same-AST/equivalent/recovery details.
- `PerturbationReport` records active slot changes and noise metadata.
- Benchmark run artifacts already expose `perturbation_active_slot_changes`, best loss, post-snap loss, snap margin, active node count, and verifier status.
- Campaign and diagnostics code already group Beer-Lambert perturbation behavior and can select high-noise failures.

### Likely Gaps
- No dedicated proof suite exists yet for `paper-perturbed-true-tree-basin`.
- The current benchmark warm-start mode is compiler-oriented; Phase 31 may need a proof-specific perturbed true-tree training mode and evidence-class derivation.
- No local snap/discrete repair module exists yet.
- No committed evidence currently narrows or supports a Beer-Lambert high-noise bound under Phase 31 proof semantics.

</code_context>

<deferred>
## Deferred Ideas

- Pure blind scaled-exponential recovery remains a Phase 30 blocker and should not be solved inside Phase 31.
- Depth 2 through 6 blind-vs-perturbed recovery curves belong to Phase 32; Phase 31 should produce the perturbed-basin primitives and bounded proof suite needed by that phase.
- Final proof campaign report and committed evidence lockdown belong to Phase 33.

</deferred>

---

*Phase: 31-perturbed-basin-training-and-local-repair*
*Context gathered: 2026-04-15*
