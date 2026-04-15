# Phase 17: Evidence Aggregation and Report Contracts - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated autonomous context

<domain>
## Phase Boundary

Aggregate benchmark run artifacts into evidence reports. This phase adds normalized per-run metrics, aggregate JSON, aggregate Markdown, recovery/failure taxonomy, and provenance fields.

</domain>

<decisions>
## Implementation Decisions

### Evidence Contract
- Add top-level metrics to each run artifact while keeping the nested optimizer/warm-start manifests intact.
- Group aggregate evidence by formula, start mode, perturbation level, depth, and seed group.
- Count verifier-owned recovery separately from same-AST warm-start return.
- Preserve suite config, code version, environment summary, and artifact paths in aggregate reports.

### the agent's Discretion
- Keep Markdown reports compact and table-oriented.
- Avoid visualization dependencies.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `BenchmarkSuiteResult` already collects run results and suite config.
- Run artifacts already include `run`, `status`, `stage_statuses`, and environment fields.

### Established Patterns
- JSON schemas use explicit `schema` fields.
- Reports are deterministic and sorted where practical.

### Integration Points
- CLI benchmark command should write `aggregate.json` and `aggregate.md` alongside `suite-result.json`.
- Phase 18 docs should explain the taxonomy introduced here.

</code_context>

<specifics>
## Specific Ideas

Use `claim_status == "recovered"` for verifier-owned recovery rate. Treat `same_ast_return` as a separate warm-start stability class rather than discovery.

</specifics>

<deferred>
## Deferred Ideas

Charts, dashboards, and distributed result comparison remain future work.

</deferred>
