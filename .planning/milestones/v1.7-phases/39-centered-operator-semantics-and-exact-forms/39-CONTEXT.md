# Phase 39: Centered Operator Semantics and Exact Forms - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-generated smart discuss context

<domain>
## Phase Boundary

Add first-class semantics and exact AST representation for raw EML, `cEML_{s,t}`, `CEML_s`, and `ZEML_s`. This phase stops at representing, evaluating, serializing, and verifying exact centered-family nodes; training and campaign matrix wiring are deferred to later v1.7 phases.

</domain>

<decisions>
## Implementation Decisions

### Operator Model
- Preserve `Eml` as the raw operator node for backward compatibility and add a separate centered-family exact node rather than changing all existing raw AST behavior.
- Represent operator-family metadata with a small immutable value object so source, manifests, and JSON artifacts can carry `family`, `s`, `t`, and terminal convention consistently.
- Keep centered-family exact candidates under the existing verifier-owned exact candidate contract; they remain exact symbolic candidates but are not reported as raw-EML-only claims.
- Keep `CEML_s` and `ZEML_s` explicit in names and JSON so the unit-terminal/formal successor path is not confused with the zero-terminal training-centered path.

### Numerical Semantics
- Use `expm1` and `log1p` in all centered-family NumPy, PyTorch, mpmath, and SymPy paths.
- Preserve the training-versus-verification split: training may clamp exp real inputs and record anomalies, while verification uses faithful centered semantics.
- Add shifted-singularity diagnostics in addition to the existing exp/log counters.
- Keep PyTorch evaluation at `complex128` by default.

### Compatibility
- Existing raw EML JSON, `expr_from_document`, tests, compiler identities, and `SoftEMLTree` defaults must remain compatible.
- Add new tests for centered numerical equivalence, AST round-trip, mpmath/SymPy export, and diagnostics without weakening existing test assertions.
- Avoid broad symbolic simplification; phase output should be deterministic representation and evaluation support.
- Do not introduce external dependencies.

### the agent's Discretion
All implementation details not described above are at the agent's discretion, guided by existing dataclass-based AST and semantics patterns.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/semantics.py` owns raw EML training/verification semantics and anomaly counters.
- `src/eml_symbolic_regression/expression.py` owns exact AST nodes, JSON serialization, SymPy export, NumPy/Torch/mpmath evaluation, and constant refit traversal.
- `src/eml_symbolic_regression/master_tree.py` snaps soft choices into `Eml` nodes and compares exact trees.
- `tests/test_semantics_expression.py` and `tests/test_master_tree.py` provide the nearest existing coverage patterns.

### Established Patterns
- Exact expressions are immutable dataclasses inheriting from `Expr`.
- JSON serialization uses stable dict payloads and `expr_from_document` validates `AST_SCHEMA`.
- Diagnostics accumulate into `AnomalyStats` with both aggregate fields and per-node `by_node` entries.
- Existing raw behavior favors additive extension over replacing archived contracts.

### Integration Points
- Centered-family semantics will be called from `CenteredEml.evaluate_*` immediately, and from `SoftEMLTree` in Phase 40.
- `expr_from_node` must understand new centered nodes while preserving raw `kind: eml`.
- `expressions_equal` must compare centered nodes for later embedding and recovery tests.

</code_context>

<specifics>
## Specific Ideas

Use the family

```math
cEML_{s,t}(x,y)=s\,expm1(x/s)-s\,log1p((y-t)/s)
```

with `CEML_s = cEML_{s,1}` and `ZEML_s = cEML_{s,0}`. Safe claims are local centering, normalized Jacobian, curvature control, shifted singularity, and subtraction limit; completeness claims are deferred.

</specifics>

<deferred>
## Deferred Ideas

- Soft master-tree family selection and continuation schedules are Phase 40.
- Operator-family proof/campaign presets are Phase 41.
- Comparative aggregate reports and regression locks are Phase 42.
- Paper decision memo and completeness boundary reporting are Phase 43.

</deferred>
