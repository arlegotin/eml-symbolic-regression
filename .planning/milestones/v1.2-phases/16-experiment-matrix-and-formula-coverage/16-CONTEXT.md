# Phase 16: Experiment Matrix and Formula Coverage - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated autonomous context

<domain>
## Phase Boundary

Populate the v1.2 benchmark matrix with meaningful formula coverage. This phase updates built-in suites and demo specs; it does not add aggregation or documentation yet.

</domain>

<decisions>
## Implementation Decisions

### Matrix Coverage
- Add `radioactive_decay` as a named demo target so the blind baseline matrix covers a FOR_DEMO-style exponential decay target beyond raw `exp` and `log`.
- Keep Beer-Lambert perturbation levels at `0.0`, `5.0`, and `35.0` to encode same-basin, mild, and slot-changing stress.
- Represent Michaelis-Menten and Planck as warm/compile diagnostics that record gate outcomes honestly.
- Include selected FOR_DEMO formulas in diagnostics even when unsupported by the compiler.

### the agent's Discretion
- Do not tune optimizer behavior in this phase; measureable matrix design comes first.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `datasets.demo_specs()` is the single registry of formula IDs accepted by benchmark validation.
- `benchmark.builtin_suite()` owns matrix composition.

### Established Patterns
- Unsupported compiler cases are valid evidence outcomes.

### Integration Points
- Phase 17 aggregation should treat matrix tags and start modes as grouping dimensions.

</code_context>

<specifics>
## Specific Ideas

Add tests that inspect suite expansion and run a small diagnostic subset to prove the matrix is executable without running the full long suite.

</specifics>

<deferred>
## Deferred Ideas

Optimizer robustness improvements and depth reduction remain future work after v1.2 evidence is collected.

</deferred>
