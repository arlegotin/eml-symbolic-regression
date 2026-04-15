# Phase 9: Constant Catalog and AST Embedding - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Make literal constants representable in soft EML terminal banks and embed compiled exact ASTs into compatible soft trees with snap-back validation.

</domain>

<decisions>
## Implementation Decisions

### Constants
- Preserve default pure `const:1` behavior.
- Add explicit finite literal constants only when requested or derived from compiled ASTs.
- Label literal constants as terminal-bank provenance.

### Embedding
- Map exact AST leaves to terminal labels and EML nodes to `child` choices.
- Fail before training for missing constants, missing variables, depth-too-small, or incompatible roots.
- Require immediate embed-to-snap equality.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SoftEMLTree.set_slot()` already biases logits toward discrete choices.

### Established Patterns
- Snap results and manifests are deterministic dictionaries.

### Integration Points
- Embedding is exposed through `SoftEMLTree.embed_expr()`.

</code_context>

<specifics>
## Specific Ideas

Use stable labels like `const:-0.8`, `const:0.5`, and `const:2`.

</specifics>

<deferred>
## Deferred Ideas

No shortest-form search or constant synthesis.

</deferred>
