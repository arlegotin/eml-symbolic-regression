# Phase 18: Smoke Tests, Docs, and Evidence Lockdown - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated autonomous context

<domain>
## Phase Boundary

Lock the benchmark contract with focused tests and documentation. This phase verifies the full smoke path and explains how users should interpret benchmark evidence.

</domain>

<decisions>
## Implementation Decisions

### Lockdown
- Keep smoke tests small enough for normal pytest runs.
- Explicitly test the combined smoke path: blind run, warm-start run, unsupported/stretch run, and aggregate report.
- Document same-AST warm-start return separately from discovery.
- Document failed and unsupported cases as first-class evidence.

### the agent's Discretion
- Update README and implementation docs without changing public recovery claims.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `smoke` built-in suite already contains blind, warm-start, and unsupported diagnostic cases.
- `write_aggregate_reports()` writes both JSON and Markdown reports.

### Established Patterns
- README contains user-facing CLI examples.
- `docs/IMPLEMENTATION.md` contains contract-level implementation details and limitations.

### Integration Points
- Final verification should run full pytest.

</code_context>

<specifics>
## Specific Ideas

Add one explicit smoke test for the whole benchmark evidence path so later refactors cannot accidentally remove a run mode or aggregate artifact.

</specifics>

<deferred>
## Deferred Ideas

Optimizer improvements and long benchmark campaigns belong to future milestones.

</deferred>
