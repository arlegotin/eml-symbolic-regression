# Phase 23: Campaign Smoke, Docs, and Report Lockdown - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated in autonomous execution

<domain>
## Phase Boundary

This phase locks the v1.3 campaign/report workflow with focused tests, documentation, a committed smoke campaign artifact, and full test-suite verification.

</domain>

<decisions>
## Implementation Decisions

### Test Lockdown
- Add CLI coverage for the campaign command writing `report.md`.
- Treat focused campaign tests as coverage for preset expansion, overwrite guardrails, CSV export, plot generation, and report assembly.
- Run full `pytest` before completion.

### Documentation
- Update README and implementation notes with campaign commands, output structure, CSV/figure meanings, and honest presentation rules.
- Document the committed smoke report and its current metrics.

### Evidence Artifact
- Commit `artifacts/campaigns/v1.3-smoke/` as the reproducible smoke evidence bundle.
- Keep the artifact small by using the smoke preset rather than the standard/showcase preset.

### the agent's Discretion
- The agent may leave the known NumPy overflow warning as non-blocking because tests pass and the warning comes from stress evaluation.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tests/test_campaign.py` already covers campaign tables, plots, and report content.
- `tests/test_benchmark_runner.py` already has CLI subprocess patterns.

### Established Patterns
- Existing v1.2 smoke benchmark artifacts are committed under `artifacts/benchmarks/smoke/`.
- Documentation emphasizes verifier-owned recovery and honest limitations.

### Integration Points
- The committed smoke report should be referenced from README.

</code_context>

<specifics>
## Specific Ideas

Use the smoke campaign to show the full pipeline without hiding weak results.

</specifics>

<deferred>
## Deferred Ideas

Standard/showcase campaign runs can be produced by users as needed; they are not committed in this phase.

</deferred>
