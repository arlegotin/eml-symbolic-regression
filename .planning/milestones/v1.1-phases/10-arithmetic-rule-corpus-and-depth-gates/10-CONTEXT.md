# Phase 10: Arithmetic Rule Corpus and Depth Gates - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Add verified EML templates for the arithmetic needed by v1.1 demos, with max-power, depth, and node gates.

</domain>

<decisions>
## Implementation Decisions

### Arithmetic Rules
- Arithmetic must live in the compiler rule layer.
- Each enabled rule must validate numerically against independent SymPy evaluation.
- Integer powers are capped by `max_power`.
- Depth and node count gates remain hard failures.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Compiler metadata already records rule traces and assumptions.

### Established Patterns
- Fail closed instead of producing partial unsupported trees.

### Integration Points
- Demo compiler stages use default gates to keep larger formulas honest.

</code_context>

<specifics>
## Specific Ideas

Beer-Lambert should pass default gates; Michaelis-Menten and Planck may compile only under larger explicit budgets.

</specifics>

<deferred>
## Deferred Ideas

Trigonometric identities and shortest EML minimization.

</deferred>
