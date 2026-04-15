# Phase 14: Benchmark Contract and Suite Registry - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated autonomous context

<domain>
## Phase Boundary

Define deterministic benchmark suite contracts before training execution exists. This phase delivers data structures, built-in suite registry, validation, run expansion, and stable artifact identity. It does not need to run training yet.

</domain>

<decisions>
## Implementation Decisions

### the agent's Discretion
- Use standard library JSON and dataclasses; do not add dependencies.
- Reuse `datasets.demo_specs()` formula IDs as the source of valid benchmark formulas.
- Represent start modes explicitly so later phases can route to blind training, compiler warm starts, compile-only diagnostics, or catalog verification.
- Generate stable run IDs from suite/case/formula/start/seed/perturbation inputs instead of depending on list position.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `datasets.py` owns built-in demo formulas and split generation.
- `optimize.TrainingConfig` owns optimizer budget fields.
- `compiler.CompilerConfig` and `warm_start.PerturbationConfig` define warm-start-related budgets.

### Established Patterns
- Reports use deterministic JSON with explicit `schema` fields.
- CLI commands are implemented in `cli.py` with argparse subcommands.
- Tests prefer direct module assertions plus subprocess CLI smoke tests.

### Integration Points
- Phase 15 should route expanded benchmark runs into `fit_eml_tree`, `compile_and_validate`, and `fit_warm_started_eml_tree`.
- Phase 17 should aggregate run artifacts using stable run IDs and schema fields introduced here.

</code_context>

<specifics>
## Specific Ideas

Implement this as `src/eml_symbolic_regression/benchmark.py` and export the public contract from `__init__.py` only if needed.

</specifics>

<deferred>
## Deferred Ideas

Training execution, formula matrix tuning, aggregation, docs, and smoke commands belong to later v1.2 phases.

</deferred>
