---
phase: 37-compiler-macro-shortening-and-warm-start-coverage
plan: 01
subsystem: compiler
tags: [compiler, macros, diagnostics, warm-start, benchmark]
requires:
  - phase: 34
    provides: "Fallback-safe exact candidate and benchmark artifact handling"
  - phase: 36
    provides: "Post-snap refit artifacts and stronger numerical diagnostics"
provides:
  - "Explicit macro-aware compiler diagnostics with audited hit/miss metadata"
  - "Direct-division shortening for true numerator-over-denominator motifs"
  - "Expanded Shockley warm-start coverage in CLI and standard benchmark suites"
affects: [phase-38, compiler-diagnostics, benchmark-suites]
tech-stack:
  added: []
  patterns: ["Macro hit/miss reporting against a no-macro baseline", "Fail-closed warm-start coverage expansion only after validated exact compile paths"]
key-files:
  created:
    - .planning/phases/37-compiler-macro-shortening-and-warm-start-coverage/37-01-SUMMARY.md
    - .planning/phases/37-compiler-macro-shortening-and-warm-start-coverage/37-VERIFICATION.md
  modified:
    - src/eml_symbolic_regression/compiler.py
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/cli.py
    - docs/IMPLEMENTATION.md
    - tests/test_compiler_warm_start.py
    - tests/test_benchmark_runner.py
    - tests/test_campaign.py
key-decisions:
  - "Direct-division only fires for explicit `Mul(..., Pow(denominator, -1))` shapes so the macro remains a real shortening path instead of rewriting generic reciprocal or rationalized-coefficient expressions."
  - "Unsupported compiler paths in the CLI now preserve the same relaxed diagnostic payload used by benchmark artifacts."
  - "Standard and showcase benchmark suites promote Shockley from compile-only diagnostics to warm-start coverage, while Michaelis-Menten and Planck remain diagnostic-only at the shipped compile gate."
patterns-established:
  - "Compiler macros are first-class, traceable rules with baseline depth/node comparisons instead of hidden special cases."
  - "Warm-start coverage expansion is gated by validated exact compile paths and preserved fail-closed behavior, not by relaxed diagnostics alone."
requirements-completed: [COMP-01, COMP-02, COMP-03]
duration: not tracked
completed: 2026-04-16
---

# Phase 37 Plan 01: Compiler Macro Shortening and Warm-Start Coverage Summary

**Macro-aware compiler shortcuts, audited diagnostics, and conservative warm-start coverage expansion**

## Performance

- **Duration:** not tracked
- **Completed:** 2026-04-16T11:58:05Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Turned the compiler shortcut path into an explicit macro layer, surfaced `hits`, `misses`, and no-macro baseline depth/node deltas, and kept unsupported cases fail-closed.
- Added a direct-division macro for true numerator-over-denominator motifs, while avoiding accidental macro hits on reciprocal-only or rationalized-coefficient expressions.
- Expanded shipped warm-start coverage to Shockley through the shorter exact tree path, aligned CLI unsupported diagnostics with benchmark artifacts, and moved the standard benchmark matrix to exercise the recovered warm-start path directly.

## Files Created/Modified

- `src/eml_symbolic_regression/compiler.py` - macro-aware shortcut layer, direct-division lowering, and macro diagnostic metadata.
- `src/eml_symbolic_regression/benchmark.py` - updated warm-start defaults and standard/showcase Shockley warm-start benchmark coverage.
- `src/eml_symbolic_regression/cli.py` - unsupported compiler diagnostics now include the relaxed diagnostic payload.
- `docs/IMPLEMENTATION.md` - documented macro diagnostics, Shockley warm-start coverage, and still-gated formulas.
- `tests/test_compiler_warm_start.py` - regression coverage for Shockley macro deltas, Michaelis direct-division diagnostics, Planck composed macro diagnostics, and CLI warm-start behavior.
- `tests/test_benchmark_runner.py` - standard benchmark regression for recovered Shockley warm-start artifacts.
- `tests/test_campaign.py` - preset-level coverage lock for the new Shockley warm-start case in the standard suite.

## Decisions Made

- Restricted the direct-division macro to explicit `Pow(denominator, -1)` factors so macro hits represent real structural shortening instead of generic algebraic normalization artifacts.
- Preserved the shipped compile gate at depth 13, which keeps Michaelis-Menten and Planck as honest diagnostic-only cases even though relaxed diagnostics now show their macro-shortened exact trees.
- Treated CLI compile failures and benchmark compile failures as the same diagnostic contract by attaching relaxed compiler diagnostics in both places.

## Deviations from Plan

- The final benchmark-coverage change was narrower than the broadest interpretation of the plan: Shockley moved into standard/showcase warm-start coverage, while Michaelis-Menten remained diagnostic-only because the validated shortened exact tree still sits above the shipped compile gate.

## Issues Encountered

- A first pass at direct-division used `sympy.together()` and accidentally reported macro hits on rationalized coefficients and reciprocal-only shapes. Rewriting the matcher to inspect actual `Mul(..., Pow(den, -1))` structure fixed that and restored honest macro diagnostics.
- The CLI initially dropped relaxed compiler diagnostics on unsupported compile paths, which made its output weaker than benchmark artifacts. Wiring `diagnose_compile_expression()` into the CLI unsupported payload resolved that inconsistency.

## User Setup Required

None.

## Next Phase Readiness

Phase 38 can now compare the hybrid pipeline against archived baselines with cleaner regime separation: compiler shortcuts are audited, supported warm-start coverage is explicit, and unsupported formulas still carry honest relaxed diagnostics instead of silent depth failures.

---
*Phase: 37-compiler-macro-shortening-and-warm-start-coverage*
*Completed: 2026-04-16*
