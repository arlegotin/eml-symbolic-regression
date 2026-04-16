# Phase 37: Compiler Macro Shortening and Warm-Start Coverage - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, compiler diagnostics, phase 36 outputs, and current warm-start gates

<domain>
## Phase Boundary

Phase 37 should formalize the compiler's shortcut layer instead of leaving it as one ad hoc special case. The goal is to keep the compiler fail-closed while making macro hits and misses visible, measuring macro depth/node wins against the old generic expansion, and expanding warm-start coverage only where the shortened exact tree is actually validated.

The safest immediate coverage target is shockley because it already compiles exactly through the existing `scaled_exp_minus_one_template` at depth 13 and returns `same_ast_return` under warm-start training when the warm-depth gate allows it. A direct division shortcut can also shorten Michaelis-Menten-style rational forms from the current generic expansion, but unsupported cases such as logistic, Planck, and damped oscillator must remain honestly gated if they still exceed depth or use unsupported operators.

</domain>

<decisions>
## Implementation Decisions

- **D-01:** Introduce an explicit macro layer in `compiler.py` with macro diagnostics instead of relying on hidden special cases.
- **D-02:** Add one new low-risk arithmetic macro only: direct division lowering for `Mul(..., Pow(denominator, -1))`, reusing the existing exact `divide_expr()` identity rather than inventing new semantics.
- **D-03:** Keep `scaled_exp_minus_one_template` as the existing macro baseline and report macro hits/misses plus depth/node delta against a no-macro compile path.
- **D-04:** Expand warm-start depth gates only enough to admit newly validated macro-shortened formulas; do not promise new support for logistic, Planck, or trigonometric formulas.
- **D-05:** Lock coverage with tests around canonical low-depth identities (`log`) and selected arithmetic motifs (Shockley macro, Michaelis-style direct division), while preserving fail-closed diagnostics for unsupported cases.

</decisions>

<specifics>
## Specific Ideas

- Add `enable_macros` and macro diagnostics to compiler config/metadata so diagnostics can compare the macro path against the old generic path.
- Surface `hits`, `misses`, `baseline_depth`, `baseline_node_count`, `depth_delta`, and `node_delta` in compiler metadata and `diagnose_compile_expression()`.
- Raise default warm-start gates just enough for validated macro-shortened coverage, likely to depth 14 so Michaelis-style direct division can warm-start if the compiled tree is still exact and verified.
- Update CLI and benchmark defaults/tests so Shockley and possibly Michaelis move from depth-gated diagnostics into verified warm-start coverage, while logistic and Planck remain diagnostic-only.

</specifics>

<canonical_refs>
## Canonical References

- `.planning/REQUIREMENTS.md` - COMP-01, COMP-02, COMP-03.
- `.planning/ROADMAP.md` - Phase 37 goal and success criteria.
- `.planning/STATE.md` - Phase 36 completion and weak-dominance direction.
- `.planning/phases/36-post-snap-constant-refit-and-numerical-stability/36-01-SUMMARY.md`
- `.planning/phases/36-post-snap-constant-refit-and-numerical-stability/36-VERIFICATION.md`
- `src/eml_symbolic_regression/compiler.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/cli.py`
- `src/eml_symbolic_regression/warm_start.py`
- `tests/test_compiler_warm_start.py`
- `tests/test_benchmark_runner.py`

</canonical_refs>

<code_context>
## Existing Code Insights

- The compiler already has one shortcut, `scaled_exp_minus_one_template`, but no macro registry or macro diagnostics.
- Warm-start depth gating happens in `cli.py` and `benchmark.py`, not in `warm_start.py`.
- Shockley already compiles at depth 13 with the existing shortcut and warm-starts cleanly when the gate allows it.
- Michaelis-Menten currently compiles too deep through the generic multiplication plus reciprocal path, but a direct division shortcut reduces the exact tree materially while keeping the same exact arithmetic identity.

</code_context>

<deferred>
## Deferred Ideas

- Logistic and Planck remain diagnostic-first if the new direct division shortcut still leaves them above the warm-start gate.
- Damped oscillator remains unsupported until trigonometric support is added in a later phase.

</deferred>

---

*Phase: 37-compiler-macro-shortening-and-warm-start-coverage*
*Context gathered: 2026-04-16*
