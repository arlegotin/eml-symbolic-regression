# Phase 50: Arrhenius Exact Warm-Start Demo - Research

**Researched:** 2026-04-17 [VERIFIED: environment_context]
**Domain:** Existing Python/PyTorch EML demo registry, compiler diagnostics, zero-noise warm-start evidence, and benchmark artifact reporting. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
**Confidence:** HIGH. [VERIFIED: focused compiler/warm-start probe for exp(-0.8/x)]

<user_constraints>
## User Constraints (from CONTEXT.md)

All bullets in this section are copied or scoped directly from `.planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md`. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

### Locked Decisions

#### Demo Definition
- Use a dimensionless transformed input `x` rather than raw SI temperature, matching the FOR_DEMO warning to avoid unit-heavy scaling.
- Define the target as `exp(-0.8 / x)` with strictly positive train, held-out, and extrapolation domains safely away from zero.
- Keep the demo source linkage pointed to `sources/FOR_DEMO.md` Arrhenius law and mark it normalized/dimensionless.
- Add the demo through the existing `DemoSpec` registry so CLI, verifier, benchmark, and proof helpers can consume it consistently.

#### Compiler and Warm-Start Evidence
- Treat Arrhenius as strict compile support, not a relaxed/stretch diagnostic.
- Require compiler metadata to include `direct_division_template` for the reciprocal-temperature exponent structure.
- Require zero-noise compiler warm-start to return the same exact AST and final verifier status `recovered`.
- Preserve the existing evidence taxonomy: same-AST warm-start return is not blind discovery.

#### Artifacts and Tests
- Add focused dataset, compiler, CLI, and benchmark runner tests near the existing Beer-Lambert/Shockley warm-start coverage.
- Add a reproducible artifact/report path that records compile depth, macro hits, warm-start status, verifier status, and evidence regime.
- Keep Michaelis-Menten and Planck unsupported/stretch behavior unchanged while adding Arrhenius.
- Prefer small campaign/benchmark registry extensions over broad campaign reruns in this phase.

### Claude's Discretion

Use the existing compiler/warm-start CLI and benchmark machinery wherever possible. If an implementation choice can reuse a Beer-Lambert or Shockley pattern without weakening regime labels, reuse it rather than creating a new artifact format.

### Deferred Ideas (OUT OF SCOPE)

Black-box neural-network extrapolation comparisons and raw-SI Arrhenius scaling are deferred. This phase proves the normalized exact warm-start path and records honest evidence regimes only.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ARR-01 | Developer can generate a normalized Arrhenius demo dataset for `exp(-0.8/x)` over positive domains safely away from zero. [VERIFIED: .planning/REQUIREMENTS.md] | Add `arrhenius` to `demo_specs()` as a `DemoSpec` using the locked positive domains and `SympyCandidate`; `DemoSpec.make_splits()` already produces train, held-out, and extrapolation splits with deterministic seeded jitter. [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] |
| ARR-02 | Developer can strictly compile the Arrhenius target within the supported depth gate and inspect macro diagnostics including `direct_division_template`. [VERIFIED: .planning/REQUIREMENTS.md] | A focused no-edit probe compiled `exp(-0.8/x)` at depth 7, node count 19, with macro hits `["direct_division_template"]`, baseline depth 11, and validation passed under `CompilerConfig(max_depth=13, max_nodes=256)`. [VERIFIED: focused compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| ARR-03 | Developer can run a zero-noise Arrhenius compiler warm start that returns the same exact AST and verifier status `recovered`. [VERIFIED: .planning/REQUIREMENTS.md] | A focused no-edit probe using train `(0.5, 3.0)`, held-out `(0.6, 2.7)`, extrapolation `(3.1, 4.2)`, `warm_steps=1`, and `warm_noise=0.0` returned `same_ast_return`, verifier status `recovered`, mechanism `same_ast_return`, and `changed_slot_count=0`. [VERIFIED: focused warm-start probe] [VERIFIED: src/eml_symbolic_regression/warm_start.py] |
| ARR-04 | Developer can reproduce an Arrhenius benchmark or report artifact with compile depth, warm-start status, verifier status, and regime labeling. [VERIFIED: .planning/REQUIREMENTS.md] | Existing CLI demo reports and benchmark artifacts already serialize `compiled_eml.metadata.depth`, `compiled_eml.metadata.macro_diagnostics`, `stage_statuses`, `warm_start_eml.verification`, `warm_start_eml.diagnosis`, `claim_status`, `evidence_class`, and `metrics`; add an Arrhenius-focused benchmark case rather than a new artifact schema. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
</phase_requirements>

## Summary

Phase 50 is low implementation risk because the current compiler already supports the exact symbolic shape required for normalized Arrhenius, `exp(-0.8/x)`, through the reusable `direct_division_template` macro. [VERIFIED: focused compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py] The planner should not allocate compiler-algorithm work unless a regression appears during implementation; the primary work is to add the built-in demo, lock strict compiler diagnostics in tests, add CLI and benchmark evidence tests, and update docs after the artifact path is proven. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py]

The exact evidence path should remain regime-honest: a zero-noise warm start returning the same AST is `same_ast_return` and `evidence_class == "same_ast"`, while the top-level verifier-owned claim can still be `recovered` because the snapped exact EML AST passes train, held-out, extrapolation, and high-precision checks. [VERIFIED: src/eml_symbolic_regression/warm_start.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: src/eml_symbolic_regression/verify.py]

**Primary recommendation:** Add `arrhenius` through `DemoSpec`, prove strict compile depth 7 with `direct_division_template`, add `demo arrhenius --warm-start-eml` and a focused `arrhenius-warm` benchmark path, and document the command only after the JSON artifact proves `same_ast_return`, verifier `recovered`, and evidence regime `same_ast`. [VERIFIED: focused compiler/warm-start probe] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Normalized Arrhenius dataset | Python dataset registry | Verifier | `DemoSpec` owns target functions, SymPy candidates, domains, provenance, and split construction for built-in demos. [VERIFIED: src/eml_symbolic_regression/datasets.py] |
| Strict compile support | Compiler | CLI and benchmark runner | `compile_and_validate()` owns exact EML compilation, validation, depth gates, node gates, and macro diagnostics; CLI and benchmark code only call it and serialize the result. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Zero-noise warm-start return | Warm-start/optimizer | Verifier | `fit_warm_started_eml_tree()` embeds a compiled AST, applies deterministic perturbation, trains/snaps, classifies `same_ast_return`, and attaches verifier output when splits are supplied. [VERIFIED: src/eml_symbolic_regression/warm_start.py] |
| Recovery status | Verifier | CLI and benchmark runner | `verify_candidate()` is the owner of `recovered` versus `verified_showcase`; CLI and benchmark payloads promote `claim_status` based on verifier status, not training loss alone. [VERIFIED: src/eml_symbolic_regression/verify.py] [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Evidence regime labeling | Benchmark/proof taxonomy | Campaign/report docs | `evidence_class_for_payload()` maps compiler warm-start `same_ast_return` to `same_ast`, keeping same-AST return separate from blind recovery. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: src/eml_symbolic_regression/proof.py] |
| Reproducible artifact path | CLI and benchmark runner | README/docs | Demo reports write JSON to `--output`; benchmark runs write per-run artifacts plus suite/aggregate outputs under the configured artifact root. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |

## Project Constraints (from AGENTS.md)

- EML semantics, complete-tree construction, snapping, and complex arithmetic must stay grounded in `sources/paper.pdf` and `sources/NORTH_STAR.md`. [VERIFIED: AGENTS.md]
- Training defaults to PyTorch `complex128`, with clamps only in training mode and faithful verification afterward. [VERIFIED: AGENTS.md] [VERIFIED: src/eml_symbolic_regression/optimize.py]
- A candidate is not recovered from training loss alone; it must pass held-out, extrapolation, and high-precision checks. [VERIFIED: AGENTS.md] [VERIFIED: src/eml_symbolic_regression/verify.py]
- v1 must avoid overselling blind deep recovery because the source paper and project state report rapid degradation beyond shallow depths. [VERIFIED: AGENTS.md] [VERIFIED: .planning/STATE.md]
- Showcase examples must come from `sources/FOR_DEMO.md`, favoring normalized, dimensionless, visually distinctive laws. [VERIFIED: AGENTS.md] [VERIFIED: sources/FOR_DEMO.md]
- File-changing work must stay inside the GSD workflow unless explicitly bypassed; this research artifact is part of the requested GSD workflow. [VERIFIED: AGENTS.md] [VERIFIED: user request]
- No project-local `CLAUDE.md` or project-local skills were found, so there are no extra local directives beyond `AGENTS.md` and GSD defaults. [VERIFIED: `test -f CLAUDE.md`] [VERIFIED: `find .claude/skills .agents/skills -maxdepth 2 -name SKILL.md`]

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11.5 local; `>=3.11,<3.13` in `pyproject.toml` | Package, CLI, tests, and benchmark orchestration. [VERIFIED: `python --version`] [VERIFIED: pyproject.toml] | The current package and CLI are Python modules under `src/`, and `pyproject.toml` defines the console script. [VERIFIED: pyproject.toml] [VERIFIED: src/eml_symbolic_regression/cli.py] |
| NumPy | 1.26.4 local; `>=1.26` in `pyproject.toml` | Demo target arrays, deterministic split targets, compiler validation inputs. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | `DemoSpec.make_splits()`, compiler validation, and benchmark execution already use NumPy arrays. [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| SymPy | 1.14.0 local; `>=1.14` in `pyproject.toml` | Catalog candidate expression and compiler source expression. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | Demo specs store `SympyCandidate` formulas and the compiler consumes SymPy expressions. [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| PyTorch | 2.10.0 local; `>=2.10` in `pyproject.toml` | Soft EML warm-start training and exact snap return. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | `fit_warm_started_eml_tree()` calls the existing PyTorch optimizer path through `fit_eml_tree()`. [VERIFIED: src/eml_symbolic_regression/warm_start.py] [VERIFIED: src/eml_symbolic_regression/optimize.py] |
| mpmath | 1.3.0 local; `>=1.3` in `pyproject.toml` | High-precision verification checks. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | `verify_candidate()` performs mpmath point checks when numeric checks are not decisively failed. [VERIFIED: src/eml_symbolic_regression/verify.py] |
| pytest | 7.4.0 local; `>=7.4` dev dependency | Focused dataset, compiler, CLI, and benchmark regression tests. [VERIFIED: `python -m pytest --version`] [VERIFIED: pyproject.toml] | Existing tests already cover compiler warm starts and benchmark artifacts with pytest. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `argparse` | Python stdlib | CLI argument parsing for `demo`, `benchmark`, and report commands. [VERIFIED: src/eml_symbolic_regression/cli.py] | Use existing parser options such as `--warm-start-eml`, `--max-compile-depth`, `--max-warm-depth`, `--warm-noise`, and `--output`. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| `json` / `pathlib` | Python stdlib | JSON report writing and artifact paths. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] | Use the existing `_write_json()` paths instead of introducing a report format. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| `hashlib` | Python stdlib | Deterministic dataset manifest hashes. [VERIFIED: src/eml_symbolic_regression/datasets.py] | Use `proof_dataset_manifest("arrhenius", ...)` after adding the demo to produce split signatures and provenance. [VERIFIED: src/eml_symbolic_regression/datasets.py] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Existing `DemoSpec` registry | A one-off Arrhenius generator | Do not use the one-off generator because CLI, verifier, benchmark, and proof helpers all consume `DemoSpec` consistently. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/datasets.py] |
| Existing `direct_division_template` macro | An Arrhenius-specific compiler recognizer | Do not add a formula-specific recognizer because the current reusable direct-division macro already compiles `exp(-0.8/x)` within the strict gate. [VERIFIED: focused compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| Existing JSON demo/benchmark artifacts | A new Arrhenius artifact schema | Do not add a new schema because existing demo and benchmark payloads already carry compile depth, macro hits, warm-start status, verifier status, and evidence class. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Focused benchmark case | Broad campaign rerun | Do not launch broad campaigns in this phase because the locked context asks for small registry extensions rather than broad campaign reruns. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] |
| Normalized `x` domain | Raw SI temperature and constants | Do not use raw SI scaling because `sources/FOR_DEMO.md` cautions to use transformed or nondimensionalized temperature input for Arrhenius. [CITED: sources/FOR_DEMO.md] |

**Installation:**

```bash
# No new packages are required for Phase 50; use the existing project environment.
python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_runner.py
```

**Version verification:** Package versions were verified locally with `python --version`, `python -m pytest --version`, and `PYTHONPATH=src python -c 'import numpy, sympy, mpmath, torch; ...'`. [VERIFIED: local version probes]

## Architecture Patterns

### System Architecture Diagram

```text
sources/FOR_DEMO.md Arrhenius guidance
        |
        v
DemoSpec("arrhenius", target=np.exp(-0.8/x), SymPy candidate, positive domains)
        |
        +--> make_splits(points, seed)
        |        |
        |        v
        |   train / heldout / extrapolation DataSplit objects
        |
        v
CLI demo or BenchmarkRun
        |
        v
compile_and_validate(SymPy expression, max_depth=13, max_nodes=256)
        |
        +--> strict success: exact EML AST, metadata.depth=7, macro hit direct_division_template
        |        |
        |        v
        |   verify_candidate(compiled AST) -> compiled_seed=recovered
        |        |
        |        v
        |   fit_warm_started_eml_tree(noise=0.0, warm_steps=1)
        |        |
        |        v
        |   snap + compare to compiled AST + verify_candidate()
        |        |
        |        v
        |   status=same_ast_return, verifier=recovered, evidence_class=same_ast
        |
        +--> strict failure path remains unsupported diagnostic
                 |
                 v
          diagnose_compile_expression() relaxed metadata, no promotion
```

This diagram uses the existing CLI/benchmark flow and strict failure path rather than adding an Arrhenius-only control flow. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: src/eml_symbolic_regression/compiler.py]

### Recommended Project Structure

```text
src/eml_symbolic_regression/
  datasets.py       # Add arrhenius DemoSpec and provenance.
  benchmark.py      # Add a focused arrhenius-warm benchmark path.
  cli.py            # No parser changes expected; existing demo options should work.
tests/
  test_compiler_warm_start.py  # Add strict compile, zero-noise warm-start, and CLI checks.
  test_benchmark_runner.py     # Add artifact/evidence-class regression check.
  test_benchmark_contract.py   # Update suite registry/formula coverage if a suite is added.
  test_proof_dataset_manifest.py # Add positive-domain/provenance assertions if useful.
docs/
  IMPLEMENTATION.md # Add Arrhenius to demo ladder after tests prove artifact path.
README.md          # Add command and claim-language note after tests prove artifact path.
```

These are the code areas named by the phase prompt and the existing files that own the same Beer-Lambert/Shockley behavior. [VERIFIED: user request] [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py] [VERIFIED: docs/IMPLEMENTATION.md] [VERIFIED: README.md]

### Pattern 1: Add a Built-In Demo Through `DemoSpec`

**What:** Add `arrhenius` to the dictionary returned by `demo_specs()`. [VERIFIED: src/eml_symbolic_regression/datasets.py]

**When to use:** Use this pattern for every built-in demo that must flow through CLI, verifier, benchmark, and proof dataset manifests. [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

**Example:**

```python
# Source pattern: src/eml_symbolic_regression/datasets.py and Phase 50 CONTEXT.md.
"arrhenius": DemoSpec(
    name="arrhenius",
    variable="x",
    description="Normalized Arrhenius law with reciprocal-temperature exponent.",
    target=lambda a: np.exp(-0.8 / a).astype(np.complex128),
    candidate=_sympy_candidate(sp.exp(-sp.Float("0.8") / x), "x", "arrhenius_catalog"),
    train_domain=(0.5, 3.0),
    heldout_domain=(0.6, 2.7),
    extrap_domain=(3.1, 4.2),
    source_document="sources/FOR_DEMO.md",
    source_linkage="Arrhenius law normalized reciprocal-temperature demo",
    normalized_dimensionless=True,
)
```

Use `sp.exp(-sp.Float("0.8") / x)` so the reciprocal-temperature exponent is visible to the compiler as a division motif. [VERIFIED: focused compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py]

### Pattern 2: Treat Strict Compilation as the Gate

**What:** The strict compiler path should call `compile_and_validate()` with the current gates and assert `metadata.unsupported_reason is None`, `metadata.depth <= 13`, validation passed, and macro hits include exactly `direct_division_template`. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: focused compiler probe]

**When to use:** Use this before any warm-start assertion so unsupported compile results cannot be promoted by training. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

**Example:**

```python
# Source pattern: tests/test_compiler_warm_start.py.
spec = get_demo("arrhenius")
splits = spec.make_splits(points=24, seed=0)
result = compile_and_validate(
    spec.candidate.to_sympy(),
    CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
    {spec.variable: splits[0].inputs[spec.variable]},
)

assert result.validation is not None
assert result.validation.passed
assert result.metadata.depth <= 13
assert result.metadata.macro_diagnostics["hits"] == ["direct_division_template"]
```

The current no-edit probe measured depth 7 and node count 19 for this expression. [VERIFIED: focused compiler probe]

### Pattern 3: Use Zero-Noise Warm Start for Same-AST Evidence

**What:** Compile the source expression, embed it into a compatible soft tree, use `PerturbationConfig(noise_scale=0.0)`, train for the minimal existing same-AST pattern, snap, and verify all splits. [VERIFIED: src/eml_symbolic_regression/warm_start.py] [VERIFIED: tests/test_compiler_warm_start.py]

**When to use:** Use this for ARR-03 because the locked requirement is exact warm-start return, not blind discovery. [VERIFIED: .planning/REQUIREMENTS.md] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

**Example:**

```python
# Source pattern: tests/test_compiler_warm_start.py and focused warm-start probe.
result = fit_warm_started_eml_tree(
    splits[0].inputs,
    splits[0].target,
    TrainingConfig(depth=compiled.metadata.depth, variables=(spec.variable,), steps=1, restarts=1, seed=0),
    compiled.expression,
    perturbation_config=PerturbationConfig(seed=0, noise_scale=0.0),
    verification_splits=splits,
    compiler_metadata=compiled.metadata.as_dict(),
)

assert result.status == "same_ast_return"
assert result.verification is not None
assert result.verification.status == "recovered"
assert result.manifest["diagnosis"]["mechanism"] == "same_ast_return"
assert result.manifest["diagnosis"]["changed_slot_count"] == 0
```

The current no-edit probe returned exactly these status values for the locked domains. [VERIFIED: focused warm-start probe]

### Pattern 4: Add a Focused Benchmark Evidence Path

**What:** Add a small `warm_start` benchmark case such as `arrhenius-warm` with `formula="arrhenius"`, `warm_steps=1`, `perturbation_noise=(0.0,)`, and tags that make the regime explicit. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

**When to use:** Use this to satisfy ARR-04 without running broad standard/showcase campaigns. [VERIFIED: .planning/REQUIREMENTS.md] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

**Example:**

```python
# Source pattern: src/eml_symbolic_regression/benchmark.py.
_case(
    "arrhenius-warm",
    "arrhenius",
    "warm_start",
    warm_steps=1,
    tags=("v1.9", "arrhenius", "warm_start", "same_ast"),
    expect_recovery=True,
)
```

The per-run artifact should assert `status == "same_ast_return"`, `claim_status == "recovered"`, `evidence_class == "same_ast"`, `compiled_eml.metadata.depth <= 13`, and `compiled_eml.metadata.macro_diagnostics.hits == ["direct_division_template"]`. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: tests/test_benchmark_runner.py]

### Anti-Patterns to Avoid

- **Formula-specific Arrhenius compiler branch:** The direct-division macro already covers the target expression, and project requirements forbid formula-specific hardcoded recognizers. [VERIFIED: focused compiler probe] [VERIFIED: .planning/REQUIREMENTS.md]
- **Relaxed diagnostic promotion:** A strict compiler success is required for Arrhenius; relaxed metadata is only for unsupported/stretch reporting. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/compiler.py]
- **Raw-SI temperature dataset:** The phase locks normalized `x`, and `sources/FOR_DEMO.md` cautions against raw SI scaling for Arrhenius. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [CITED: sources/FOR_DEMO.md]
- **Calling same-AST warm start blind discovery:** README and benchmark taxonomy already state that same-AST return is useful basin evidence, not blind discovery. [VERIFIED: README.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
- **Mutating Michaelis-Menten or Planck outcomes:** The context explicitly requires their unsupported/stretch behavior to remain unchanged in this phase. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dataset generation | A separate Arrhenius sampler | `DemoSpec.make_splits()` | It already creates deterministic train, held-out, and extrapolation `DataSplit` objects and plugs into proof dataset manifests. [VERIFIED: src/eml_symbolic_regression/datasets.py] |
| SymPy-to-EML compilation | An Arrhenius recognizer | `compile_and_validate()` and `direct_division_template` | The existing compiler already validates `exp(-0.8/x)` strictly at depth 7 and records macro diagnostics. [VERIFIED: focused compiler probe] [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| Warm-start embedding/training | A custom exact-AST return checker | `fit_warm_started_eml_tree()` | It already embeds compiled ASTs, applies deterministic perturbation, trains, snaps, compares ASTs, verifies splits, and records diagnosis. [VERIFIED: src/eml_symbolic_regression/warm_start.py] |
| Recovery decision | A training-loss threshold | `verify_candidate()` | The verifier owns `recovered` and checks numeric splits plus mpmath points. [VERIFIED: src/eml_symbolic_regression/verify.py] |
| Evidence regime labels | Manual `evidence_class` assignment in suite JSON | `evidence_class_for_payload()` | The benchmark validator rejects supplied `evidence_class`, and execution derives it from the payload. [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Artifact/report writing | A new report writer | CLI `_write_json()` and benchmark `run_benchmark_suite()` | Existing reports already carry dataset manifests, provenance, compiler metadata, warm-start manifests, metrics, timing, and evidence class. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] |

**Key insight:** Phase 50 should compose existing registry, compiler, warm-start, verifier, and benchmark contracts; custom logic would increase claim risk without adding capability. [VERIFIED: focused compiler/warm-start probe] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

## Common Pitfalls

### Pitfall 1: Accidentally Hiding the Division Motif

**What goes wrong:** The candidate expression is encoded in a way that does not expose the `-0.8 / x` denominator structure, so the compiler may miss `direct_division_template`. [VERIFIED: src/eml_symbolic_regression/compiler.py]

**Why it happens:** `_compile_direct_division()` looks for `Pow(..., -1)` denominator factors inside a SymPy `Mul`; `sp.exp(-sp.Float("0.8") / x)` produces the desired motif in the exponent. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: focused compiler probe]

**How to avoid:** Use `candidate=_sympy_candidate(sp.exp(-sp.Float("0.8") / x), "x", "arrhenius_catalog")` and assert the macro hit in tests. [VERIFIED: focused compiler probe]

**Warning signs:** `macro_diagnostics["hits"]` is empty or does not equal `["direct_division_template"]`, or strict compile depth rises above the current measured depth 7. [VERIFIED: focused compiler probe]

### Pitfall 2: Letting Jitter Undermine Positive-Domain Guarantees

**What goes wrong:** Tests only check configured domain tuples and miss actual sampled split values. [VERIFIED: src/eml_symbolic_regression/datasets.py]

**Why it happens:** `DemoSpec.make_splits()` adds seeded `0.2%` domain-width jitter to linspace samples. [VERIFIED: src/eml_symbolic_regression/datasets.py]

**How to avoid:** Use domains far from zero, such as train `(0.5, 3.0)`, held-out `(0.6, 2.7)`, and extrapolation `(3.1, 4.2)`, then assert generated split inputs are positive for the test seed. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/datasets.py]

**Warning signs:** A test only asserts `spec.train_domain[0] > 0` and never inspects `split.inputs[spec.variable].min()`. [VERIFIED: src/eml_symbolic_regression/datasets.py]

### Pitfall 3: Confusing `same_ast_return` With Top-Level `recovered`

**What goes wrong:** Reports or docs imply the engine discovered Arrhenius blindly because top-level `claim_status` is `recovered`. [VERIFIED: README.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

**Why it happens:** CLI and benchmark payloads can promote `claim_status` to `recovered` when the post-training exact EML verifies, while benchmark `status` remains `same_ast_return` and `evidence_class` remains `same_ast`. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

**How to avoid:** Tests must assert both `stage_statuses["warm_start_attempt"] == "same_ast_return"` and verifier status `recovered`; docs must state this is exact warm-start/basin evidence. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py] [VERIFIED: README.md]

**Warning signs:** A new doc line says "blind recovery" or "discovered" for the Arrhenius warm-start path. [VERIFIED: .planning/PROJECT.md] [VERIFIED: README.md]

### Pitfall 4: Broad Campaign Churn

**What goes wrong:** The implementation changes historical campaign presets or launches broad reruns to prove one formula. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

**Why it happens:** Existing standard/showcase suites already contain related warm-start rows, but Phase 50 only needs a focused artifact path. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]

**How to avoid:** Add a focused Arrhenius benchmark case or focused v1.9 Arrhenius suite and run it through `--case arrhenius-warm`. [VERIFIED: src/eml_symbolic_regression/benchmark.py]

**Warning signs:** Tests become slow because they run a full campaign or multiple seeds/noise levels that are not required by ARR-04. [VERIFIED: .planning/REQUIREMENTS.md]

### Pitfall 5: Regressing Unsupported Stretch Rows

**What goes wrong:** Changes made for Arrhenius alter Michaelis-Menten or Planck strict/relaxed diagnostics. [VERIFIED: tests/test_compiler_warm_start.py]

**Why it happens:** Arrhenius shares `direct_division_template` with Michaelis-Menten and Planck relaxed diagnostics. [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: tests/test_compiler_warm_start.py]

**How to avoid:** Keep the compiler unchanged unless implementation proves a real bug, and rerun the existing Michaelis-Menten and Planck unsupported tests after adding Arrhenius. [VERIFIED: focused compiler probe] [VERIFIED: tests/test_compiler_warm_start.py]

**Warning signs:** `test_cli_reports_michaelis_menten_depth_gate_without_promotion` or `test_cli_reports_planck_as_stretch_without_promotion` starts failing. [VERIFIED: tests/test_compiler_warm_start.py]

## Code Examples

Verified patterns from existing sources and focused probes:

### Dataset Positive-Domain Test

```python
# Source: src/eml_symbolic_regression/datasets.py and Phase 50 CONTEXT.md.
def test_arrhenius_demo_uses_positive_normalized_domains():
    spec = get_demo("arrhenius")

    assert spec.variable == "x"
    assert spec.normalized_dimensionless is True
    assert spec.source_document == "sources/FOR_DEMO.md"
    assert str(spec.candidate.to_sympy()) == "exp(-0.8/x)"

    splits = spec.make_splits(points=24, seed=0)
    assert {split.name for split in splits} == {"train", "heldout", "extrapolation"}
    assert all(split.inputs[spec.variable].min() > 0.0 for split in splits)
```

This test covers the actual sampled values, not only the declared domain tuples. [VERIFIED: src/eml_symbolic_regression/datasets.py]

### Strict Compile Test

```python
# Source: tests/test_compiler_warm_start.py and focused compiler probe.
def test_compile_arrhenius_uses_direct_division_template():
    spec = get_demo("arrhenius")
    splits = spec.make_splits(points=24, seed=0)
    result = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
        {spec.variable: splits[0].inputs[spec.variable]},
    )

    assert result.validation is not None
    assert result.validation.passed
    assert result.metadata.depth <= 13
    assert result.metadata.macro_diagnostics["hits"] == ["direct_division_template"]
```

The no-edit probe measured depth 7 and validation max absolute error about `1.7e-16`. [VERIFIED: focused compiler probe]

### CLI Report Test

```python
# Source: tests/test_compiler_warm_start.py and src/eml_symbolic_regression/cli.py.
def test_cli_warm_start_promotes_arrhenius_after_same_ast_return(tmp_path):
    output = tmp_path / "arrhenius-warm.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "arrhenius",
            "--warm-start-eml",
            "--points",
            "24",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert "trained_exact_recovery=recovered" in result.stdout
    payload = json.loads(output.read_text())
    assert payload["claim_status"] == "recovered"
    assert payload["stage_statuses"]["compiled_seed"] == "recovered"
    assert payload["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
    assert payload["stage_statuses"]["trained_exact_recovery"] == "recovered"
    assert payload["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["direct_division_template"]
```

The CLI path already supports `--warm-start-eml`, `--max-compile-depth`, `--max-warm-depth`, and `--warm-noise`; no parser change is expected. [VERIFIED: src/eml_symbolic_regression/cli.py]

### Benchmark Artifact Test

```python
# Source: tests/test_benchmark_runner.py and src/eml_symbolic_regression/benchmark.py.
def test_arrhenius_warm_start_records_same_ast_evidence(tmp_path):
    base = builtin_suite("v1.9-arrhenius-evidence")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("arrhenius-warm",)))

    assert len(result.results) == 1
    artifact = result.results[0].payload
    assert result.results[0].status == "same_ast_return"
    assert artifact["claim_status"] == "recovered"
    assert artifact["evidence_class"] == "same_ast"
    assert artifact["compiled_eml"]["metadata"]["depth"] <= 13
    assert artifact["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["direct_division_template"]
    assert artifact["stage_statuses"]["compiled_seed"] == "recovered"
    assert artifact["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
    assert artifact["stage_statuses"]["trained_exact_recovery"] == "recovered"
    assert artifact["metrics"]["verifier_status"] == "recovered"
    assert artifact["metrics"]["warm_start_status"] == "same_ast_return"
```

Use a focused v1.9 suite or equivalently focused case so ARR-04 has a reproducible path without changing older broad campaign semantics. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Catalog-only scientific-law demos | Compiler-generated exact EML seeds with verifier-owned warm-start returns for supported formulas | Existing code before Phase 50; Beer-Lambert and Shockley paths are present now. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py] | Arrhenius should reuse the same path rather than adding a new demo mechanism. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] |
| Hidden shortcut behavior | Compiler macro diagnostics with hits, misses, baseline depth, node delta, and rule trace | Phase 37 per state history. [VERIFIED: .planning/STATE.md] [VERIFIED: src/eml_symbolic_regression/compiler.py] | ARR-02 should assert `direct_division_template` in strict metadata. [VERIFIED: .planning/REQUIREMENTS.md] |
| Single recovered/not-recovered label | Regime-separated statuses such as `same_ast_return`, `verified_equivalent_ast`, `unsupported`, and derived evidence classes | Existing benchmark/proof taxonomy before Phase 50. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: src/eml_symbolic_regression/proof.py] | ARR-03 and ARR-04 must record same-AST evidence separately from blind discovery. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] |
| Raw SI scientific constants | Normalized, dimensionless showcase formulas | Existing project constraint and FOR_DEMO guidance. [VERIFIED: AGENTS.md] [CITED: sources/FOR_DEMO.md] | Arrhenius should use transformed input `x`, not raw temperature units. [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md] |

**Deprecated/outdated:**
- Treating a verified non-EML catalog formula as recovered is not allowed because `verify_candidate()` reports `verified_showcase` unless the candidate kind is exact EML or the caller explicitly relaxes that requirement. [VERIFIED: src/eml_symbolic_regression/verify.py]
- Treating same-AST warm-start return as blind discovery is not allowed because the project documentation and benchmark taxonomy separate same-AST evidence from blind recovery. [VERIFIED: README.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py]
- Using formula-specific hardcoded recognizers is out of scope because v1.9 requirements reject one-off formula recognizers and the existing macro already supports Arrhenius. [VERIFIED: .planning/REQUIREMENTS.md] [VERIFIED: focused compiler probe]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|

All claims in this research were verified from the codebase, local command probes, or cited project source documents; no `[ASSUMED]` claims are used. [VERIFIED: source review and local probes]

## Open Questions (RESOLVED)

1. **Should the focused benchmark path be a new `v1.9-arrhenius-evidence` suite or an added row in `for-demo-diagnostics`?** [VERIFIED: src/eml_symbolic_regression/benchmark.py]
   - What we know: ARR-04 only needs a reproducible benchmark or report artifact, and the context prefers small registry extensions over broad reruns. [VERIFIED: .planning/REQUIREMENTS.md] [VERIFIED: .planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md]
   - RESOLVED decision: Add a new focused `v1.9-arrhenius-evidence` built-in suite with `arrhenius-warm`; this avoids changing older broad campaign semantics while giving a stable artifact command. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: .planning/PROJECT.md]
   - Required scope: Do not alter `for-demo-diagnostics` denominators in this phase; docs may mention the new focused suite and CLI artifact command after tests pass.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Package, CLI, pytest | yes | 3.11.5 | None needed. [VERIFIED: `python --version`] |
| pytest | Focused regression tests | yes | 7.4.0 | None needed. [VERIFIED: `python -m pytest --version`] |
| NumPy | Dataset arrays and validation inputs | yes | 1.26.4 | None needed. [VERIFIED: local version probe] |
| SymPy | Catalog candidate and compiler source expression | yes | 1.14.0 | None needed. [VERIFIED: local version probe] |
| PyTorch | Warm-start optimizer path | yes | 2.10.0 | None needed. [VERIFIED: local version probe] |
| mpmath | High-precision verification | yes | 1.3.0 | None needed. [VERIFIED: local version probe] |
| Project CLI via `PYTHONPATH=src python -m eml_symbolic_regression.cli` | Demo and benchmark artifact reproduction | yes | package source checkout | Use installed `eml-sr` script after packaging, but tests should keep using `PYTHONPATH=src`. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: tests/test_compiler_warm_start.py] |

**Missing dependencies with no fallback:** None found for Phase 50. [VERIFIED: local version probes]

**Missing dependencies with fallback:** None found for Phase 50. [VERIFIED: local version probes]

## Security Domain

Security enforcement is not disabled in `.planning/config.json`, so this section is included. [VERIFIED: .planning/config.json]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | Phase 50 has no user identity, login, or auth boundary. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| V3 Session Management | no | Phase 50 has no sessions or browser state. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| V4 Access Control | no | Phase 50 is a local CLI/package workflow with no permission model. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| V5 Input Validation | yes | Use existing `argparse` choices, `BenchmarkCase.validate()`, `DatasetConfig.validate()`, compiler fail-closed exceptions, and demo registry lookup errors. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: src/eml_symbolic_regression/compiler.py] [VERIFIED: src/eml_symbolic_regression/datasets.py] |
| V6 Cryptography | no for security | Dataset manifests use SHA-256 as deterministic signatures, not authentication or secret protection. [VERIFIED: src/eml_symbolic_regression/datasets.py] |

### Known Threat Patterns for the Phase 50 Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Unknown formula IDs in benchmark suite JSON | Tampering | `BenchmarkCase.validate()` rejects formulas not present in `demo_specs()`. [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Unsupported or unsafe SymPy operators/constants | Tampering | `compile_sympy_expression()` raises `UnsupportedExpression` with explicit reason codes. [VERIFIED: src/eml_symbolic_regression/compiler.py] |
| Misleading recovery claims | Repudiation | Preserve `stage_statuses`, `claim_status`, `status`, `evidence_class`, compiler metadata, and verifier payloads in artifacts. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: src/eml_symbolic_regression/cli.py] |
| Non-reproducible dataset evidence | Repudiation | Use deterministic seed, split metadata, input/target SHA-256 signatures, and manifest hash. [VERIFIED: src/eml_symbolic_regression/datasets.py] |
| Writing artifacts to an unintended local path | Tampering | Tests should write to `tmp_path`; docs should show explicit artifact paths under `artifacts/`. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py] |

## Sources

### Primary (HIGH confidence)
- `.planning/phases/50-arrhenius-exact-warm-start-demo/50-CONTEXT.md` - locked phase decisions, domains, strict macro requirement, warm-start evidence requirement, deferred ideas. [VERIFIED]
- `.planning/REQUIREMENTS.md` - ARR-01 through ARR-04 and v1.9 scope boundaries. [VERIFIED]
- `.planning/ROADMAP.md` - Phase 50 goal, why now, success criteria, and requirement mapping. [VERIFIED]
- `.planning/STATE.md` - prior milestone decisions, Phase 49 completion, raw-EML evidence taxonomy, and current v1.9 state. [VERIFIED]
- `.planning/PROJECT.md` - current project constraints, active v1.9 target features, and out-of-scope claim boundaries. [VERIFIED]
- `AGENTS.md` - project instructions and source-of-truth constraints. [VERIFIED]
- `src/eml_symbolic_regression/datasets.py` - `DemoSpec`, split generation, formula provenance, and proof dataset manifests. [VERIFIED]
- `src/eml_symbolic_regression/compiler.py` - compiler gates, direct-division macro, macro diagnostics, strict/relaxed diagnostics, validation. [VERIFIED]
- `src/eml_symbolic_regression/warm_start.py` - embedding, perturbation, same-AST classification, manifest diagnosis. [VERIFIED]
- `src/eml_symbolic_regression/verify.py` - verifier-owned recovered/verified_showcase status and mpmath checks. [VERIFIED]
- `src/eml_symbolic_regression/cli.py` - demo report payload and warm-start CLI path. [VERIFIED]
- `src/eml_symbolic_regression/benchmark.py` - built-in suites, benchmark artifacts, metrics, evidence classes, and validation. [VERIFIED]
- `tests/test_compiler_warm_start.py` - established compiler/warm-start/CLI test patterns. [VERIFIED]
- `tests/test_benchmark_runner.py` - established benchmark artifact/evidence-class test patterns. [VERIFIED]
- Local compiler probe - `exp(-0.8/x)` compiled at depth 7, node count 19, macro hit `direct_division_template`, validation passed. [VERIFIED]
- Local warm-start probe - zero-noise Arrhenius warm start returned `same_ast_return`, verifier `recovered`, mechanism `same_ast_return`, changed slots 0. [VERIFIED]

### Secondary (MEDIUM confidence)
- `README.md` - current user-facing evidence taxonomy and commands. [VERIFIED]
- `docs/IMPLEMENTATION.md` - current implementation documentation for compiler macros, warm-start statuses, and demo ladder. [VERIFIED]
- `pyproject.toml` - dependency constraints, pytest config, and console script. [VERIFIED]

### Tertiary (LOW confidence)
- None. [VERIFIED: source review]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - versions and dependency policy were verified locally and in `pyproject.toml`. [VERIFIED: local version probes] [VERIFIED: pyproject.toml]
- Architecture: HIGH - the existing Beer-Lambert/Shockley paths and code ownership are clear in source and tests. [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: tests/test_benchmark_runner.py]
- Compiler feasibility: HIGH - the exact Arrhenius expression was compiled and validated under the strict gate without code edits. [VERIFIED: focused compiler probe]
- Warm-start feasibility: HIGH - the zero-noise same-AST return and verifier recovery were reproduced without code edits. [VERIFIED: focused warm-start probe]
- Pitfalls: HIGH - each pitfall maps to an existing source contract or locked phase constraint. [VERIFIED: source review]

**Research date:** 2026-04-17 [VERIFIED: environment_context]
**Valid until:** 2026-05-17 for codebase planning unless compiler, benchmark, or verifier contracts change first. [VERIFIED: current git/source review]
