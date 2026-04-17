---
phase: 51-reciprocal-and-saturation-compiler-motifs
plan: 01
subsystem: compiler
tags: [sympy, eml, warm-start, cli, pytest]

requires:
  - phase: 50-arrhenius-exact-warm-start-demo
    provides: Arrhenius direct-division same-AST warm-start baseline and Planck stretch guard
provides:
  - reusable reciprocal_shift_template structural compiler macro
  - reusable saturation_ratio_template structural compiler macro
  - Michaelis-Menten strict compile and same-AST warm-start evidence
affects: [compiler, warm-start, michaelis_menten, phase-52, phase-53]

tech-stack:
  added: []
  patterns:
    - structural SymPy macro matching without formula ids
    - validation-gated EML shortening behind strict compile gates

key-files:
  created:
    - .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-01-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/compiler.py
    - tests/test_compiler_warm_start.py

key-decisions:
  - "Reciprocal and saturation motifs match direct SymPy structure only; no demo-name or string hardcoding was added."
  - "Michaelis-Menten is promoted only as compiled same-AST warm-start evidence, not blind discovery."
  - "Arrhenius remains on direct_division_template and Planck remains stretch/unsupported under warm-start promotion."

patterns-established:
  - "Unit-shift builder: x+b is lowered as eml(log(x), exp(-b)) and accepted only after validation."
  - "Top-level saturation ratios c*x/(x+b) record saturation_ratio_template instead of nested reciprocal or direct-division hits."

requirements-completed: [MIC-01, MIC-02, MIC-03, MIC-04]

duration: 8min
completed: 2026-04-17
---

# Phase 51 Plan 01: Reciprocal and Saturation Compiler Motifs Summary

**Structural reciprocal-shift and saturation-ratio EML compiler macros with Michaelis-Menten same-AST warm-start recovery**

## Performance

- **Duration:** 8 min
- **Started:** 2026-04-17T13:45:52Z
- **Completed:** 2026-04-17T13:53:18Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Added `reciprocal_shift_template` for strict `1/(x+0.5)` compilation at depth 10 with 25 nodes and baseline diagnostics of depth 14 / 43 nodes.
- Added `saturation_ratio_template` for strict `2*x/(x+0.5)` and Michaelis-Menten compilation at depth 12 with 41 nodes and baseline diagnostics of depth 18 / 75 nodes.
- Locked Michaelis-Menten zero-noise warm-start and CLI evidence as `same_ast_return` with verifier `recovered` and `changed_slot_count == 0`.
- Preserved Arrhenius as `direct_division_template` and Planck as stretch/unsupported for warm-start promotion.

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Reciprocal strict diagnostics test** - `aa631e5` (test)
2. **Task 1 GREEN: Reciprocal shift compiler macro** - `ff642ff` (feat)
3. **Task 2 RED: Saturation ratio strict compile test** - `500da17` (test)
4. **Task 2 GREEN: Saturation ratio compiler macro** - `fd51fda` (feat)
5. **Task 3: Michaelis same-AST warm-start and CLI evidence tests** - `434304d` (test)

## Files Created/Modified

- `src/eml_symbolic_regression/compiler.py` - Added unit-shift matching/building plus reciprocal and saturation structural macros.
- `tests/test_compiler_warm_start.py` - Added reciprocal, saturation, Michaelis warm-start, CLI, and guard assertions.
- `.planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-01-SUMMARY.md` - Captures execution results and verification.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_reciprocal_shift_uses_template -q` -> `1 passed`
- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_michaelis_uses_saturation_ratio_template tests/test_compiler_warm_start.py::test_compile_arrhenius_uses_direct_division_template -q` -> `2 passed`
- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_michaelis_warm_start_returns_same_ast_and_verifies tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_michaelis_same_ast_evidence tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_arrhenius_same_ast_evidence tests/test_compiler_warm_start.py::test_cli_reports_planck_as_stretch_without_promotion -q` -> `4 passed`
- Plan focused command covering six required tests -> `6 passed`
- Full warm-start/compiler test file: `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py -q` -> `20 passed, 1 warning`
- Direct CLI smoke: `PYTHONPATH=src python -m eml_symbolic_regression.cli demo michaelis_menten --warm-start-eml --points 24 --output /tmp/michaelis-51-01-cli.json` -> `michaelis_menten: recovered (catalog_showcase=verified_showcase, compiled_seed=recovered, warm_start_attempt=same_ast_return, trained_exact_recovery=recovered)`

## Decisions Made

- Used direct SymPy structure matching for unit shifts and saturation ratios rather than `sympy.together()`, formula ids, or string matching.
- Kept the default strict gate unchanged: `CompilerConfig().max_depth == 13` and `CompilerConfig().max_nodes == 256`.
- Treated Michaelis-Menten as same-AST warm-start evidence only; no blind-discovery status or claim wording was introduced.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Task 3 had no production-code change after the Task 2 macro, because the existing CLI and warm-start path automatically promoted validated compiled seeds. The stale unsupported Michaelis CLI test failed after Task 2 and was replaced with the required same-AST evidence assertions.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 52 can build exact cleanup expansion on top of the new structural macro diagnostics. Residual risk is intentionally scoped: the new motifs handle direct unit-shift and `c*x/(x+b)` SymPy shapes only, and branch correctness remains enforced through compile-time validation rather than broad algebraic normalization.

## Self-Check: PASSED

- Verified files exist: `src/eml_symbolic_regression/compiler.py`, `tests/test_compiler_warm_start.py`, `.planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-01-SUMMARY.md`.
- Verified task commits exist in git history: `aa631e5`, `ff642ff`, `500da17`, `fd51fda`, `434304d`.
- Stub scan found no TODO/FIXME/placeholder or hardcoded empty UI-data patterns in touched source/test files.

---
*Phase: 51-reciprocal-and-saturation-compiler-motifs*
*Completed: 2026-04-17*
