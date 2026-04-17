---
phase: 50-arrhenius-exact-warm-start-demo
verified: 2026-04-17T13:18:30Z
status: passed
score: "8/8 must-haves verified"
overrides_applied: 0
---

# Phase 50: Arrhenius Exact Warm-Start Demo Verification Report

**Phase Goal:** Add Arrhenius as a normalized scientific-law demo with strict compile support and exact verified warm-start return.
**Verified:** 2026-04-17T13:18:30Z
**Status:** passed
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `arrhenius` exists as a built-in demo dataset with positive train, held-out, and extrapolation domains. | VERIFIED | `src/eml_symbolic_regression/datasets.py` defines `DemoSpec("arrhenius")` with target `np.exp(-0.8 / a)`, SymPy candidate `sp.exp(-sp.Float("0.8") / x)`, domains `(0.5, 3.0)`, `(0.6, 2.7)`, `(3.1, 4.2)`, `sources/FOR_DEMO.md`, and `normalized_dimensionless=True`. |
| 2 | Strict compiler diagnostics report support within the current depth gate and include `direct_division_template`. | VERIFIED | `tests/test_compiler_warm_start.py::test_compile_arrhenius_uses_direct_division_template` asserts validation passed, unsupported reason is `None`, depth is `7`, and macro hits are exactly `["direct_division_template"]`. `src/eml_symbolic_regression/compiler.py` has generic `_compile_direct_division`; no `arrhenius` branch exists in compiler, warm-start, or CLI code. |
| 3 | Zero-noise compiler warm-start returns the same exact AST and verifier status `recovered`. | VERIFIED | `test_arrhenius_warm_start_returns_same_ast_and_verifies` asserts `same_ast_return`, verifier `recovered`, diagnosis mechanism `same_ast_return`, changed slot count `0`, and direct-division compiler metadata. |
| 4 | A reproducible artifact/report path records compile depth, warm-start status, verifier status, and evidence regime. | VERIFIED | Permanent artifacts under `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/` contain one `arrhenius-warm` run with depth `7`, macro `direct_division_template`, status `same_ast_return`, claim/verifier `recovered`, evidence class `same_ast`, and aggregate classification `same_ast_warm_start_return`. |
| 5 | CLI demo output preserves same-AST warm-start evidence, not blind discovery. | VERIFIED | `test_cli_warm_start_promotes_arrhenius_same_ast_evidence` asserts `compiled_seed=recovered`, `warm_start_attempt=same_ast_return`, `trained_exact_recovery=recovered`, depth `7`, macro `direct_division_template`, and warm-start verifier `recovered`; README and implementation docs explicitly say not blind discovery. |
| 6 | Focused suite `v1.9-arrhenius-evidence` expands exactly case `arrhenius-warm` for zero-noise warm start. | VERIFIED | `src/eml_symbolic_regression/benchmark.py` registers one focused suite/case with formula `arrhenius`, start mode `warm_start`, seed `0`, perturbation noise `0.0`, points `24`, `warm_steps=1`, and tags `v1.9`, `arrhenius`, `warm_start`, `same_ast`. |
| 7 | Documentation is evidence-backed and regime-honest. | VERIFIED | `README.md` and `docs/IMPLEMENTATION.md` cite the generated artifact root, exact suite/case, formula `exp(-0.8/x)`, domains, macro, `same_ast_return`, verifier `recovered`, and `same_ast` evidence class. Both describe exact compiler warm-start / same-AST basin evidence, not blind discovery. |
| 8 | Michaelis-Menten and Planck unsupported/stretch behavior is preserved. | VERIFIED | Existing CLI guard tests still assert Michaelis-Menten `compiled_seed == "unsupported"` and Planck stretch reported with unsupported warm start. README and implementation docs preserve default-gate unsupported/stretch caveats. |

**Score:** 8/8 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/datasets.py` | Built-in `arrhenius` demo with normalized formula and positive domains. | VERIFIED | Lines 155-166 define the required demo. The GSD artifact text matcher missed the literal pattern `exp(-0.8 / x)` because the code uses `sp.exp(-sp.Float("0.8") / x)` plus target `np.exp(-0.8 / a)`; manual semantic checks, tests, and artifacts confirm `exp(-0.8/x)`. |
| `src/eml_symbolic_regression/benchmark.py` | Built-in `v1.9-arrhenius-evidence` suite and `arrhenius-warm` case. | VERIFIED | Suite registry includes `v1.9-arrhenius-evidence`; case uses formula `arrhenius`, warm start, seed `0`, noise `0.0`, and same-AST tags. |
| `tests/test_proof_dataset_manifest.py` | Positive-domain and provenance coverage. | VERIFIED | Test checks domains, jittered positive samples, complex finite targets, manifest domains, FOR_DEMO provenance, and no raw arrays. |
| `tests/test_compiler_warm_start.py` | Strict compile, warm-start, CLI, and unsupported/stretch guards. | VERIFIED | Tests cover strict macro compile, zero-noise same-AST return, CLI output, Michaelis-Menten unsupported, and Planck stretch. |
| `tests/test_benchmark_contract.py` | Suite registry and expansion contract. | VERIFIED | Test asserts one `arrhenius-warm` run with stable identity, formula expression, domains, tags, seed, noise, and warm budget. |
| `tests/test_benchmark_runner.py` | Artifact regression for same-AST Arrhenius evidence. | VERIFIED | Test runs the focused suite and asserts per-run artifact plus aggregate evidence classification. |
| `README.md` | User-facing command and claim boundary. | VERIFIED | Contains demo and benchmark commands plus explicit same-AST/not-blind-discovery wording. |
| `docs/IMPLEMENTATION.md` | Implementation-level evidence notes. | VERIFIED | Contains suite, artifact root, demo ladder, macro, statuses, and preserved unsupported/stretch notes. |
| `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/suite-result.json` | Permanent suite evidence. | VERIFIED | Structured validation found suite `v1.9-arrhenius-evidence`, one result, case `arrhenius-warm`, status `same_ast_return`. |
| `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/aggregate.json` | Machine-readable aggregate. | VERIFIED | Structured validation found total `1`, evidence class `same_ast`, classification `same_ast_warm_start_return`. |
| `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/aggregate.md` | Human-readable aggregate. | VERIFIED | Records `arrhenius`, `same_ast_return`, and `same_ast_warm_start_return`. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `datasets.py` | `compiler.py` | SymPy candidate `sp.exp(-sp.Float("0.8") / x)` exposes direct division. | VERIFIED | GSD key-link check passed; compile test records direct-division trace. |
| `tests/test_compiler_warm_start.py` | `warm_start.py` | `fit_warm_started_eml_tree` with `noise_scale=0.0`. | VERIFIED | GSD key-link check passed; warm-start test asserts same-AST result. |
| `tests/test_compiler_warm_start.py` | `cli.py` | `demo arrhenius --warm-start-eml` JSON output. | VERIFIED | GSD key-link check passed; CLI test asserts stage statuses and verifier result. |
| `benchmark.py` | `datasets.py` | `_case("arrhenius-warm", "arrhenius", "warm_start")`. | VERIFIED | GSD key-link check passed; suite contract test confirms expansion. |
| `benchmark.py` | `compiler.py` | Warm-start run calls `_compile_demo` and serializes `compiled_eml`. | VERIFIED | GSD key-link check passed; artifact has compile depth and macro diagnostics. |
| `tests/test_benchmark_runner.py` | `benchmark.py` | `run_benchmark_suite` writes artifact and derives `same_ast`. | VERIFIED | GSD key-link check passed; runner test and permanent artifact agree. |
| `README.md` | generated artifacts | Docs cite focused artifact path. | VERIFIED | GSD key-link check passed; docs cite artifact root. |
| `docs/IMPLEMENTATION.md` | `benchmark.py` | Documentation uses implemented suite/case names. | VERIFIED | GSD key-link check passed. |
| `suite-result.json` | `tests/test_benchmark_runner.py` | Artifact fields mirror runner regression assertions. | VERIFIED | GSD key-link check passed. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `datasets.py` | Split inputs/targets for `arrhenius` | `DemoSpec.make_splits(points=24, seed=0)` samples configured domains and evaluates `np.exp(-0.8 / a)`. | Yes | FLOWING |
| `tests/test_compiler_warm_start.py` | Compiled Arrhenius AST | `compile_and_validate(spec.candidate.to_sympy(), CompilerConfig(...), validation_inputs)` | Yes | FLOWING |
| `warm_start.py` path via tests/CLI | Warm-start manifest and verifier result | `fit_warm_started_eml_tree(..., PerturbationConfig(noise_scale=0.0), verification_splits=splits)` | Yes | FLOWING |
| `benchmark.py` | Per-run artifact payload | `run_benchmark_suite(builtin_suite("v1.9-arrhenius-evidence"), RunFilter(...))` | Yes | FLOWING |
| permanent artifacts | Suite, per-run, aggregate JSON/Markdown | Focused benchmark command output under `artifacts/campaigns/v1.9-arrhenius-evidence`. | Yes | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Arrhenius dataset, strict compile, warm start, CLI, suite, artifact, and MM/Planck guards pass. | `env PYTHONPATH=src python -m pytest tests/test_proof_dataset_manifest.py::test_arrhenius_demo_uses_positive_dimensionless_domains tests/test_compiler_warm_start.py::test_compile_arrhenius_uses_direct_division_template tests/test_compiler_warm_start.py::test_arrhenius_warm_start_returns_same_ast_and_verifies tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_arrhenius_same_ast_evidence tests/test_compiler_warm_start.py::test_cli_reports_michaelis_menten_depth_gate_without_promotion tests/test_compiler_warm_start.py::test_cli_reports_planck_as_stretch_without_promotion tests/test_benchmark_contract.py::test_arrhenius_evidence_suite_contains_exact_warm_start_case tests/test_benchmark_runner.py::test_arrhenius_warm_benchmark_records_same_ast_evidence -q` | `8 passed in 8.77s` | PASS |
| Permanent artifact fields are internally consistent. | Structured JSON validation over `suite-result.json`, referenced per-run artifact, and `aggregate.json`. | Suite count `1`; `arrhenius-warm`; formula `exp(-0.8/x)`; domains `[0.5, 3.0]`, `[0.6, 2.7]`, `[3.1, 4.2]`; depth `7`; macro `direct_division_template`; `same_ast_return`; verifier `recovered`; aggregate `same_ast_warm_start_return`. | PASS |
| No formula-specific compiler branch exists. | `rg -n "arrhenius|Arrhenius" src/eml_symbolic_regression/compiler.py src/eml_symbolic_regression/warm_start.py src/eml_symbolic_regression/cli.py` | No matches. | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| ARR-01 | 50-01 | Developer can generate a normalized Arrhenius demo dataset for `exp(-0.8/x)` over positive domains safely away from zero. | SATISFIED | DemoSpec, manifest test, and permanent artifact all show formula and domains. |
| ARR-02 | 50-01 | Developer can strictly compile the Arrhenius target within the supported depth gate and inspect macro diagnostics including `direct_division_template`. | SATISFIED | Compile test and artifact show depth `7`, macro `direct_division_template`, validation passed, no unsupported reason. |
| ARR-03 | 50-01 | Developer can run a zero-noise Arrhenius compiler warm start that returns the same exact AST and verifier status `recovered`. | SATISFIED | Warm-start and CLI tests plus artifact show `same_ast_return`, verifier `recovered`, changed slots `0`. |
| ARR-04 | 50-02, 50-03 | Developer can reproduce an Arrhenius benchmark or report artifact with compile depth, warm-start status, verifier status, and regime labeling. | SATISFIED | `v1.9-arrhenius-evidence` suite/case, permanent artifacts, aggregate report, README, and implementation docs all carry required fields and `same_ast` regime labeling. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/eml_symbolic_regression/benchmark.py` | 750 | Internal variable named `placeholder` used while constructing stable run IDs. | Info | Not a stub; existing implementation detail, not user-visible output. |
| Multiple source/test files | Various | Empty list/dict initializers and assertions. | Info | Not stubs; local accumulators, optional fields, or test expectations. |

No blocker anti-patterns were found. No TODO/FIXME/placeholder user-facing text, hardcoded empty output, or console-log-only implementation blocks Phase 50.

### Human Verification Required

None. Phase 50 is a deterministic package/CLI/artifact phase; the relevant behavior is covered by focused tests and structured artifact validation.

### Gaps Summary

No gaps found. The phase goal is achieved: Arrhenius is a normalized positive-domain demo; strict compile support uses the reusable `direct_division_template` within the depth gate; zero-noise warm start returns the same exact AST with verifier `recovered`; and permanent focused artifacts plus docs preserve the `same_ast` evidence regime without claiming blind discovery.

---

_Verified: 2026-04-17T13:18:30Z_
_Verifier: Codex (gsd-verifier)_
