# Phase 91: Full Matched GEML Paper Campaign - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce the full matched v1.16 GEML campaign only if the Phase 90 pilot gate passes. Because the actual pilot gate returned `stop_full_campaign_fail_closed`, this phase should produce a locked fail-closed negative/inconclusive package rather than launching the expensive full run.

</domain>

<decisions>
## Implementation Decisions

### Campaign Routing
- Do not run `geml-v116-full` after a pilot with zero verifier-gated exact recoveries.
- Package the pilot and ladder evidence as the Phase 91 fail-closed result.
- The package should preserve exact recovery, loss-only, branch, runtime, seed-level, and negative-control diagnostics.
- The package must explain that full campaign absence is a gate outcome, not missing work.

### Claim Accounting
- Loss-only, repaired, compile-only, and same-AST rows cannot contaminate trained exact-recovery denominators.
- The final package should remain eligible for Phase 92 ablation/failure analysis and Phase 93 claim audit.
- Source locks should include the pilot campaign and budget ladder artifacts.
- The result can be inconclusive if the gate says the exact-recovery signal is absent.

### the agent's Discretion
Extend the existing v1.16 package writer only as needed to include the budget-ladder source.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `write_v116_paper_package` already writes gate evaluation, decision, claim audit, reproduction, and source locks.
- `write_v116_budget_ladder` already records the full-campaign blocker.
- Campaign paired tables include branch diagnostics, loss metrics, runtime/resource metadata, and recovery-accounting fields.

### Established Patterns
- Paper packages fail closed rather than running broad campaigns after negative pilot gates.

### Integration Points
- Phase 92 will read the package, ladder, and campaign tables for ablation/failure artifacts.

</code_context>

<specifics>
## Specific Ideas

Add optional budget-ladder source locks to `geml-paper-v116`, then generate `artifacts/paper/v1.16-geml/` from the pilot campaign.

</specifics>

<deferred>
## Deferred Ideas

Running the full multi-seed paper campaign is deferred until a future milestone produces pilot exact-recovery signal.

</deferred>
