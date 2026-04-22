# Phase 84: Family-Aware Training and Snapping Integration - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning
**Mode:** Autonomous smart discuss defaults

<domain>
## Phase Boundary

Phase 84 threads fixed GEML specializations, especially i*pi EML, through the existing differentiable master-tree optimization, snapping, exact-candidate pool, cleanup/refit metadata, and regression tests without allowing raw-family scaffold witnesses to count as i*pi evidence.

</domain>

<decisions>
## Implementation Decisions

### Integration Scope
- Keep raw EML as the default optimizer behavior.
- Treat i*pi EML as a fixed operator family selected by `operator_family`, not as a learned continuous parameter.
- Use random initialization for i*pi EML unless same-family witnesses are explicitly added later.
- Preserve fail-closed scaffold exclusions for non-raw families.

### Artifact Metrics
- Add explicit candidate `pre_snap_mse` and `post_snap_mse` aliases.
- Add gradient norm metrics to training trace rows.
- Add wall-clock timing metadata to the run manifest.
- Carry branch diagnostics from Phase 83 into trace summaries, semantics alignment, and verifier evidence.

### Regression Boundary
- Add focused i*pi optimizer smoke tests instead of expensive campaign training.
- Keep raw and centered-family optimizer tests passing unchanged.
- Do not claim i*pi recovery quality in this phase; this phase proves plumbing and artifact integrity.

### the agent's Discretion
Exact metric field names and summary placement are at the agent's discretion, provided existing manifest keys remain compatible.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SoftEMLTree` already accepts an `operator_family`; Phase 82 added `Geml` snapping and embedding support.
- `TrainingConfig.operator_family` and `operator_schedule` already serialize family metadata.
- `fit_eml_tree()` already emits candidate pools, selected/fallback manifests, trace rows, and semantics alignment payloads.

### Established Patterns
- Non-raw operator families fail closed for paper scaffold initializers unless same-family witnesses are registered.
- Candidate ranking is verifier-owned when verification splits are supplied.
- Manifest fields are additive to preserve benchmark compatibility.

### Integration Points
- `optimize.py` trace rows and manifest summaries need the new Phase 83 branch fields.
- `tests/test_optimizer_cleanup.py` is the focused optimizer integration suite.

</code_context>

<specifics>
## Specific Ideas

- Use a small depth-1 i*pi smoke fit against `exp(i*pi*x)` to verify snapping and artifact metadata.
- Assert scaffold exclusions are present so raw witnesses cannot silently contaminate i*pi runs.

</specifics>

<deferred>
## Deferred Ideas

- Benchmark suite registration belongs to Phase 85.
- Matched campaign aggregation belongs to Phase 86.
- Paper-claim classification belongs to Phase 87.

</deferred>
