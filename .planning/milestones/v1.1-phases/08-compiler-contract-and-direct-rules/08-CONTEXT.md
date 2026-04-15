# Phase 8: Compiler Contract and Direct Rules - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Create a fail-closed SymPy subset compiler that emits the existing exact EML `Expr` AST, structured metadata, and independent validation evidence.

</domain>

<decisions>
## Implementation Decisions

### Compiler Contract
- Compiler output must be `Const`, `Var`, and `Eml`, not a parallel AST.
- Unsupported expressions must raise stable machine-readable reason codes.
- Compile-only verification is a seed/provenance stage, not a trained recovery claim.
- Metadata must include source, normalized expression, variables, constants, assumptions, trace, depth, and node count.

### the agent's Discretion
Use conservative SymPy handling and fail closed whenever a rule is not explicitly implemented.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `expression.py` already owns exact EML ASTs and deterministic JSON.
- `verify.py` owns recovered versus showcase status.

### Established Patterns
- Verifier-owned statuses remain separate from optimizer or compiler output.

### Integration Points
- New compiler code integrates with CLI demo reports and later warm-start embedding.

</code_context>

<specifics>
## Specific Ideas

Support constants, variables, `exp`, and `log` immediately; arithmetic can use the same rule layer in the next phase.

</specifics>

<deferred>
## Deferred Ideas

Pure `{1, eml}` synthesis for arbitrary numeric constants is deferred.

</deferred>
