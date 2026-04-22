# Phase 90: Budget Ladder and Pilot Recovery Runs - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Create a smoke -> pilot -> full budget ladder for v1.16 GEML evidence. The ladder must summarize exact-recovery signal, branch/failure diagnostics, source locks, and decide whether the full campaign is justified.

</domain>

<decisions>
## Implementation Decisions

### Pilot Gate
- Full campaign runs only when pilot evidence has verifier-gated exact i*pi signal on natural-bias targets.
- If pilot evidence is missing, loss-only, or confounded, Phase 91 should produce a fail-closed negative/inconclusive package instead of launching full runs.
- Smoke and pilot tiers must write reproducible command manifests and source locks.
- The gate must be deterministic from committed campaign outputs.

### Failure Taxonomy
- Failure classes should include optimization/snap miss, loss-only signal, branch pathology, verifier mismatch, unsupported/over-depth, and numerical instability.
- Taxonomy should be table-friendly JSON/CSV/Markdown.
- The taxonomy should be source-locked to the campaign comparison rows.
- Missing campaign files should produce explicit `not_performed` rows, not silent success.

### the agent's Discretion
Implement the ladder in the v1.16 paper package module and expose it via CLI for repeatability.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `campaign.py` already writes `geml-paired-comparison.csv` and `geml-paired-summary.json`.
- `paper_v116.py` already has the gate evaluator and source-lock helpers.
- CLI command patterns are simple `argparse` subcommands.

### Established Patterns
- Evidence packages write JSON plus Markdown, then tests inspect both.
- Missing evidence must fail closed and remain visible.

### Integration Points
- The ladder decision feeds Phase 91 package routing.
- Failure taxonomy feeds Phase 92 ablation/figure assets.

</code_context>

<specifics>
## Specific Ideas

Add `write_v116_budget_ladder` with smoke/pilot paths and a `geml-v116-ladder` CLI command.

</specifics>

<deferred>
## Deferred Ideas

Full paper campaign execution is Phase 91 and should be skipped if the pilot gate fails.

</deferred>
