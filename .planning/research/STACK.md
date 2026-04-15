# Technology Stack

**Project:** EML Symbolic Regression
**Research dimension:** Stack
**Researched:** 2026-04-15
**Overall confidence:** HIGH for Python/PyTorch MVP; MEDIUM for later Rust/CUDA acceleration timing

## Recommendation

Use a Python-first research package and CLI built around PyTorch `complex128`, with NumPy for data/reference arrays, SymPy for exact expression representation and targeted rewrites, mpmath for high-precision verification, and pytest for regression tests.

Do not start with Rust, CUDA kernels, JAX, Julia, PySR, Mathematica, or a web UI. They are either misaligned with the local source documents or add implementation surface before the core EML semantics, snapping, cleanup, and verification loop is proven.

The practical MVP stack is:

```text
Python package + CLI
  -> PyTorch complete EML master tree
  -> hardening / snapping into exact EML AST
  -> SymPy export and targeted cleanup
  -> mpmath high-precision verifier
  -> pytest demo and regression harness
```

This matches the paper and `sources/NORTH_STAR.md`: the hard part is not a missing framework, but getting canonical EML semantics, stable complex optimization, exact snapping, local cleanup, and verification correct.

## Local Baseline

Observed in the current repo environment on 2026-04-15:

| Tool | Local Version | Use in MVP | Confidence |
|------|---------------|------------|------------|
| Python | 3.11.5 | Package, CLI, orchestration | HIGH |
| PyTorch | 2.10.0 | Differentiable EML tree, complex autograd, Adam | HIGH |
| NumPy | 1.26.4 | Dataset generation, CPU baselines, reference checks | HIGH |
| SymPy | 1.14.0 | Symbolic AST export, targeted rewrites, pretty formulas | HIGH |
| mpmath | 1.3.0 | Arbitrary-precision complex verification | HIGH |
| pytest | 7.4.0 | Unit, regression, demo, and verifier tests | HIGH |
| CUDA | unavailable locally | Not an MVP dependency | HIGH |

No `pyproject.toml`, lockfile, or package skeleton exists yet. The first implementation phase should add normal Python packaging, but it should not require new runtime dependencies beyond the packages already present unless profiling or usability demands them.

## Recommended Stack

### Core Runtime

| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| Python | Use current 3.11.5 locally; declare `>=3.11,<3.13` initially | Main implementation language, CLI, experiment orchestration | The repo is greenfield, the local environment is already ready, and Python is the fastest path for numerical research iteration. |
| PyTorch | Start with local 2.10.0; pin a lower bound around the observed version once `pyproject.toml` exists | Differentiable complete EML master tree, logits, softmax gates, Adam optimization, batched evaluation | The paper's ML experiments explicitly use PyTorch with `torch.complex128`; `sources/NORTH_STAR.md` requires complex128 training, restarts, annealing, entropy regularization, hardening, and anomaly logging. |
| `torch.complex128` | Default dtype | Complex-valued EML semantics during training and verification | The paper says EML requires complex intermediates and reports PyTorch experiments using `DTYPE = torch.complex128`. Symbolic recovery is branch-sensitive, so `complex64` should be only an optional speed mode. |
| PyTorch eager mode | Default execution mode | First implementation of training and evaluation | Eager mode keeps anomaly inspection, per-node logging, and numerical debugging simple. Use graph compilation only after semantics stabilize. |

**Implementation rule:** keep the EML model as a static `torch.nn.Module` for a chosen depth and arity. Store gate logits as `nn.Parameter`, convert to probabilities with `torch.softmax`, and snap by `argmax` into an exact AST.

### Numerics and Verification

| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| NumPy | Local 1.26.4 is enough | Synthetic datasets, deterministic sampling, non-gradient reference evaluation | The paper notes EML works in NumPy and uses NumPy as one verification backend. It is the right lightweight CPU reference layer. |
| mpmath | Local 1.3.0 is enough | High-precision real/complex verification of snapped formulas | The project requirements say candidates must pass high-precision checks, not just training loss. mpmath gives this without a proprietary dependency. |
| Python `decimal` | Standard library only, optional | Decimal sanity checks for real-only simple demos | Useful for a small subset of real smoke tests, but not a replacement for mpmath complex evaluation. |
| Explicit anomaly logging | Project code, not a dependency | Count NaN, Inf, overflow clamps, branch-cut hits, and post-snap mismatch | The paper reports overflow and NaN issues from composed exponentials and complex arithmetic. Logging these is core product functionality. |

**Implementation rule:** maintain two evaluator modes:

1. `training`: guarded PyTorch complex evaluator with controlled clamps on dangerous intermediates.
2. `verification`: faithful canonical evaluator with no hidden epsilons, checked against mpmath and held-out/extrapolation points.

This split matters because training stabilizers are search aids, not proof of recovered formulas.

### Symbolic Layer

| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| SymPy | Local 1.14.0 is enough | Exact EML AST translation, ordinary-expression export, targeted rewrites | The MVP needs human-readable formulas. SymPy is available locally and avoids requiring Mathematica. |
| Python `dataclasses` / `enum` / `json` | Standard library | Exact snapped EML tree representation and deterministic JSON export | The tree format is simple: terminals, variables, and binary `eml` nodes. A standard-library AST is easier to audit than a heavy schema library. |
| Targeted rewrite passes | Project code using SymPy | Cleanup after snapping | SymPy's generic `simplify()` is useful interactively but too broad as a core algorithm. Use explicit passes such as `expand`, `factor`, `cancel`, `powsimp`, and project-specific EML identities. |

**Implementation rule:** SymPy is a representation and rewrite backend, not the verifier of record. Numeric high-precision and cross-backend checks must decide whether a snapped formula is accepted.

### CLI, Packaging, and Developer Tools

| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| `pyproject.toml` | Add in first implementation phase | Package metadata, dependencies, console script | The repo is greenfield; standard Python packaging is enough. |
| `argparse` | Standard library | MVP CLI | Avoid adding Typer/Click until the command surface is large enough to justify another dependency. |
| `logging` + JSONL artifacts | Standard library | Reproducible experiment records | Training diagnostics, snap decisions, and verification reports should be machine-readable from day one. |
| pytest | Local 7.4.0 is enough | Unit tests and demo regression tests | The project requires tests for semantics, tree construction, snapping, verification, and demos. pytest parametrization fits these cases directly. |
| uv | Optional dev workflow | Dependency locking and repeatable environments once `pyproject.toml` exists | Useful for a new Python project, but do not block MVP execution on adopting it. The current conda environment already has the required scientific stack. |
| Ruff | Optional dev dependency | Formatting and linting once code exists | Good default for a Python package, but secondary to mathematical correctness and verifier coverage. |

**Implementation rule:** start with `argparse`, `logging`, deterministic JSON outputs, and pytest. Add richer UX only after the algorithmic loop is proven.

## Module-Level Stack Mapping

The stack should map to source modules like this:

| Module | Primary Stack | Responsibility |
|--------|---------------|----------------|
| `eml.semantics` | PyTorch, NumPy, mpmath | Canonical `eml(x, y) = exp(x) - ln(y)`, branch handling, training vs verification evaluators |
| `eml.tree` | dataclasses, enum, json | Exact EML AST, terminals, variables, node serialization |
| `eml.master_tree` | PyTorch | Complete depth-bounded trainable tree with categorical logits |
| `eml.optimize` | PyTorch | Adam/AdamW, restarts, temperature annealing, entropy and size penalties |
| `eml.snap` | PyTorch, AST layer | Argmax hardening, dead-branch pruning, exact one-hot tree export |
| `eml.simplify` | SymPy, project rewrite rules | Targeted symbolic cleanup and ordinary-expression export |
| `eml.verify` | NumPy, mpmath, PyTorch | Held-out, extrapolation, backend consistency, high-precision checks |
| `eml.datasets` | NumPy, PyTorch | Demo data from `sources/FOR_DEMO.md` with normalization and seeds |
| `eml.cli` | argparse, logging, json | Reproducible commands for train, snap, verify, and demo |
| `tests` | pytest | Paper-grounded semantics, tree construction, snapping, verification, demos |

This module split keeps PyTorch where gradients are needed and keeps exact AST, simplification, and verification logic independent of training tensors.

## Categorical Gates

Use `torch.softmax(logits / temperature, dim=-1)` as the normal soft gate. For hardening:

1. select `argmax` categories,
2. construct an exact one-hot tree,
3. re-evaluate the snapped tree outside the differentiable model,
4. optionally use a project-owned straight-through estimator during late training.

Do not build the core API around `torch.nn.functional.gumbel_softmax`. Official PyTorch docs keep it available but label it legacy and warn it may be removed from `nn.functional` in the future. If needed, wrap it behind a small local abstraction so the rest of the engine depends only on project-owned gate semantics.

## Data and Demo Stack

Use NumPy for deterministic data generation and PyTorch tensors only when entering training. Start with the `sources/FOR_DEMO.md` progression:

1. Beer-Lambert or radioactive decay
2. Michaelis-Menten
3. Logistic growth
4. Shockley diode
5. Damped oscillator
6. Normalized Planck spectrum

The stack should support normalization and dimensionless variables as first-class dataset metadata. Raw SI constants and unit-heavy formulas should stay out of the MVP path because they make optimization harder without testing the core EML idea.

## What Not To Use First

| Alternative | Recommendation | Why Not MVP |
|-------------|----------------|-------------|
| JAX | Do not use | Viable generally, but the paper, local environment, and project requirements are PyTorch-centered. Switching would spend early effort on backend behavior rather than EML recovery. |
| Julia / SymbolicRegression.jl / PySR | Use later as comparator only | Excellent symbolic-regression ecosystem, but its normal strength is heterogeneous operator search. This repo's point is complete EML-tree search, snapping, and EML-specific verification. |
| Mathematica | Optional oracle only | The paper uses it, but a practical open MVP should not depend on proprietary software. |
| Lean / theorem proving | Out of scope for MVP | Formal equivalence is explicitly out of scope in `.planning/PROJECT.md`; numeric, high-precision, and targeted symbolic checks are enough for v1. |
| Pydantic | Do not add initially | The AST is small and deterministic JSON is enough. Add schema validation only when external artifact compatibility becomes a real concern. |
| Typer / Click / Rich / tqdm | Defer | Nice CLI ergonomics, but not needed to validate semantics and recovery. |
| Custom CUDA kernels | Defer | Current local CUDA is unavailable, and `.planning/PROJECT.md` explicitly says to use normal PyTorch first and profile before adding kernels. |
| Rust core implementation | Defer | Rust is justified later for exhaustive search and fast verification, but early iteration needs Python/PyTorch. |

## Later Acceleration Path

Rust and CUDA are justified only after the Python MVP has stable semantics and profiles identify bottlenecks.

### Rust

Use Rust later for:

- bounded exhaustive/local neighborhood search,
- deduplication of snapped candidates,
- batch evaluation of many exact EML trees,
- fast verifier kernels,
- shortest-form search helpers.

Rationale: the paper reports a Rust reimplementation of `VerifyBaseSet` running roughly three orders of magnitude faster than the original Mathematica workflow. That supports Rust for discrete search and verification, not for the first differentiable training runtime.

Interoperability choice when needed:

- PyO3 + maturin for Python extension modules,
- `serde`/JSON-compatible structs for exact tree exchange.

Confidence: MEDIUM. The paper strongly motivates Rust for verification speed, but this repo has no Rust code yet and the MVP bottlenecks are not measured.

### CUDA

Use standard PyTorch GPU support first if a CUDA machine is available. Add custom CUDA only for measured hotspots such as batched candidate evaluation or neighborhood scoring.

Do not custom-kernel:

- symbolic snapping,
- tree serialization,
- SymPy cleanup,
- verifier decision logic.

Confidence: MEDIUM. CUDA is a plausible later target and NVIDIA's current CUDA programming guide is active, but the local machine currently reports `torch.cuda.is_available() == False`.

## Version and Dependency Policy

Recommended initial `pyproject.toml` policy once packaging starts:

```toml
[project]
requires-python = ">=3.11,<3.13"
dependencies = [
  "torch>=2.10",
  "numpy>=1.26",
  "sympy>=1.14",
  "mpmath>=1.3",
]

[project.optional-dependencies]
dev = [
  "pytest>=7.4",
  "ruff",
]
```

Keep exact locks in the dev environment, but keep library lower bounds conservative until CI exists. Do not pin to CUDA-specific PyTorch wheels in project metadata; document GPU installation separately if needed.

## Installation

For the current local repo, no new installs are required for the MVP research stack. The environment already imports the required runtime packages.

Suggested commands after the first package skeleton exists:

```bash
# Run tests in the current environment
python -m pytest

# Optional once pyproject.toml exists
uv sync
uv run pytest
uv run ruff check .
```

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Python-first MVP | HIGH | Required packages are already installed locally; source docs explicitly call for a Python/PyTorch-first implementation. |
| PyTorch `complex128` training | HIGH | Directly grounded in the paper and `.planning/PROJECT.md`; official docs support complex tensors, while warning they remain beta. |
| Eager-first execution | HIGH | The paper reports numerical pathologies that need transparent debugging before compilation. |
| SymPy + mpmath verification layer | HIGH | Matches project requirement for symbolic cleanup plus high-precision checks using local packages. |
| Avoiding PySR/JAX as core | HIGH | The project is specifically about complete EML trees, not generic heterogeneous symbolic regression. |
| Deferring Rust | MEDIUM | Paper strongly supports Rust speedups for verification, but implementation should measure bottlenecks before adding language complexity. |
| Deferring custom CUDA | HIGH | Explicitly out of scope for v1 in `.planning/PROJECT.md`; current local environment has no CUDA available. |
| uv/Ruff developer workflow | MEDIUM | Current official docs and Python practice support them, but they are not algorithmically necessary. |

## Sources

Local project sources:

- `.planning/PROJECT.md` - active requirements: Python/PyTorch first, complex128 training, snapping, JSON/SymPy export, mpmath verification, demos, tests; custom CUDA and web UI out of scope.
- `sources/NORTH_STAR.md` - hybrid pipeline, train/evaluate split, complete master tree, optimizer requirements, hardening/snap, local cleanup, verifier, 2026 technology guidance.
- `sources/paper.pdf` - EML definition, complex-domain requirement, complete tree grammar, master formula, PyTorch `complex128` experiments, Adam/hardening/clamping, success-rate limits by depth, Rust verification speed note.
- `sources/FOR_DEMO.md` - demo ordering, normalization guidance, and warnings against high-depth/unit-heavy/special-function demos.
- `AGENTS.md` - repo source-of-truth pointers.

Official/current external sources checked:

- PyTorch complex numbers docs: https://docs.pytorch.org/docs/stable/complex_numbers.html
- PyTorch `torch.compile` docs: https://docs.pytorch.org/docs/stable/generated/torch.compile.html
- PyTorch `torch.export` docs: https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/export.html
- PyTorch `gumbel_softmax` docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.gumbel_softmax.html
- SymPy simplification tutorial: https://docs.sympy.org/latest/tutorials/intro-tutorial/simplification.html
- SymPy term rewriting docs: https://docs.sympy.org/latest/modules/rewriting.html
- mpmath docs: https://mpmath.org/doc/current/
- pytest parametrization docs: https://docs.pytest.org/en/stable/how-to/parametrize.html
- Python packaging `pyproject.toml` metadata specs: https://packaging.python.org/en/latest/specifications/section-distribution-metadata/
- uv docs: https://docs.astral.sh/uv/
- NVIDIA CUDA C++ Programming Guide 13.2: https://docs.nvidia.com/cuda/archive/13.2.0/cuda-c-programming-guide/contents.html
