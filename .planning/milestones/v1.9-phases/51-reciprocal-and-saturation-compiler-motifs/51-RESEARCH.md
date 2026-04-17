# Phase 51: Reciprocal and Saturation Compiler Motifs - Research

**Researched:** 2026-04-17 [VERIFIED: environment_context]
**Domain:** Existing SymPy-to-EML compiler macros, Michaelis-Menten demo diagnostics, CLI warm-start reporting, and benchmark artifact evidence regimes. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
**Confidence:** HIGH for the recommended compiler approach because local probes validated the exact EML identity, depth reduction, verifier status, and zero-noise warm-start behavior before any code edits. [VERIFIED: local compiler probe] [VERIFIED: local warm-start probe]

<user_constraints>
## User Constraints (from CONTEXT.md)

All bullets in this section are copied or scoped directly from `.planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md`. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]

### Locked Decisions

- Target demo: `michaelis_menten`.
- Target formula: `2*x/(x + 0.5)`.
- Current best diagnostic: strict compile is unsupported at `max_depth=13`, but relaxed compile succeeds at depth `<= 14` and already records `direct_division_template`.
- Primary motifs:
  - `reciprocal_shift_template` for structures like `1/(x + b)`.
  - `saturation_ratio_template` for structures like `(a*x)/(b + x)`.
- Macro work must be reusable motif logic, not a one-off recognizer for `michaelis_menten`.
- If strict support reaches the current gate, add a Michaelis-Menten exact warm-start recovery path; otherwise record material depth/node reduction with honest unsupported status.
- Preserve existing Planck stretch behavior and Arrhenius same-AST evidence classification.

### Claude's Discretion

The phase context gives implementation freedom inside reusable compiler helpers, focused tests, and focused evidence artifacts, as long as the work preserves strict depth gates and evidence regime labels. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]

### Deferred Ideas (OUT OF SCOPE)

- Broad paper-facing campaign packaging belongs to Phase 53. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md] [VERIFIED: .planning/ROADMAP.md]
- Planck is not a Phase 51 flagship and should only be guarded through regression tests. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]
- Silent compile-depth relaxation and formula-id-specific recognizers are out of scope. [VERIFIED: .planning/REQUIREMENTS.md] [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| MIC-01 | Developer can compile reciprocal-shift motifs such as `1/(x + b)` or inspect a fail-closed diagnostic explaining remaining unsupported structure. [VERIFIED: .planning/REQUIREMENTS.md] | Add `reciprocal_shift_template` for `Pow(Add(Symbol, numeric), -1)` using the validated unit-shift EML identity, then keep validation as the acceptance gate. [VERIFIED: local compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| MIC-02 | Developer can compile or rewrite saturation-ratio motifs such as `(a*x)/(b + x)` through reusable compiler logic rather than a one-off formula recognizer. [VERIFIED: .planning/REQUIREMENTS.md] | Add `saturation_ratio_template` for structural `Mul(a, Symbol, Pow(Add(Symbol, numeric), -1))`, not for the `michaelis_menten` demo id. [VERIFIED: local compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| MIC-03 | Developer can compare before/after compiler diagnostics for `1/(x+0.5)` and `2*x/(x+0.5)`, including depth, node count, rule trace, and macro hits. [VERIFIED: .planning/REQUIREMENTS.md] | Current probes establish baseline diagnostics; post-change tests should assert strict compile, depth/node deltas, trace rules, and macro hits. [VERIFIED: local compiler probe] [VERIFIED: tests/test_compiler_warm_start.py] |
| MIC-04 | Developer can run Michaelis-Menten warm-start recovery if strict support reaches the gate, or see an honest unsupported artifact if the macro work only reduces depth. [VERIFIED: .planning/REQUIREMENTS.md] | Prototype exact EML tree for `2*x/(x+0.5)` has depth 12 and returned `same_ast_return` with verifier `recovered`, so strict support should enable focused same-AST warm-start evidence if implementation preserves the identity. [VERIFIED: local warm-start probe] |
</phase_requirements>

## Summary

The current compiler already has a macro layer with serialized hits, misses, no-macro baseline depth, no-macro node count, and depth/node deltas. [VERIFIED: src/eml_symbolic_regression/compiler.py] Phase 37 deliberately kept `direct_division_template` limited to explicit numerator-over-denominator structures, which made Michaelis-Menten materially shorter but still strict-unsupported at the depth-13 gate. [VERIFIED: .planning/milestones/v1.6-phases/37-01-SUMMARY.md] [VERIFIED: tests/test_compiler_warm_start.py]

The best implementation path is to add a shared unit-shift EML builder for `x + b`, then use it from two first-class macro rules: `reciprocal_shift_template` for `1/(x+b)` and `saturation_ratio_template` for `a*x/(x+b)`. [VERIFIED: local compiler probe] The validated identity is `x + b = eml(log(x), exp(-b))`, represented as `Eml(log_of(Var(x)), Const(exp(-b)))`; on the positive Michaelis domain it validated against NumPy and SymPy at numerical error below `1e-15`. [VERIFIED: local compiler probe] [VERIFIED: src/eml_symbolic_regression/expression.py]

**Primary recommendation:** implement reusable structural matchers in `compiler.py`, add the new macro names to `MACRO_RULES`, prove `1/(x+0.5)` compiles at depth 10 and `2*x/(x+0.5)` compiles at depth 12 under the unchanged strict gate, then promote Michaelis-Menten only as compiler warm-start / same-AST evidence if CLI and benchmark artifacts verify `same_ast_return`, verifier `recovered`, and `evidence_class == "same_ast"`. [VERIFIED: local compiler probe] [VERIFIED: local warm-start probe] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Motif recognition | Compiler | Tests | `compile_sympy_expression()` owns structural SymPy lowering and macro trace recording. [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| Exact EML identities | Compiler / expression AST | Verifier | The compiler builds `Expr` trees from `Const`, `Var`, `Eml`, `log_of`, `multiply_expr`, and `divide_expr`; `compile_and_validate()` validates behavior before returning a compile result. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/expression.py] |
| Michaelis demo definition | Dataset registry | CLI and benchmark | `demo_specs()` owns formula id, target function, SymPy candidate, domains, and provenance for `michaelis_menten`. [VERIFIED: src/eml_symbolic_regression/datasets.py] |
| Warm-start promotion | CLI / benchmark runner | Warm-start optimizer | CLI and benchmark code only warm-start after strict `compile_and_validate()` succeeds and compiled depth is within the warm-depth gate. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Recovery status | Verifier | CLI / benchmark runner | `verify_candidate()` owns `recovered`; reports should not promote training loss or relaxed compile diagnostics to recovery. [VERIFIED: src/eml_symbolic_regression/verify.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Evidence class | Benchmark taxonomy | Reports/docs | `evidence_class_for_payload()` maps compiler warm-start `same_ast_return` to `same_ast`, separate from blind recovery. [VERIFIED: src/eml_symbolic_regression/benchmark.py] |

## Project Constraints (from AGENTS.md)

- EML semantics, complete-tree construction, snapping, and complex arithmetic must stay grounded in `sources/paper.pdf` and `sources/NORTH_STAR.md`. [VERIFIED: AGENTS.md]
- Training defaults to PyTorch `complex128`, with clamps only in training mode and faithful verification afterward. [VERIFIED: AGENTS.md] [VERIFIED: src/eml_symbolic_regression/optimize.py]
- A candidate is not recovered from training loss alone; it must pass held-out, extrapolation, and high-precision checks. [VERIFIED: AGENTS.md] [VERIFIED: src/eml_symbolic_regression/verify.py]
- v1 must avoid overselling blind deep recovery because project state records rapid degradation beyond shallow depths. [VERIFIED: AGENTS.md] [VERIFIED: .planning/STATE.md]
- Showcase examples must come from `sources/FOR_DEMO.md`, favoring normalized, dimensionless, visually distinctive laws. [VERIFIED: AGENTS.md] [VERIFIED: sources/FOR_DEMO.md]
- GSD workflow instructions require file-changing work to go through a GSD command; this research artifact is part of the requested GSD phase workflow. [VERIFIED: AGENTS.md] [VERIFIED: user request]
- No project-local `CLAUDE.md` or project-local skills were found. [VERIFIED: `ls -la`] [VERIFIED: `find .claude/skills .agents/skills -maxdepth 2 -name SKILL.md`]

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11.5 local; `>=3.11,<3.13` in `pyproject.toml` | Package, CLI, and tests. [VERIFIED: `python --version`] [VERIFIED: pyproject.toml] | The package and console script are Python modules under `src/`. [VERIFIED: pyproject.toml] |
| SymPy | 1.14.0 local; `>=1.14` in `pyproject.toml` | Source expression tree and structural motif matching. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | `DemoSpec` stores SymPy candidates and the compiler consumes SymPy expressions. [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| NumPy | 1.26.4 local; `>=1.26` in `pyproject.toml` | Validation inputs, demo targets, and exact EML NumPy evaluation. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | Compiler validation and demo datasets already use NumPy arrays. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/datasets.py] |
| PyTorch | 2.10.0 local; `>=2.10` in `pyproject.toml` | Warm-start embedding, one-step same-AST return, and optimizer path. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | `fit_warm_started_eml_tree()` uses the existing PyTorch-backed optimizer and snap path. [VERIFIED: src/eml_symbolic_regression/warm_start.py] |
| mpmath | 1.3.0 local; `>=1.3` in `pyproject.toml` | High-precision verifier checks. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | `verify_candidate()` uses high-precision checks in the recovery contract. [VERIFIED: src/eml_symbolic_regression/verify.py] |
| pytest | 7.4.0 local; `>=7.4` dev dependency | Compiler, CLI, and benchmark regression tests. [VERIFIED: `python -m pytest --version`] [VERIFIED: pyproject.toml] | Existing Phase 50 and Phase 37 regression tests are pytest-based. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `argparse` | Python stdlib | Existing CLI options for demo and benchmark commands. [VERIFIED: src/eml_symbolic_regression/cli.py] | Use existing `--warm-start-eml`, `--max-compile-depth`, `--max-warm-depth`, and `--output` options; no parser change is required for the compiler motif itself. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| `json` / `pathlib` | Python stdlib | Existing demo and benchmark JSON artifacts. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] | Reuse current artifact schemas rather than adding a Phase 51-only output format. [VERIFIED: src/eml_symbolic_regression/benchmark.py] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Structural `reciprocal_shift_template` | Generic negative power lowering | Generic lowering compiles `1/(x+0.5)` at depth 14, which fails the strict depth-13 gate. [VERIFIED: local compiler probe] |
| Structural `saturation_ratio_template` | Existing `direct_division_template` only | Existing direct division compiles `2*x/(x+0.5)` at depth 14 and node count 59; the unit-shift saturation prototype compiles at depth 12 and node count 41. [VERIFIED: local compiler probe] |
| Reusable motif matcher | Formula-id branch for `michaelis_menten` | Formula-id branching violates locked context and would not satisfy MIC-02. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md] [VERIFIED: .planning/REQUIREMENTS.md] |
| Strict gate unchanged | Raise `max_depth` or `max_warm_depth` silently | Silent gate relaxation is explicitly out of scope for v1.9. [VERIFIED: .planning/REQUIREMENTS.md] |
| Focused Michaelis evidence path | Broad Phase 53 paper suite now | Phase 53 owns paper-facing campaign/report packaging after Phase 51 and Phase 52 evidence exists. [VERIFIED: .planning/ROADMAP.md] |

**Installation:**

```bash
# No new packages are required for Phase 51.
python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py
```

Version verification used local commands only because the user requested codebase-grounded research, not internet lookup. [VERIFIED: user request] [VERIFIED: local version probe]

## Current Baseline Diagnostics

The local probe used `CompilerConfig(variables=("x",), max_depth=13, max_nodes=256)` and validation inputs `x = linspace(0.25, 2.5, 12)`. [VERIFIED: local compiler probe]

| Expression | Strict Status | Strict Reason | Relaxed Depth | Relaxed Nodes | Current Macro Hits | No-Macro Depth | No-Macro Nodes | Notes |
|------------|---------------|---------------|---------------|---------------|--------------------|----------------|----------------|-------|
| `1/(x + 0.5)` | unsupported [VERIFIED: local compiler probe] | `depth_exceeded`; compiled depth 14 exceeds max_depth 13. [VERIFIED: local compiler probe] | 14 [VERIFIED: local compiler probe] | 43 [VERIFIED: local compiler probe] | none; misses `direct_division_template` and `scaled_exp_minus_one_template`. [VERIFIED: local compiler probe] | 14 [VERIFIED: local compiler probe] | 43 [VERIFIED: local compiler probe] | Current path is generic `negative_power` after compiling `x + 0.5`. [VERIFIED: local compiler probe] |
| `2*x/(x + 0.5)` | unsupported [VERIFIED: local compiler probe] | `depth_exceeded`; compiled depth 14 exceeds max_depth 13. [VERIFIED: local compiler probe] | 14 [VERIFIED: local compiler probe] | 59 [VERIFIED: local compiler probe] | `direct_division_template`. [VERIFIED: local compiler probe] | 18 [VERIFIED: local compiler probe] | 75 [VERIFIED: local compiler probe] | Current macro saves 4 depth and 16 nodes versus no-macro baseline but still misses the strict gate. [VERIFIED: local compiler probe] |

The proposed unit-shift EML builder produced these no-edit prototype results on the same validation domain. [VERIFIED: local compiler probe]

| Prototype Expression | Depth | Node Count | Validation Result | Expected Macro |
|----------------------|-------|------------|-------------------|----------------|
| `x + 0.5` as `eml(log(x), exp(-0.5))` | 4 [VERIFIED: local compiler probe] | 9 [VERIFIED: local compiler probe] | Max absolute error `4.44e-16`. [VERIFIED: local compiler probe] | internal helper, not necessarily public macro. [VERIFIED: local compiler probe] |
| `1/(x + 0.5)` using shifted denominator | 10 [VERIFIED: local compiler probe] | 25 [VERIFIED: local compiler probe] | Max absolute error `4.44e-16`. [VERIFIED: local compiler probe] | `reciprocal_shift_template`. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md] |
| `2*x/(x + 0.5)` using shifted denominator | 12 [VERIFIED: local compiler probe] | 41 [VERIFIED: local compiler probe] | Max absolute error `8.88e-16`. [VERIFIED: local compiler probe] | `saturation_ratio_template`. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md] |

The no-edit prototype for `2*x/(x+0.5)` verified as `recovered`, had high-precision max error about `1.07e-18`, and returned `same_ast_return` with `changed_slot_count == 0` under zero-noise warm start. [VERIFIED: local warm-start probe]

## Architecture Patterns

### System Architecture Diagram

```text
SymPy expression from demo or direct compiler test
        |
        v
_Compiler.compile()
        |
        +--> _compile_special()
        |        |
        |        +--> Pow(Add(Symbol, numeric), -1)
        |        |        |
        |        |        v
        |        |   reciprocal_shift_template
        |        |        |
        |        |        v
        |        |   unit_shift_expr: eml(log(x), exp(-b))
        |        |        |
        |        |        v
        |        |   divide_expr(1, shifted_denominator)
        |        |
        |        +--> Mul(a, Symbol, Pow(Add(same Symbol, numeric), -1))
        |        |        |
        |        |        v
        |        |   saturation_ratio_template
        |        |        |
        |        |        v
        |        |   divide_expr(a*x, shifted_denominator)
        |        |
        |        +--> existing direct_division_template / scaled_exp_minus_one_template
        |
        v
compile_and_validate()
        |
        +--> depth <= 13 and nodes <= 256 -> compiled_eml metadata + verifier
        |
        +--> depth > 13 or validation failure -> fail-closed diagnostic
```

This architecture preserves the existing ownership: compiler macros produce exact ASTs and metadata, while CLI and benchmark code serialize strict success or fail-closed diagnostics. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

### Recommended Project Structure

```text
src/eml_symbolic_regression/
  compiler.py       # Add macro names, structural matchers, unit-shift helper, diagnostics.
  benchmark.py      # Add focused Michaelis suite only if strict support succeeds.
tests/
  test_compiler_warm_start.py  # Add reciprocal/saturation compile tests and update Michaelis CLI expectations.
  test_benchmark_contract.py   # Add focused suite registry test if a Phase 51 suite is added.
  test_benchmark_runner.py     # Add artifact/evidence-class regression if a Phase 51 suite is added.
docs/
  IMPLEMENTATION.md # Update after tests/artifacts prove the new claim boundary.
README.md          # Update after a durable artifact exists, if Phase 51 produces one.
```

These files are the current owners of compiler macros, CLI warm-start checks, benchmark suites, and artifact evidence tests. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: tests/test_benchmark_runner.py]

### Pattern 1: Shared Unit-Shift Builder

**What:** Build `x + b` as `Eml(log_of(Var(variable)), Const(exp(-b)))` for unit-coefficient variable plus numeric literal. [VERIFIED: local compiler probe]

**When to use:** Use only inside structural reciprocal-shift and saturation-ratio macros, and only after matching exactly one symbol term and one numeric term. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]

**Example:**

```python
# Source pattern: local probe using existing Expr, Eml, Const, Var, and log_of.
def _unit_shift_expr(variable: str, offset: complex) -> Expr:
    return Eml(log_of(Var(variable)), Const(np.exp(-offset)))
```

This helper is valid only if downstream validation passes on the configured inputs, so `compile_and_validate()` remains the gate for branch and singularity problems. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: local compiler probe]

### Pattern 2: Reciprocal Shift Macro

**What:** Match `Pow(base, -1)` where `base` is a unit shift `x + b`, then return `divide_expr(Const(1.0), _unit_shift_expr(x, b))`. [VERIFIED: local compiler probe]

**When to use:** Use before generic `_compile_power()` so reciprocal-only expressions get a first-class macro hit instead of silently falling through to `negative_power`. [VERIFIED: src/eml_symbolic_regression/compiler.py]

**Example:**

```python
# Source pattern: src/eml_symbolic_regression/compiler.py macro style.
if isinstance(expr, sp.Pow) and expr.exp == -1:
    match = self._match_unit_shift(expr.base)
    if match is not None:
        variable, offset = match
        shifted = self._unit_shift_expr(variable, offset)
        return self._record("reciprocal_shift_template", expr, divide_expr(Const(1.0), shifted))
```

The test should assert strict `compile_and_validate(1/(x+0.5))` succeeds at depth 10, node count 25, and macro hits include `reciprocal_shift_template`. [VERIFIED: local compiler probe]

### Pattern 3: Saturation Ratio Macro

**What:** Match `Mul(a, x, Pow(x + b, -1))` or the SymPy-equivalent ordered form, require that the numerator symbol and denominator shift symbol are the same, then return `divide_expr(a*x, _unit_shift_expr(x, b))`. [VERIFIED: local compiler probe]

**When to use:** Use before `_compile_direct_division()` so Michaelis-style saturation ratios get the lower-depth motif while arbitrary numerator-over-denominator cases keep the existing direct-division behavior. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: local compiler probe]

**Example:**

```python
# Source pattern: existing _compile_direct_division() structural matching.
factor = denominator_factors[0]
match = self._match_unit_shift(factor.base)
coeff, rest = numerator.as_coeff_Mul()
if match is not None and rest == sp.Symbol(match.variable) and coeff.is_number:
    numerator_expr = multiply_expr(Const(self._constant_value(coeff)), Var(match.variable))
    shifted = self._unit_shift_expr(match.variable, match.offset)
    return self._record("saturation_ratio_template", expr, divide_expr(numerator_expr, shifted))
```

The test should assert strict `compile_and_validate(2*x/(x+0.5))` succeeds at depth 12, node count 41, and macro hits include `saturation_ratio_template`. [VERIFIED: local compiler probe]

### Anti-Patterns to Avoid

- **Formula-id branching:** Do not branch on `michaelis_menten`; match SymPy structure only. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]
- **Silent gate relaxation:** Do not change default `CompilerConfig.max_depth=13`, CLI `--max-compile-depth=13`, benchmark `max_compile_depth=13`, or `max_warm_depth=14` as a substitute for shortening. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
- **Macro hits without real shortening:** Do not use `sympy.together()` or broad simplification that turns unrelated forms into apparent denominator motifs; Phase 37 already found that this can produce dishonest macro hits. [VERIFIED: .planning/milestones/v1.6-phases/37-01-SUMMARY.md]
- **Relaxed diagnostic promotion:** Do not run warm start from `diagnose_compile_expression()["relaxed"]`; existing CLI and benchmark code correctly require strict `compile_and_validate()` before warm start. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
- **Evidence regime collapse:** Do not label same-AST warm start as blind discovery. [VERIFIED: .planning/PROJECT.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| New artifact schema | A Phase 51-only JSON report | Existing CLI and benchmark payloads | Current payloads already serialize `compiled_eml`, diagnostics, `stage_statuses`, verifier status, `evidence_class`, and metrics. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Symbolic equality proof | A custom theorem prover | `compile_and_validate()` plus `verify_candidate()` | The project recovery contract is numeric/high-precision verification, not formal theorem proving. [VERIFIED: .planning/PROJECT.md] [VERIFIED: src/eml_symbolic_regression/verify.py] |
| Broad algebraic normalizer | Custom rational simplification or `sympy.together()` macro input | Local structural matching | Phase 37 recorded that broad rationalization caused accidental macro hits and was replaced by explicit structure inspection. [VERIFIED: .planning/milestones/v1.6-phases/37-01-SUMMARY.md] |
| New warm-start runner | Separate Michaelis training script | Existing `fit_warm_started_eml_tree()` through CLI/benchmark | Existing code already handles compiled AST embedding, zero-noise same-AST return, verifier output, and evidence classification. [VERIFIED: src/eml_symbolic_regression/warm_start.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| New dependencies | External symbolic regression or optimizer package | Existing Python/SymPy/PyTorch stack | Phase 51 only needs compiler motif logic and focused tests; no new package is required. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] |

**Key insight:** The useful shortcut is not a Michaelis recognizer; it is the reusable unit-shift identity `x+b = eml(log(x), exp(-b))`, applied in reciprocal and saturation structures while preserving strict validation. [VERIFIED: local compiler probe]

## Risks And Common Pitfalls

### Pitfall 1: Branch-Sensitive Shift Identity

**What goes wrong:** `eml(log(x), exp(-b))` depends on the principal log path and is unsafe at `x = 0`; validation can fail or produce non-finite values if inputs hit singular points. [VERIFIED: src/eml_symbolic_regression/expression.py] [VERIFIED: local compiler probe]

**Why it happens:** `log_of(x)` is an EML identity for principal-branch log and the compiler validates on supplied numeric inputs. [VERIFIED: src/eml_symbolic_regression/expression.py] [VERIFIED: src/eml_symbolic_regression/compiler.py]

**How to avoid:** Keep the motif behind `compile_and_validate()` and use Michaelis positive domains away from zero. [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/compiler.py]

**Warning signs:** Validation reason becomes `validation_failed`, `max_abs_error` exceeds tolerance, or candidate verification loses high-precision recovery. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/verify.py]

### Pitfall 2: Matching Too Broadly

**What goes wrong:** A broad rational rewrite can mark unrelated expressions as reciprocal/saturation motifs. [VERIFIED: .planning/milestones/v1.6-phases/37-01-SUMMARY.md]

**Why it happens:** SymPy normalization can hide whether a denominator was present in the original structural form. [VERIFIED: .planning/milestones/v1.6-phases/37-01-SUMMARY.md]

**How to avoid:** Inspect `Mul` factors and `Pow(..., -1)` factors directly, as `_compile_direct_division()` already does. [VERIFIED: src/eml_symbolic_regression/compiler.py]

**Warning signs:** Macro hits appear on plain constants, reciprocal-only cases under the wrong macro name, denominator powers other than `-1`, or formulas outside unit-shift saturation. [VERIFIED: src/eml_symbolic_regression/compiler.py]

### Pitfall 3: Breaking Existing Macro Evidence

**What goes wrong:** New macro order can accidentally steal Arrhenius or Planck paths from `direct_division_template` or `scaled_exp_minus_one_template`. [VERIFIED: tests/test_compiler_warm_start.py]

**Why it happens:** `_compile_special()` checks macro hooks before generic lowering. [VERIFIED: src/eml_symbolic_regression/compiler.py]

**How to avoid:** Order `saturation_ratio_template` before `direct_division_template`, but require same-symbol numerator and unit-shift denominator; order `reciprocal_shift_template` only for `Pow(Add(Symbol, numeric), -1)`. [VERIFIED: local compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py]

**Warning signs:** Arrhenius no longer reports `direct_division_template`, Shockley no longer reports `scaled_exp_minus_one_template`, or Planck relaxed diagnostics lose the expected macro set. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md]

### Pitfall 4: Overclaiming Michaelis

**What goes wrong:** Strict compile and zero-noise same-AST warm start are reported as blind discovery. [VERIFIED: .planning/PROJECT.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

**Why it happens:** `claim_status == "recovered"` and `evidence_class == "same_ast"` coexist in the current artifact model for compiler warm-start paths. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: tests/test_benchmark_runner.py]

**How to avoid:** Use the Phase 50 Arrhenius pattern: report verifier `recovered` but evidence class `same_ast`, and write docs only after artifact validation. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md] [VERIFIED: tests/test_benchmark_runner.py]

**Warning signs:** Generated docs or aggregate tables group Michaelis with blind recovery, or a benchmark case uses `start_mode == "blind"` to represent compiler warm-start evidence. [VERIFIED: src/eml_symbolic_regression/benchmark.py]

## Code Examples

### Baseline Diagnostic Probe

```python
# Source: local Phase 51 probe against src/eml_symbolic_regression/compiler.py.
x = sp.Symbol("x")
diagnostic = diagnose_compile_expression(
    2 * x / (x + sp.Float("0.5")),
    CompilerConfig(variables=("x",), max_depth=13, max_nodes=256),
    {"x": np.linspace(0.25, 2.5, 12).astype(np.complex128)},
)
assert diagnostic["status"] == "unsupported"
assert diagnostic["strict"]["reason"] == CompileReason.DEPTH_EXCEEDED
assert diagnostic["relaxed"]["metadata"]["depth"] == 14
```

The current Michaelis-style expression is unsupported at strict depth 13 but validates in relaxed diagnostics at depth 14. [VERIFIED: local compiler probe]

### Proposed Unit-Shift Builder

```python
# Source: local Phase 51 probe using existing expression/compiler helpers.
def _unit_shift_expr(variable: str, offset: complex) -> Expr:
    return Eml(log_of(Var(variable)), Const(np.exp(-offset)))
```

This builder produced `x + 0.5` at depth 4 and node count 9 in the local probe. [VERIFIED: local compiler probe]

### Proposed Strict Test Shape

```python
# Source pattern: tests/test_compiler_warm_start.py.
def test_compile_michaelis_uses_saturation_ratio_template():
    spec = get_demo("michaelis_menten")
    splits = spec.make_splits(points=24, seed=0)
    result = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
        {spec.variable: splits[0].inputs[spec.variable]},
    )

    assert result.validation is not None
    assert result.validation.passed
    assert result.metadata.depth <= 13
    assert result.metadata.macro_diagnostics is not None
    assert "saturation_ratio_template" in result.metadata.macro_diagnostics["hits"]
```

The prototype result for the same formula had depth 12 and node count 41. [VERIFIED: local compiler probe]

### Proposed Warm-Start Artifact Test Shape

```python
# Source pattern: tests/test_benchmark_runner.py and Phase 50 Arrhenius artifact test.
assert artifact["run"]["formula"] == "michaelis_menten"
assert artifact["run"]["start_mode"] == "warm_start"
assert artifact["status"] == "same_ast_return"
assert artifact["claim_status"] == "recovered"
assert artifact["evidence_class"] == "same_ast"
assert artifact["stage_statuses"]["compiled_seed"] == "recovered"
assert artifact["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
assert artifact["stage_statuses"]["trained_exact_recovery"] == "recovered"
assert "saturation_ratio_template" in artifact["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"]
```

This follows the already verified Arrhenius same-AST evidence pattern. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md] [VERIFIED: tests/test_benchmark_runner.py]

## Recommended Approach

1. Add `reciprocal_shift_template` and `saturation_ratio_template` to `MACRO_RULES`, preserving existing macro names so diagnostics still report current rules. [VERIFIED: src/eml_symbolic_regression/compiler.py]
2. Add a private structural matcher for unit shifts with exactly one allowed `Symbol` and exactly one numeric literal offset. [VERIFIED: local compiler probe]
3. Add a private unit-shift builder that emits `Eml(log_of(Var(variable)), Const(np.exp(-offset)))` and records an assumption about principal-branch validation. [VERIFIED: local compiler probe] [VERIFIED: src/eml_symbolic_regression/expression.py]
4. Route `Pow(unit_shift, -1)` through `reciprocal_shift_template` before `_compile_power()` falls back to generic negative power. [VERIFIED: src/eml_symbolic_regression/compiler.py]
5. Route `a*x/(x+b)` through `saturation_ratio_template` before `_compile_direct_division()`, requiring the same variable in numerator and denominator. [VERIFIED: local compiler probe]
6. Keep `direct_division_template` for Arrhenius, Planck, and arbitrary numerator-over-denominator motifs that do not satisfy saturation matching. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md]
7. If strict Michaelis compiles at depth 12 as the prototype predicts, add a focused benchmark suite such as `v1.9-michaelis-evidence` with one zero-noise `michaelis-warm` case modeled on `v1.9-arrhenius-evidence`. [VERIFIED: local warm-start probe] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
8. If strict compile unexpectedly remains above depth 13, keep Michaelis unsupported and add only before/after diagnostic tests/artifacts showing material reduction. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]

## Verification Plan

Focused test additions should come before any docs update. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]

| Requirement | Test / Command | Expected Result |
|-------------|----------------|-----------------|
| MIC-01 | `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_reciprocal_shift_uses_template -q` | `1/(x+0.5)` strict-compiles at depth 10, node count 25, validation passes, and macro hits include `reciprocal_shift_template`. [VERIFIED: local compiler probe] |
| MIC-02 | `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_michaelis_uses_saturation_ratio_template -q` | `2*x/(x+0.5)` strict-compiles at depth 12, node count 41, validation passes, and macro hits include `saturation_ratio_template`. [VERIFIED: local compiler probe] |
| MIC-03 | `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_reciprocal_and_saturation_diagnostics_include_before_after_macro_metadata -q` | Diagnostics expose baseline depth/node counts, depth/node deltas, trace rules, and macro hits for both target expressions. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: local compiler probe] |
| MIC-04 | `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_michaelis_warm_start_returns_same_ast_and_verifies -q` if strict support lands | Zero-noise warm start returns `same_ast_return`, verifier status `recovered`, and `changed_slot_count == 0`. [VERIFIED: local warm-start probe] |
| Regression | `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_arrhenius_uses_direct_division_template tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_arrhenius_same_ast_evidence tests/test_compiler_warm_start.py::test_cli_reports_planck_as_stretch_without_promotion -q` | Arrhenius remains `direct_division_template`, Arrhenius remains `same_ast`, and Planck remains stretch/unsupported under default gates. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md] [VERIFIED: tests/test_compiler_warm_start.py] |
| Benchmark artifact if strict support lands | `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_michaelis_evidence_suite_contains_exact_warm_start_case tests/test_benchmark_runner.py::test_michaelis_warm_benchmark_records_same_ast_evidence -q` | Focused suite expands one `michaelis-warm` run and artifact records `same_ast_return`, verifier `recovered`, macro hit, and evidence class `same_ast`. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: tests/test_benchmark_runner.py] |

Full focused verification after implementation should run:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_compiler_warm_start.py \
  tests/test_benchmark_contract.py \
  tests/test_benchmark_runner.py \
  -q
```

This command covers compiler macros, CLI behavior, benchmark suite contracts, and benchmark artifact regime labeling. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_contract.py] [VERIFIED: tests/test_benchmark_runner.py]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Generic arithmetic lowering for reciprocal and division | Explicit macro layer with `direct_division_template` and `scaled_exp_minus_one_template` | Phase 37 [VERIFIED: .planning/milestones/v1.6-phases/37-VERIFICATION.md] | Shockley reached warm-start evidence while Michaelis stayed strict-unsupported with relaxed diagnostics. [VERIFIED: .planning/milestones/v1.6-phases/37-VERIFICATION.md] |
| Direct division for Michaelis | Proposed saturation-specific structural macro using unit-shift denominator | Phase 51 planned [VERIFIED: .planning/ROADMAP.md] | Prototype reduces Michaelis from strict-unsupported depth 14 to strict-supported depth 12. [VERIFIED: local compiler probe] |
| Arrhenius same-AST evidence | Existing focused suite `v1.9-arrhenius-evidence` | Phase 50 [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md] | Phase 51 should copy the evidence labeling pattern if Michaelis strict support lands. [VERIFIED: tests/test_benchmark_runner.py] |

**Deprecated/outdated:**
- Treating Michaelis relaxed compile as recovery is not valid because current CLI and benchmark code only warm-start after strict compile success. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
- Using broad rational simplification for macro detection is outdated because Phase 37 replaced it after accidental macro hits. [VERIFIED: .planning/milestones/v1.6-phases/37-01-SUMMARY.md]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Package, CLI, tests | yes [VERIFIED: `python --version`] | 3.11.5 [VERIFIED: `python --version`] | none required. [VERIFIED: pyproject.toml] |
| pytest | Focused test verification | yes [VERIFIED: `python -m pytest --version`] | 7.4.0 [VERIFIED: `python -m pytest --version`] | none required. [VERIFIED: pyproject.toml] |
| NumPy | Compiler validation and demo targets | yes [VERIFIED: local version probe] | 1.26.4 [VERIFIED: local version probe] | none required. [VERIFIED: pyproject.toml] |
| SymPy | Compiler source expressions and matching | yes [VERIFIED: local version probe] | 1.14.0 [VERIFIED: local version probe] | none required. [VERIFIED: pyproject.toml] |
| PyTorch | Warm-start same-AST probe | yes [VERIFIED: local version probe] | 2.10.0 [VERIFIED: local version probe] | skip warm-start promotion if unavailable. [VERIFIED: src/eml_symbolic_regression/warm_start.py] |
| mpmath | High-precision verifier | yes [VERIFIED: local version probe] | 1.3.0 [VERIFIED: local version probe] | no acceptable recovery fallback. [VERIFIED: src/eml_symbolic_regression/verify.py] |

**Missing dependencies with no fallback:** none found for Phase 51. [VERIFIED: local version probe]

**Missing dependencies with fallback:** none found for Phase 51. [VERIFIED: local version probe]

## Security Domain

This phase does not introduce authentication, sessions, access control, persistence, networking, or cryptography. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/cli.py]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no [VERIFIED: source audit] | Not applicable because no authentication surface changes. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| V3 Session Management | no [VERIFIED: source audit] | Not applicable because no session surface exists in this phase. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| V4 Access Control | no [VERIFIED: source audit] | Not applicable because Phase 51 changes local compiler/test behavior only. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md] |
| V5 Input Validation | yes [VERIFIED: src/eml_symbolic_regression/compiler.py] | Keep structural SymPy matching fail-closed and require `compile_and_validate()` before accepting macro output. [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| V6 Cryptography | no [VERIFIED: source audit] | Not applicable because no cryptographic behavior changes. [VERIFIED: src/eml_symbolic_regression/compiler.py] |

### Known Threat Patterns for This Phase

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Dishonest macro hit from overbroad matching | Tampering / Repudiation | Match local SymPy structure directly and serialize trace plus baseline diagnostics. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: .planning/milestones/v1.6-phases/37-01-SUMMARY.md] |
| Recovery overclaim from strict compile or same-AST return | Information disclosure / Repudiation | Preserve verifier-owned `recovered` and benchmark `evidence_class == "same_ast"` labels. [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Domain singularity from reciprocal or log | Denial of service / Integrity | Validate on configured inputs and keep unsafe expressions fail-closed. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/datasets.py] |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The post-implementation macro code can preserve the prototype depth 10 and depth 12 results exactly. [ASSUMED] | Recommended Approach | If helper implementation differs from the prototype, Michaelis may remain strict-unsupported and Phase 51 should record depth reduction rather than recovery. |
| A2 | A focused suite name such as `v1.9-michaelis-evidence` is acceptable if strict support lands. [ASSUMED] | Verification Plan | If the project wants no new suite until Phase 53, use CLI and tests only and leave broad artifact packaging for Phase 53. |

## Open Questions (RESOLVED)

1. **Should saturation artifacts report both `saturation_ratio_template` and `reciprocal_shift_template`, or only the top-level saturation macro?** [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md]
   - What we know: reciprocal-only tests should report `reciprocal_shift_template`, and Michaelis should report `saturation_ratio_template`. [VERIFIED: .planning/REQUIREMENTS.md]
   - Decision: record `saturation_ratio_template` as the top-level macro hit for Michaelis-style saturation ratios, and keep `reciprocal_shift_template` for reciprocal-only expressions. Do not force nested reciprocal macro hits inside saturation artifacts unless a future trace schema explicitly needs nested provenance.

2. **Should Phase 51 commit a permanent Michaelis evidence artifact if same-AST recovery lands?** [VERIFIED: .planning/ROADMAP.md]
   - What we know: Phase 50 committed focused Arrhenius evidence after tests passed. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md]
   - Decision: add one focused benchmark suite and permanent artifact if strict support lands, modeled on `v1.9-arrhenius-evidence`; otherwise add a focused unsupported diagnostic artifact that records the measured depth/node reduction. Broad paper-facing packaging still belongs to Phase 53.

## Sources

### Primary (HIGH confidence)

- `.planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-CONTEXT.md` - locked Phase 51 motifs, constraints, success criteria, and evidence path. [VERIFIED]
- `.planning/REQUIREMENTS.md` - MIC-01 through MIC-04 and out-of-scope constraints. [VERIFIED]
- `.planning/ROADMAP.md` - Phase 51 role in v1.9 and Phase 53 packaging boundary. [VERIFIED]
- `.planning/PROJECT.md` - project constraints, evidence-regime separation, and current v1.9 target features. [VERIFIED]
- `.planning/STATE.md` - accumulated decisions from Phase 37, Phase 49, and Phase 50. [VERIFIED]
- `.planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md` - Arrhenius same-AST artifact pattern and Michaelis/Planck guard status. [VERIFIED]
- `sources/FOR_DEMO.md` - Michaelis-Menten showcase rationale and normalized demo source. [VERIFIED]
- `src/eml_symbolic_regression/compiler.py` - macro layer, compiler gates, diagnostics, validation, and EML arithmetic identities. [VERIFIED]
- `src/eml_symbolic_regression/datasets.py` - `michaelis_menten` formula, domains, and provenance. [VERIFIED]
- `src/eml_symbolic_regression/cli.py` - strict compile and warm-start CLI flow. [VERIFIED]
- `src/eml_symbolic_regression/benchmark.py` - benchmark suites, strict compile flow, same-AST evidence classification, and metrics. [VERIFIED]
- `tests/test_compiler_warm_start.py` - current compiler macro, CLI unsupported, Arrhenius, Michaelis, and Planck regression expectations. [VERIFIED]
- `tests/test_benchmark_contract.py` - built-in suite registry and focused Arrhenius contract pattern. [VERIFIED]
- `tests/test_benchmark_runner.py` - benchmark artifact and evidence-class regression pattern. [VERIFIED]
- Local compiler probe - baseline and prototype depth/node/macro/validation diagnostics for `1/(x+0.5)` and `2*x/(x+0.5)`. [VERIFIED]
- Local warm-start probe - prototype Michaelis exact tree verifier `recovered` and zero-noise `same_ast_return`. [VERIFIED]

### Secondary (MEDIUM confidence)

- `.planning/milestones/v1.6-phases/37-01-SUMMARY.md` - historical decision to avoid broad rationalization and preserve honest direct-division macro hits. [VERIFIED]
- `.planning/milestones/v1.6-phases/37-VERIFICATION.md` - Phase 37 macro-diagnostics and unsupported-depth behavior. [VERIFIED]
- `.planning/phases/50-arrhenius-exact-warm-start-demo/50-RESEARCH.md` - prior research pattern for same-AST evidence artifacts. [VERIFIED]

### Tertiary (LOW confidence)

- None. [VERIFIED: source list]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH because versions and dependency declarations were verified locally and in `pyproject.toml`. [VERIFIED: local version probe] [VERIFIED: pyproject.toml]
- Architecture: HIGH because compiler, CLI, benchmark, and tests were read directly. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
- Baseline diagnostics: HIGH because both requested probes were executed locally. [VERIFIED: local compiler probe]
- Recommended motif implementation: HIGH for mathematical/diagnostic feasibility, MEDIUM for exact post-edit depth until the planner implements and tests it. [VERIFIED: local compiler probe] [ASSUMED]
- Evidence artifact path: MEDIUM because it reuses the verified Phase 50 pattern but the exact suite name is not yet locked. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-VERIFICATION.md] [ASSUMED]

**Research date:** 2026-04-17 [VERIFIED: environment_context]
**Valid until:** 2026-05-17, or until `compiler.py`, `benchmark.py`, or `tests/test_compiler_warm_start.py` change materially. [ASSUMED]
