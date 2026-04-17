# Phase 50: Arrhenius Exact Warm-Start Demo - Context

**Gathered:** 2026-04-17
**Status:** Ready for planning
**Mode:** Auto-selected defaults from `$gsd-autonomous`

<domain>
## Phase Boundary

Add `arrhenius` as a normalized, positive-domain scientific-law demo for `exp(-0.8 / x)`, prove strict compiler support with macro diagnostics, and produce reproducible compile/warm-start evidence that returns the same exact AST and verifier status `recovered`.

</domain>

<decisions>
## Implementation Decisions

### Demo Definition
- Use a dimensionless transformed input `x` rather than raw SI temperature, matching the FOR_DEMO warning to avoid unit-heavy scaling.
- Define the target as `exp(-0.8 / x)` with strictly positive train, held-out, and extrapolation domains safely away from zero.
- Keep the demo source linkage pointed to `sources/FOR_DEMO.md` Arrhenius law and mark it normalized/dimensionless.
- Add the demo through the existing `DemoSpec` registry so CLI, verifier, benchmark, and proof helpers can consume it consistently.

### Compiler and Warm-Start Evidence
- Treat Arrhenius as strict compile support, not a relaxed/stretch diagnostic.
- Require compiler metadata to include `direct_division_template` for the reciprocal-temperature exponent structure.
- Require zero-noise compiler warm-start to return the same exact AST and final verifier status `recovered`.
- Preserve the existing evidence taxonomy: same-AST warm-start return is not blind discovery.

### Artifacts and Tests
- Add focused dataset, compiler, CLI, and benchmark runner tests near the existing Beer-Lambert/Shockley warm-start coverage.
- Add a reproducible artifact/report path that records compile depth, macro hits, warm-start status, verifier status, and evidence regime.
- Keep Michaelis-Menten and Planck unsupported/stretch behavior unchanged while adding Arrhenius.
- Prefer small campaign/benchmark registry extensions over broad campaign reruns in this phase.

### the agent's Discretion
Use the existing compiler/warm-start CLI and benchmark machinery wherever possible. If an implementation choice can reuse a Beer-Lambert or Shockley pattern without weakening regime labels, reuse it rather than creating a new artifact format.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `DemoSpec` in `src/eml_symbolic_regression/datasets.py` already carries target functions, SymPy candidates, domains, provenance, and normalized flags.
- `compiler.py` already supports `direct_division_template` and records macro diagnostics.
- `tests/test_compiler_warm_start.py` has CLI warm-start promotion tests for Beer-Lambert and Shockley plus unsupported diagnostics for Michaelis-Menten and Planck.
- `tests/test_benchmark_runner.py` verifies Shockley warm-start artifacts with compile depth, macro hits, same-AST return, and recovered trained status.

### Established Patterns
- Compile-only, warm-start, same-AST return, verified-equivalent return, and unsupported regimes are recorded separately.
- Demo CLI JSON artifacts include `stage_statuses`, `claim_status`, `compiled_eml`, `warm_start_eml`, and verifier payloads.
- Benchmark suites add scientific-law rows through `BenchmarkCase` entries and focused runner tests.

### Integration Points
- `src/eml_symbolic_regression/datasets.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/cli.py`
- `tests/test_compiler_warm_start.py`
- `tests/test_benchmark_runner.py`
- `docs/IMPLEMENTATION.md`
- `README.md`

</code_context>

<specifics>
## Specific Ideas

Use domains such as train `(0.5, 3.0)`, held-out `(0.6, 2.7)`, and extrapolation `(3.1, 4.2)` so all splits remain positive and away from the singularity at zero. The expected source expression is `exp(-0.8/x)`, and the expected macro hit is `direct_division_template`.

</specifics>

<deferred>
## Deferred Ideas

Black-box neural-network extrapolation comparisons and raw-SI Arrhenius scaling are deferred. This phase proves the normalized exact warm-start path and records honest evidence regimes only.

</deferred>
