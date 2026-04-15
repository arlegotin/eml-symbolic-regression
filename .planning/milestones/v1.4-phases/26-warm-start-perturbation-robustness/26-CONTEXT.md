# Phase 26: Warm-Start Perturbation Robustness - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase improves Beer-Lambert high-perturbation interpretability. It may add diagnostics that narrow why a perturbed warm start fails, but it must not relabel failed trained snaps as recovered and must not weaken literal-constant provenance.

</domain>

<decisions>
## Implementation Decisions

### Perturbation Diagnostics
- Keep current warm-start status taxonomy: `same_ast_return`, `verified_equivalent_ast`, `snapped_but_failed`, `soft_fit_only`, and `failed`.
- Add a nested diagnosis block to warm-start manifests that records active slot counts, changed slot counts, verifier status, snap margin, losses, and a failure mechanism label.
- Prefer precise explanation over automatic fallback to the compiled seed; fallback would obscure whether training recovered from perturbation.
- Surface failure mechanism through benchmark metrics and campaign CSVs so before/after reports can group high-noise failures.

### Semantics Boundary
- Do not change verifier tolerances or `verify_candidate`.
- Do not add literal constants beyond those coming from compiler metadata.
- Do not mark original compiled seed verification as trained recovery.

### the agent's Discretion
The exact failure mechanism labels are at the agent's discretion, but they must separate active-slot perturbation, snap instability, verifier mismatch, soft-fit-only, and non-finite snap paths.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `fit_warm_started_eml_tree` already receives compiler metadata, perturbation reports, fit manifest, and verification output.
- `PerturbationReport` already records active-slot changes before and after perturbation.
- `benchmark._extract_run_metrics` already surfaces `changed_slot_count` and verifier status from warm-start manifests.

### Established Patterns
- Warm-start statuses remain distinct from blind recovery.
- Metrics are copied into aggregate/campaign rows for CSV and reporting.

### Integration Points
- Add diagnosis to `warm_start.py`.
- Surface diagnosis fields in `benchmark.py`.
- Add a CSV column in `campaign.py`.
- Add tests in warm-start and campaign coverage.

</code_context>

<specifics>
## Specific Ideas

For high-noise Beer-Lambert failures, the useful mechanism is usually changed active slots followed by verifier failure. Capture that directly instead of only showing `reason: verified` from the compiled seed.

</specifics>

<deferred>
## Deferred Ideas

Actual discrete repair or local search around perturbed warm-start snaps is deferred until diagnostics show which mechanism dominates.

</deferred>
