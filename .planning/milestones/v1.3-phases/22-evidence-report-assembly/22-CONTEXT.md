# Phase 22: Evidence Report Assembly - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated in autonomous execution

<domain>
## Phase Boundary

This phase assembles the generated campaign artifacts into a self-contained Markdown evidence report. It covers headline metrics, links to CSV/JSON/figure/raw artifacts, exact reproduction command, interpretation, limitations, and next experiments.

</domain>

<decisions>
## Implementation Decisions

### Report Shape
- Write `report.md` at the campaign root.
- Include a copy-paste reproduction command.
- Link generated figures and tables using campaign-relative paths.
- Include a failed/unsupported table with artifact links.

### Narrative Rules
- Explain warm-start evidence separately from blind recovery.
- Keep unsupported and failed cases visible.
- Avoid claiming general real-world symbolic-regression superiority.
- Convert measured limitations into concrete next experiments.

### the agent's Discretion
- Keep report prose concise and artifact-driven rather than decorative.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 20 provides headline metrics and failure rows.
- Phase 21 provides stable SVG figure paths.
- Campaign manifest already stores reproduction metadata.

### Established Patterns
- Reports are Markdown files checked into artifacts for human review.
- Aggregate evidence already uses verifier-owned recovery semantics.

### Integration Points
- `run_campaign` should write the report before the final manifest so the manifest can link it.

</code_context>

<specifics>
## Specific Ideas

The report should answer the user's practical question: what performed well, what failed, and what should be improved next.

</specifics>

<deferred>
## Deferred Ideas

Docs and committed smoke evidence are deferred to Phase 23.

</deferred>
