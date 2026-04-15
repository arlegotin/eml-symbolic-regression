# Phase 28: Before/After Campaign Evaluation - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase reruns the same standard/showcase campaign contracts after v1.4 optimizer/compiler changes, then compares v1.4 outputs against committed v1.3 baselines. It does not introduce more algorithmic changes except comparison/reporting code and documentation.

</domain>

<decisions>
## Implementation Decisions

### Campaign Evidence
- Generate `artifacts/campaigns/v1.4-standard/` and `artifacts/campaigns/v1.4-showcase/` with the existing campaign command and overwrite guard.
- Compare against `artifacts/campaigns/v1.3-standard/` and `artifacts/campaigns/v1.3-showcase/`.
- Keep all failed/unsupported cases in denominators.
- Report overall deltas and target-category deltas for blind recovery, Beer-Lambert perturbation robustness, and compiler coverage.

### Comparison Contract
- Compute deltas for verifier recovery rate, unsupported rate, failure rate, median best loss, median post-snap loss, and median runtime.
- Classify categories as improved, regressed, or unchanged based on recovery/unsupported/failure rate movement, with loss/runtime as supporting metrics.
- Include one clean command that regenerates the comparison from existing v1.3/v1.4 campaign folders.

### the agent's Discretion
Report layout and exact JSON schema are at the agent's discretion, as long as the Markdown report is readable and the JSON output is machine-verifiable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `campaign.py` already generates standard/showcase campaign folders with aggregate, tables, figures, and reports.
- `diagnostics.py` already loads campaign directories and computes focused diagnostic filters.
- Phase 25 added blind comparison helpers.
- Phase 26 added warm-start mechanism metrics.
- Phase 27 moved Shockley compile coverage.

### Established Patterns
- Campaign reports are generated artifacts committed under `artifacts/campaigns/`.
- Evidence must remain reproducible from CLI commands.

### Integration Points
- Add comparison helpers and CLI command in diagnostics/CLI.
- Add tests for comparison JSON/Markdown.
- Update README with the one-command comparison flow.

</code_context>

<specifics>
## Specific Ideas

The main expected improvements are blind `exp`/`log` recovery from primitive scaffolds and Shockley moving from unsupported to verified compiled coverage. Beer-Lambert high-noise may remain failed but should now report `active_slot_perturbation`.

</specifics>

<deferred>
## Deferred Ideas

Further optimizer tuning, Beer-Lambert repair, Planck/logistic/Michaelis depth reduction, and external baselines are deferred to future milestones.

</deferred>
