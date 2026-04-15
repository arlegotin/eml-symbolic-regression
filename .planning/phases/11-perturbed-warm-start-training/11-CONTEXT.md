# Phase 11: Perturbed Warm-Start Training - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Train from compiled EML embeddings through the existing optimizer and record perturbation, optimizer, snap, and verification evidence.

</domain>

<decisions>
## Implementation Decisions

### Warm Start
- Warm starts are optimizer initializers, not a separate optimizer.
- The optimizer cannot label candidates as recovered.
- Perturbation is deterministic and recorded per restart.
- Post-snap verifier status determines recovery.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `fit_eml_tree()` already returns optimizer and snap manifests.

### Established Patterns
- Verification is separate from training loss.

### Integration Points
- New warm-start wrapper calls `fit_eml_tree()` with an initializer.

</code_context>

<specifics>
## Specific Ideas

Classify outcomes as same-AST return, verified-equivalent AST, snapped-but-failed, soft-fit-only, or failed.

</specifics>

<deferred>
## Deferred Ideas

Learned coefficients and blind deep recovery improvements.

</deferred>
