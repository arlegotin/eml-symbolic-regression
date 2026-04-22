# Phase 82: GEML Family Semantics and Structural Identity - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning
**Mode:** Autonomous smart discuss defaults

<domain>
## Phase Boundary

Phase 82 introduces exact fixed-parameter `GEML_a(x, y) = exp(a*x) - log(y)/a` semantics for explicit nonzero complex `a`, while keeping existing raw EML behavior as the default `a = 1` specialization. It must cover operator metadata, NumPy/PyTorch/mpmath evaluation, exact AST serialization, SymPy export, and identity tests/docs for `exp(a*GEML_a(u, v)) = exp(a*exp(a*u))/v`.

</domain>

<decisions>
## Implementation Decisions

### Operator Model
- Extend the existing `EmlOperator` value object instead of adding a parallel family abstraction.
- Preserve raw EML as the default and make `raw_eml` serialize as the named `a = 1` GEML specialization without changing legacy node kind `eml`.
- Add a named i*pi specialization with stable parse aliases such as `ipi_eml`, `i*pi`, and `geml:ipi`.
- Reject zero and non-finite GEML parameters at construction time.

### Evaluator Contract
- Implement canonical GEML as `exp(a*x) - log(y)/a` in NumPy, PyTorch, and mpmath-compatible exact AST evaluation.
- Reuse existing principal-log branch convention and anomaly counters for the second slot.
- Do not introduce branch-safety training guards in Phase 82; Phase 83 owns restricted branch contracts and diagnostics expansion.
- Preserve existing centered-family `CEML`/`ZEML` behavior unchanged.

### AST and Export
- Add an exact AST node for non-raw GEML specializations rather than overloading `CenteredEml`.
- Keep legacy raw `Eml` JSON artifacts round-trippable.
- Include `operator_family` metadata in `semantics_document()` for all family-aware nodes, including raw EML.
- Generate direct SymPy expressions using the GEML formula and exact-ish constants for `I*pi` where practical.

### Verification Scope
- Add focused tests for backend agreement, JSON round-trip, named-specialization parsing, SymPy export, and the structural identity.
- Use representative parameters `a = 1`, `a = 2`, and `a = i*pi` with safe nonzero second-slot inputs.
- Update documentation only where it clarifies the new family contract.
- Avoid empirical training integration in this phase; Phase 84 owns master-tree threading and snapping paths beyond basic expression support.

### the agent's Discretion
Naming details, helper placement, and exact test factoring are at the agent's discretion as long as they preserve existing raw and centered-family compatibility.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/semantics.py` already owns `EmlOperator`, PyTorch/NumPy evaluators, and anomaly counters.
- `src/eml_symbolic_regression/expression.py` already owns exact AST nodes, JSON export, SymPy export, and backend evaluation.
- `src/eml_symbolic_regression/master_tree.py` already selects `Eml` versus `CenteredEml` based on `operator_family.is_raw`.
- `tests/test_semantics_expression.py` is the focused place for semantic and AST round-trip tests.

### Established Patterns
- Operator metadata serializes through `EmlOperator.as_dict()` and parses through `eml_operator_from_spec()`.
- Raw EML artifacts use node kind `eml`; centered variants use node kind `centered_eml` with an `operator` object.
- Training-mode clamps are implemented only in torch evaluator functions and bypassed in faithful mode.

### Integration Points
- Public API exports in `src/eml_symbolic_regression/__init__.py` must include any new user-facing helpers.
- `SoftEMLTree._snap()` and expression embedding currently rely on `operator_family.is_raw`; later phases may need a richer predicate for GEML.
- Benchmark and optimizer configs already carry `operator_family` metadata, so new GEML operator parsing must not break existing centered-family suites.

</code_context>

<specifics>
## Specific Ideas

- Treat i*pi EML as a named fixed specialization, not learned continuous `a`.
- The structural identity is the core Phase 82 proof/test surface.
- Preserve all v1.14 claim-accounting behavior.

</specifics>

<deferred>
## Deferred Ideas

- Branch-cut proximity/crossing diagnostics and restricted i*pi theory identities belong to Phase 83.
- Master-tree training, snapping, exact-candidate pooling, cleanup, and refit integration belong to Phase 84.
- Oscillatory benchmarks, matched campaigns, and paper evidence packaging belong to Phases 85-87.

</deferred>
