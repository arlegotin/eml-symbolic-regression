# Phase 27: Compiler Coverage and Depth Reduction - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase improves compiler coverage diagnostics and moves at least one v1.3 unsupported/depth-gated FOR_DEMO formula closer to verified EML coverage. It must preserve fail-closed behavior: unsupported formulas still return structured reasons and never invalid EML trees.

</domain>

<decisions>
## Implementation Decisions

### Coverage Target
- Target Shockley first because it has the recognizable form `scale * (exp(a) - 1)`, is currently depth-gated, and can be represented by a lower-depth EML template without special functions.
- Keep Michaelis-Menten, logistic, and Planck diagnostic-first if they still exceed depth gates.
- Explicitly defer damped oscillator `cos` support with structured diagnostics and tests instead of adding a risky trigonometric transform.

### Compiler Diagnostics
- Add diagnostics that expose strict unsupported reason plus relaxed compile depth, node count, rule trace, and validation result when available.
- Include compiler diagnostics in benchmark run artifacts when compile fails.
- Do not suppress exceptions in direct compiler APIs; fail-closed behavior remains the contract.

### the agent's Discretion
The exact diagnostics schema is at the agent's discretion, provided it is JSON-serializable and includes strict reason, relaxed metadata when available, and explicit unsupported details when unavailable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `compiler.py` already tracks rule traces and metadata for successful compilations.
- `UnsupportedExpression` already preserves structured reason/expression/detail.
- `benchmark._compile_demo` already converts unsupported compiler errors into run artifacts.

### Established Patterns
- Compiler validation compares exact EML output against ordinary SymPy evaluation before accepting compiled ASTs.
- Depth and node budgets are enforced after compilation.

### Integration Points
- Add a lower-depth template in `_Compiler.compile`.
- Add a public diagnostic helper in `compiler.py`.
- Add diagnostic payloads to `_compile_demo` unsupported outputs.
- Update tests for Shockley improvement and damped oscillator fail-closed diagnostics.

</code_context>

<specifics>
## Specific Ideas

For Shockley, compile `c*exp(a) - c` as `c * (exp(a) - 1)` using `eml(a, E)` for the `(exp(a) - 1)` part. This lowers the candidate from the previous depth-21 generic arithmetic path to a depth-13 validated EML AST. Raise the default compile depth gate to 13 so the lower-depth candidate passes while deeper formulas remain gated.

</specifics>

<deferred>
## Deferred Ideas

Support for trigonometric functions, broad rational simplification, and lower-depth templates for Planck/logistic/Michaelis-Menten remain deferred until the compiler diagnostics show the next highest-leverage transform.

</deferred>
