status: passed

# Phase 9 Verification

Default parameter-count behavior remains valid for pure `const:1`; literal constants are visible in slot catalogs; compiled ASTs embed and snap back; missing constants fail before training.

| Requirement | Status | Evidence |
|-------------|--------|----------|
| CONST-01 | passed | `SoftEMLTree` defaults to `(1,)` and accepts literal constant catalogs. |
| CONST-02 | passed | Compiled constants feed terminal labels such as `const:-0.8`. |
| EMBED-01 | passed | `embed_expr_into_tree()` maps AST nodes to slot logits. |
| EMBED-02 | passed | `EmbeddingResult` includes snap round-trip equality. |
| EMBED-03 | passed | `EmbeddingError` reports missing constant, missing variable, depth, and incompatible tree failures. |
