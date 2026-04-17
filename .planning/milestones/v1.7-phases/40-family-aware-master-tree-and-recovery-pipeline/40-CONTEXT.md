# Phase 40: Family-Aware Master Tree and Recovery Pipeline - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-generated smart discuss context

<domain>
## Phase Boundary

Thread operator-family selection through the differentiable soft tree, optimizer config, snapping, exact-candidate ranking, warm-start/perturbed-tree embedding, and benchmark budget metadata. This phase provides executable fixed-family and scheduled-family training plumbing; campaign matrices and comparative reports are deferred to Phases 41 and 42.

</domain>

<decisions>
## Implementation Decisions

### Family Selection
- Keep raw EML as the default everywhere.
- Use a fixed operator family per `SoftEMLTree` and `TrainingConfig` run.
- Support simple continuation schedules as explicit metadata and per-attempt family selection, not as a new learnable per-node parameter system.
- Limit schedule syntax to named operator specifications that can be serialized deterministically.

### Recovery Pipeline
- Snap centered trees into `CenteredEml` nodes and raw trees into existing `Eml` nodes.
- Preserve candidate-pool ranking, fallback, cleanup, repair, and refit semantics; only the exact expression type changes.
- Warm-start and perturbed-tree embedding should work when the target expression has the same operator family as the tree; mismatches must fail closed with diagnostics.
- Compiler support for centered trees is opt-in; existing raw compiler output remains raw and unchanged.

### Benchmark Contract
- Add operator-family and schedule fields to optimizer budgets and run IDs so raw-vs-centered artifacts do not collide.
- Preserve old suite JSON compatibility by defaulting absent family fields to raw EML.
- Expose family metadata in run payloads and aggregate metrics.
- Add focused tests instead of running expensive full campaigns in this phase.

### the agent's Discretion
Implementation details are at the agent's discretion as long as raw defaults remain compatible and artifacts make the operator family auditable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SoftEMLTree` owns complete tree construction, snapping, slot catalogs, exact embedding, and replay.
- `TrainingConfig` and `fit_eml_tree` own optimizer budgets, hardening checkpoints, candidate manifests, and exact ranking.
- `OptimizerBudget`, `BenchmarkRun`, and `BenchmarkCase` own benchmark config parsing and stable run IDs.
- `warm_start.py` and `basin.py` already route exact embeddings into `fit_eml_tree`.

### Established Patterns
- New config fields should default to raw behavior.
- Artifact payloads prefer explicit schema and deterministic dictionaries.
- Fail-closed diagnostics are preferred over silently coercing unsupported exact trees.

### Integration Points
- `_SoftNode._snap` is the key place that decides raw `Eml` versus centered `CenteredEml`.
- `SoftEMLTree.__init__`, `fit_eml_tree`, and `_training_config_from_budget` must accept operator-family config.
- Benchmark run IDs must include family metadata to avoid artifact collisions.

</code_context>

<specifics>
## Specific Ideas

Fixed-family variants should include raw EML plus declared `CEML_s` and `ZEML_s` values. Continuation schedules should preserve metadata for schedules like `8 -> 4 -> 2 -> 1` and `8 -> 4`, even if the first implementation applies them at attempt boundaries rather than mid-optimizer step.

</specifics>

<deferred>
## Deferred Ideas

- Built-in campaign matrices are Phase 41.
- Aggregate family-comparison tables and figures are Phase 42.
- Paper claim wording and completeness-search boundary reporting are Phase 43.

</deferred>
