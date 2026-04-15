# Phase 21: Static Plot Generation - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated in autonomous execution

<domain>
## Phase Boundary

This phase generates deterministic static figures from campaign evidence. It covers recovery-rate charts, loss comparison, Beer-Lambert perturbation behavior, runtime/depth/budget cost, and failure taxonomy. Final report prose is deferred to Phase 22.

</domain>

<decisions>
## Implementation Decisions

### Plot Format
- Generate SVG files with stable names under `figures/`.
- Use standard-library SVG generation to avoid introducing plotting dependencies.
- Keep charts deterministic and directly linkable from Markdown.

### Chart Semantics
- Plot verifier recovery separately by formula and start mode.
- Use `-log10(loss)` for loss comparison so lower losses render as taller bars.
- Keep Beer-Lambert perturbation recovery separate from general recovery.
- Plot unsupported/failure taxonomy without hiding those runs.

### the agent's Discretion
- The agent can keep the visual style simple as long as charts are crisp, deterministic, and machine-generated from campaign evidence.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 20 added table and headline metrics derived from `aggregate_evidence`.
- Campaign manifests already collect output paths.

### Established Patterns
- Campaign outputs are rooted in a single labeled/timestamped folder.
- Tests should use smoke campaigns and inspect file existence/content rather than pixel screenshots.

### Integration Points
- `run_campaign` should call `write_campaign_plots` after table generation and add figure paths to the manifest.

</code_context>

<specifics>
## Specific Ideas

Use SVG so the report can link figures without binary dependencies or image conversion steps.

</specifics>

<deferred>
## Deferred Ideas

Report narrative and interpretation are deferred to Phase 22.

</deferred>
