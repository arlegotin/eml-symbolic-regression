# Phase 15: Benchmark Runner and Training Modes - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated autonomous context

<domain>
## Phase Boundary

Execute benchmark suites through existing demo, compile, blind optimizer, and compiler warm-start paths. Preserve unsupported and failed run outcomes as artifacts instead of aborting suite execution.

</domain>

<decisions>
## Implementation Decisions

### Runner Contract
- Add execution functions to the benchmark module rather than duplicating logic in the CLI.
- Keep per-run artifacts JSON-first with explicit schema, run identity, status, and nested stage payloads.
- Catch unsupported compiler and embedding cases as structured outcomes; reserve unexpected exceptions for `execution_error` artifacts.
- Add CLI commands to list and run benchmark suites.

### the agent's Discretion
- Use the existing optimizer and warm-start APIs directly.
- Keep filtering simple: formula, start mode, case ID, and seed filters are enough for v1.2.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `benchmark.py` already expands stable `BenchmarkRun` objects.
- `cli.run_demo` has the routing behavior to reuse for compile, blind, and warm-start runs.
- `datasets.DemoSpec.make_splits` provides train/heldout/extrapolation splits.

### Established Patterns
- CLI writes deterministic JSON through `_write_json`.
- Verifier status, not optimizer status, owns exact recovery.

### Integration Points
- Phase 17 aggregation should consume the run artifacts written here.

</code_context>

<specifics>
## Specific Ideas

Expose `run_benchmark_suite()` for tests and CLI use. CLI command should print a concise completed/failed count and write artifacts under the configured root.

</specifics>

<deferred>
## Deferred Ideas

Aggregate Markdown reports and richer evidence summaries belong to Phase 17.

</deferred>
