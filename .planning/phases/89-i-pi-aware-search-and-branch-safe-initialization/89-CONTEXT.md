# Phase 89: i*pi-Aware Search and Branch-Safe Initialization - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Improve i*pi/GEML search enough to create better exact-candidate opportunities without embedding exact target formulas. This phase adds generic initializer/prior mechanisms and v1.16 benchmark contracts; it does not relax verifier semantics.

</domain>

<decisions>
## Implementation Decisions

### Initializer Discipline
- Initializers must be generic operator-family primitives, not formula-name branches or exact target trees.
- i*pi-specific initializers should be recorded separately from raw EML scaffold provenance.
- Manifests must expose initializer names, strategy, and embedding details for claim audits.
- Existing raw EML scaffold behavior must remain unchanged.

### Branch Safety
- i*pi rows should use branch diagnostics and training-mode guards already present in the semantics layer.
- Faithful verification remains unchanged and owns exact recovery.
- Branch-related suite tags must remain required for i*pi rows.
- Budget/schedule changes should be opt-in through v1.16 suites and presets.

### the agent's Discretion
Use the smallest additive changes to `optimize.py`, `benchmark.py`, and tests so older v1.15 suites still pass.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SoftEMLTree.embed_expr` can embed same-family exact GEML expressions without special slot code.
- `fit_eml_tree` already accepts an external initializer and records per-attempt initialization logs.
- `BenchmarkCase` and `OptimizerBudget` already serialize optimizer budgets into stable manifests.

### Established Patterns
- Raw scaffold initializers are controlled by `scaffold_initializers` and same-family witness checks.
- i*pi branch-safe tags are validated in benchmark suite construction.
- Candidate pools and hardening checkpoints already feed verifier-owned selection.

### Integration Points
- Add `phase_initializers` as a separate budget/config field so raw scaffold contracts are not overloaded.
- Register v1.16 suites/presets without changing v1.15 IDs.

</code_context>

<specifics>
## Specific Ideas

Add `ipi_phase_unit` and `ipi_log_unit` generic initializers that embed shallow i*pi primitive trees like `ipi_eml(x, 1)` and `ipi_eml(1, x)`.

</specifics>

<deferred>
## Deferred Ideas

Learning continuous `a` values remains future work.

</deferred>
