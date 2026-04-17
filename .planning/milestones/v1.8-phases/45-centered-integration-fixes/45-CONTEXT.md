# Phase 45: Centered Integration Fixes - Context

**Gathered:** 2026-04-17
**Status:** Ready for planning
**Mode:** Auto-selected defaults from `$gsd-autonomous`

<domain>
## Phase Boundary

Make centered-family integration paths either real or explicitly fail-closed with stable metadata, especially warm-start, compiler-seed embedding, scaffolds, continuation schedules, repair, and refit.

</domain>

<decisions>
## Implementation Decisions

### Fail-Closed Semantics
- Do not silently embed raw EML compiler seeds into centered-family trees.
- Centered warm-start and perturbed-tree modes remain unsupported unless a same-family exact seed exists.
- Unsupported rows must keep operator family, schedule, and reason metadata visible in artifacts and aggregate tables.
- Missing support remains denominator-visible rather than hidden by filters.

### Training Metadata
- Record scaffold exclusions in benchmark budgets when centered families drop raw-only scaffolds.
- Record continuation schedule traces in optimizer manifests.
- Preserve centered operator family in repair and refit candidate paths.
- Add regression tests around unsupported reasons and schedule/scaffold metadata.

### the agent's Discretion
Use the smallest code changes that make artifact semantics explicit without pretending centered exact seeds exist.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SoftEMLTree.embed_expr` already rejects operator-family mismatches.
- Benchmark warm-start and perturbed-tree paths already fail closed for centered variants.
- Optimizer manifests already include operator-family and operator-schedule config.

### Established Patterns
- Unsupported benchmark rows include structured payloads and are summarized through aggregate metrics.
- Tests prefer targeted contract checks around artifact payload shape.

### Integration Points
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/optimize.py`
- `tests/test_benchmark_runner.py`
- `tests/test_optimizer_cleanup.py`

</code_context>

<specifics>
## Specific Ideas

Keep raw EML defaults unchanged. Centered-family fixes must improve observability and safety before enabling any centered warm-start behavior.

</specifics>

<deferred>
## Deferred Ideas

Constructive centered-family compiler witnesses are deferred until a later completeness/search phase.

</deferred>
