---
phase: 51-reciprocal-and-saturation-compiler-motifs
verified: 2026-04-17T14:36:50Z
status: passed
score: 10/10 must-haves verified
overrides_applied: 0
---

# Phase 51: Reciprocal and Saturation Compiler Motifs Verification Report

**Phase Goal:** Add reusable reciprocal-shift and saturation-ratio compiler motifs to reduce Michaelis-Menten depth and support honest recovery diagnostics.
**Verified:** 2026-04-17T14:36:50Z
**Status:** passed
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Reciprocal-shift motifs such as `1/(x+b)` are supported or fail closed with improved diagnostics. | VERIFIED | `tests/test_compiler_warm_start.py:61` asserts strict `1/(x+0.5)` compile at depth `10`, nodes `25`, macro hit `reciprocal_shift_template`, baseline depth `14`, baseline nodes `43`, and trace coverage. |
| 2 | Saturation-ratio motifs such as `(a*x)/(b+x)` use reusable compiler logic rather than formula-specific hardcoding. | VERIFIED | `compiler.py:331` implements `_compile_saturation_ratio` as structural `Mul`/`Pow` matching; no `michaelis_menten` or formula-string branch exists in `compiler.py`. |
| 3 | Before/after diagnostics record depth, node count, rule trace, and macro hits for reciprocal shift and Michaelis targets. | VERIFIED | Reciprocal diagnostics assert baseline/depth deltas at `tests/test_compiler_warm_start.py:79`; Michaelis diagnostics assert macro, baseline depth `18`, baseline nodes `75`, delta `6/34`, and trace at `tests/test_compiler_warm_start.py:104`. |
| 4 | Michaelis-Menten exact-recovers when strict support reaches the gate. | VERIFIED | `test_michaelis_warm_start_returns_same_ast_and_verifies` asserts `same_ast_return`, verifier `recovered`, depth `12`, nodes `41`, and macro `saturation_ratio_template`. |
| 5 | Strict default compiler and benchmark gates remain unchanged. | VERIFIED | `CompilerConfig.max_depth == 13`, `max_nodes == 256`; CLI defaults are `--max-compile-depth 13`, `--max-compile-nodes 256`; benchmark defaults are `max_compile_depth=13`, `max_compile_nodes=256`, `max_warm_depth=14`. |
| 6 | `1/(x+0.5)` compiles with macro `reciprocal_shift_template`, depth `10`, and nodes `25`. | VERIFIED | Focused pytest passed; code-level assertion at `tests/test_compiler_warm_start.py:76`. |
| 7 | `2*x/(x+0.5)` compiles with top-level macro `saturation_ratio_template`, depth `12`, and nodes `41`. | VERIFIED | Focused pytest passed; code-level assertion at `tests/test_compiler_warm_start.py:100`. |
| 8 | Review fixes are present: basis-only and non-finite derived constants fail closed, explicit unit coefficients are accepted, non-unit shifts are rejected. | VERIFIED | `_build_unit_shift()` checks finiteness and constant policy in `compiler.py:300`; `_match_unit_shift()` accepts only coefficient `1` in `compiler.py:276`; review-fix tests passed. |
| 9 | Michaelis artifact/CLI reports same-AST warm-start evidence, verifier `recovered`, evidence class `same_ast`, and does not claim blind discovery. | VERIFIED | CLI test asserts no `blind_baseline` in Michaelis payload at `tests/test_compiler_warm_start.py:544`; committed artifact validates `same_ast_return`, `recovered`, and `same_ast`; docs say "not blind discovery". |
| 10 | Arrhenius same-AST and Planck stretch behavior are preserved. | VERIFIED | Focused pytest included Arrhenius CLI same-AST and Planck stretch/unsupported tests; docs preserve Arrhenius and Planck wording in `README.md:183` and `README.md:217`. |

**Score:** 10/10 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `src/eml_symbolic_regression/compiler.py` | Reusable reciprocal and saturation macros | VERIFIED | `MACRO_RULES` includes `reciprocal_shift_template` and `saturation_ratio_template`; structural helper code is present and review fixes are implemented. |
| `src/eml_symbolic_regression/benchmark.py` | Focused `v1.9-michaelis-evidence` suite | VERIFIED | Built-in suite has one `michaelis-warm` warm-start case, seed `0`, noise `0.0`, points `24`, warm steps `1`, and default gates. |
| `tests/test_compiler_warm_start.py` | Compiler, warm-start, CLI, and review-fix regressions | VERIFIED | Targeted tests passed, including reciprocal/saturation depth locks, review-fix edge cases, Michaelis CLI, Arrhenius, and Planck. |
| `tests/test_benchmark_contract.py` | Suite expansion contract | VERIFIED | `test_michaelis_evidence_suite_contains_exact_warm_start_case` verifies suite id, run id, formula, expression, default gates, and tags. |
| `tests/test_benchmark_runner.py` | Artifact/evidence regression | VERIFIED | `test_michaelis_warm_benchmark_records_same_ast_evidence` verifies same-AST artifact fields and aggregate classification. |
| `README.md` | User-facing command and claim boundary | VERIFIED | Documents Michaelis as exact compiler warm-start / same-AST basin evidence and explicitly not blind discovery. |
| `docs/IMPLEMENTATION.md` | Implementation notes and evidence taxonomy | VERIFIED | Names both new macros, focused suite, artifact path, and Planck stretch boundary. |
| `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/suite-result.json` | Focused suite result | VERIFIED | Committed JSON validates one run, zero unsupported, zero failed, same-AST status, and strict gate metadata. |
| `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.json` | Machine-readable aggregate | VERIFIED | Aggregate run classification is `same_ast_warm_start_return`, evidence class `same_ast`. |
| `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.md` | Human-readable aggregate | VERIFIED | Includes `same_ast_warm_start_return` run row. |
| `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/v1-9-michaelis-evidence-michaelis-warm-a67d8ccfb108.json` | Per-run Michaelis artifact | VERIFIED | Validated status `same_ast_return`, claim `recovered`, evidence class `same_ast`, macro `saturation_ratio_template`, depth `12`, nodes `41`. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `compiler.py` | `tests/test_compiler_warm_start.py` | `compile_and_validate` | VERIFIED | GSD key-link check passed; tests assert exact motif outputs and validation. |
| `compiler.py` | `warm_start.py` | `fit_warm_started_eml_tree` | VERIFIED | Michaelis strict compiled AST is passed into the warm-start path and returns same AST. |
| `benchmark.py` | `datasets.py` | `_case("michaelis-warm", "michaelis_menten", "warm_start")` | VERIFIED | Suite expansion points at existing normalized Michaelis demo, not a duplicate formula. |
| `benchmark.py` | `compiler.py` | `_compile_demo` | VERIFIED | `_compile_demo` builds `CompilerConfig` from run optimizer gates and calls `compile_and_validate`. |
| `README.md` / `docs/IMPLEMENTATION.md` | Generated artifacts | Artifact path citations | VERIFIED | Docs cite `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/`. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| `compiler.py` | `CompileMetadata.macro_diagnostics` | Structural macro dispatch -> `_macro_diagnostics()` | Yes | FLOWING - tests and artifacts contain real macro hits, baselines, deltas, and trace entries. |
| `benchmark.py` | `compiled_eml`, `warm_start_eml`, `evidence_class` | `_compile_demo()` -> `fit_warm_started_eml_tree()` -> `evidence_class_for_payload()` | Yes | FLOWING - committed artifact and runner test show derived same-AST evidence, not hardcoded class in suite config. |
| Michaelis artifact JSON | Per-run evidence fields | Focused benchmark command and runner output | Yes | FLOWING - artifact validation checked status, verifier result, macro, depth, nodes, gates, and aggregate classification. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Compiler motifs, review fixes, CLI guards, and benchmark artifact regression | `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_reciprocal_shift_uses_template tests/test_compiler_warm_start.py::test_compile_michaelis_uses_saturation_ratio_template tests/test_compiler_warm_start.py::test_unit_shift_macros_do_not_smuggle_basis_only_constants tests/test_compiler_warm_start.py::test_unit_shift_macro_rejects_nonfinite_derived_constant tests/test_compiler_warm_start.py::test_explicit_unit_coefficient_reciprocal_shift_uses_template tests/test_compiler_warm_start.py::test_explicit_unit_coefficient_saturation_ratio_uses_template tests/test_compiler_warm_start.py::test_non_unit_coefficient_shift_does_not_use_unit_shift_templates tests/test_compiler_warm_start.py::test_michaelis_warm_start_returns_same_ast_and_verifies tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_michaelis_same_ast_evidence tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_arrhenius_same_ast_evidence tests/test_compiler_warm_start.py::test_cli_reports_planck_as_stretch_without_promotion tests/test_benchmark_contract.py::test_michaelis_evidence_suite_contains_exact_warm_start_case tests/test_benchmark_runner.py::test_michaelis_warm_benchmark_records_same_ast_evidence -q` | `13 passed in 34.73s` | PASS |
| Committed Michaelis artifacts validate against strict evidence fields | `python -c '...artifact assertions...'` | `artifact validation passed: same_ast_return recovered, depth=12, nodes=41, macro=saturation_ratio_template` | PASS |
| GSD artifact/key-link verifier | `gsd-tools verify artifacts/key-links` for all three plans | 11/11 artifacts and 9/9 key links passed | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| MIC-01 | 51-01 | Compile reciprocal shifts or fail closed with diagnostics | SATISFIED | `1/(x+0.5)` strict-compiles at depth `10`, nodes `25`, macro `reciprocal_shift_template`; basis-only/non-finite cases fail closed. |
| MIC-02 | 51-01 | Compile or rewrite saturation ratios through reusable logic | SATISFIED | Structural `saturation_ratio_template` handles `2*x/(x+0.5)` and explicit unit-coefficient forms; no compiler formula-id hardcoding found. |
| MIC-03 | 51-01, 51-03 | Compare before/after diagnostics with depth, nodes, trace, macro hits | SATISFIED | Tests and artifacts record baseline depth/nodes, deltas, macro hits, and trace rules for reciprocal and Michaelis targets. |
| MIC-04 | 51-01, 51-02, 51-03 | Run Michaelis warm-start recovery if strict support reaches the gate | SATISFIED | CLI, benchmark runner, and committed artifact report `same_ast_return`, verifier `recovered`, and evidence class `same_ast`. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `src/eml_symbolic_regression/benchmark.py` | 751 | local variable named `placeholder` | Info | Existing run-id placeholder object, not a stub and not introduced as incomplete behavior. |
| Various tests/generated artifact schemas | n/a | benign empty arrays/null schema fields | Info | Test fixtures and generated JSON schema values, not hollow runtime data. |

No blocker or warning anti-patterns were found. No `TODO`, `FIXME`, placeholder UI/data stubs, empty source implementations, or console-log-only implementations were found in Phase 51 source/test/doc files.

### Human Verification Required

None. Phase 51 is a local compiler/CLI/benchmark artifact change with automated checks covering the observable behaviors.

### Gaps Summary

No gaps found. Phase 51 achieved the goal: reusable reciprocal-shift and saturation-ratio motifs exist, strict gates remain unchanged, Michaelis-Menten reaches strict same-AST warm-start recovery with honest evidence classification, the review fixes are present, focused artifacts validate, and Arrhenius/Planck boundaries remain intact.

---

_Verified: 2026-04-17T14:36:50Z_
_Verifier: Codex (gsd-verifier)_
