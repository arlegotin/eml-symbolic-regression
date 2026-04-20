# Phase 73: Basis-Only and Literal-Constants Benchmark Tracks - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning
**Mode:** Autonomous smart-discuss equivalent

<domain>
## Phase Boundary

Paper-faithful synthesis and applied literal-constant recovery must be separated in benchmark suites and reports. The repo already supports compiler `basis_only` versus `literal_constants` policies and optimizer literal terminal banks, but the benchmark suite/run/aggregate schema does not expose an explicit track denominator.

</domain>

<decisions>
## Implementation Decisions

### Track Contract

Use an explicit benchmark-track field rather than inferring claims from `optimizer.constants`. Track data should travel through case expansion, run artifacts, aggregate summaries, markdown reports, and campaign presets.

### Track Names

Use two stable track IDs:

- `basis_only`: paper-faithful `{1, eml, variables}` track with compiler `basis_only` policy and no non-1 literal terminal constants.
- `literal_constants`: applied convenience track with compiler `literal_constants` policy and a declared literal catalog.

### Denominators

Aggregates must count recovery rates by track, not just by formula or start mode. Mixed-track suites are allowed only when aggregate outputs still expose separate per-track totals.

### Runtime Scope

Phase 73 should add track infrastructure, built-in suite definitions, focused tests, and docs. It should not run a full publication campaign; Phase 76 owns full evidence regeneration.

</decisions>

<code_context>
## Existing Code Insights

- `src/eml_symbolic_regression/benchmark.py` defines `BenchmarkCase`, `BenchmarkRun`, built-in suites, execution, aggregate JSON/Markdown, and suite run IDs.
- `OptimizerBudget.constants` already serializes terminal constants and participates in run IDs.
- `_compile_demo()` currently hardcodes compiler `constant_policy="literal_constants"`, so basis-only compile rows cannot fail closed under the paper-faithful policy yet.
- Aggregate reports currently group by formula, start mode, evidence class, return kind, raw status, repair status, perturbation, depth, and seed group, but not by track or constants policy.
- `src/eml_symbolic_regression/campaign.py` maps named campaign presets to built-in benchmark suites and can add a v1.13 track preset without changing CLI shape.
- `docs/IMPLEMENTATION.md` already warns that `literal_constants` is not pure `{1, eml}` synthesis; Phase 73 should make that contract machine-readable.

</code_context>

<specifics>
## Specific Ideas

- Add benchmark track metadata to case/run serialization.
- Add built-in v1.13 suites for basis-only, literal-constants, and combined paper-track denominators.
- Make `_compile_demo()` use the run's track constant policy.
- Add aggregate `tracks` summary and `benchmark_track`/`constants_policy` groups.
- Add tests that every publication target has both tracks and that aggregates keep totals separate.

</specifics>

<deferred>
## Deferred Ideas

- Full v1.13 evidence execution and claim audit remain Phase 76.
- Baseline comparators remain Phase 75.
- Expanded datasets remain Phase 74.

</deferred>
