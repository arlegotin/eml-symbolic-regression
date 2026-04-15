# Overview

This repo implements [this paper](sources/paper.pdf).
The implementation details [are here](sources/NORTH_STAR.md).
To showcase how the system performs [use these examples](sources/FOR_DEMO.md).

<!-- GSD:project-start source:PROJECT.md -->
## Project

**EML Symbolic Regression**

This project implements a hybrid symbolic-regression engine based on the paper "All elementary functions from a single binary operator." It searches over complete depth-bounded EML trees, optimizes soft categorical choices with PyTorch, snaps the result into an exact EML tree, cleans it up symbolically, and verifies candidate formulas against held-out data and high-precision evaluators.

The first release is a research-grade Python package and CLI for recovering compact elementary laws from synthetic scientific datasets, with demos drawn from `sources/FOR_DEMO.md`.

**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

### Constraints

- **Paper fidelity**: EML semantics, complete-tree construction, snapping, and complex arithmetic must be grounded in `sources/paper.pdf` and `sources/NORTH_STAR.md`.
- **Numerics**: Training defaults to PyTorch `complex128`, with clamps only in training mode and faithful verification mode afterwards.
- **Verification**: A candidate is not "recovered" based on training loss alone; it must pass held-out, extrapolation, and high-precision checks.
- **Scope realism**: v1 must avoid overselling blind deep recovery because the paper reports rapid degradation beyond shallow depths.
- **Demos**: Showcase examples must come from `sources/FOR_DEMO.md`, favoring normalized, dimensionless, visually distinctive laws.
- **Repository state**: This started as a greenfield repo with only source documents and `AGENTS.md`.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Recommendation
## Local Baseline
| Tool | Local Version | Use in MVP | Confidence |
|------|---------------|------------|------------|
| Python | 3.11.5 | Package, CLI, orchestration | HIGH |
| PyTorch | 2.10.0 | Differentiable EML tree, complex autograd, Adam | HIGH |
| NumPy | 1.26.4 | Dataset generation, CPU baselines, reference checks | HIGH |
| SymPy | 1.14.0 | Symbolic AST export, targeted rewrites, pretty formulas | HIGH |
| mpmath | 1.3.0 | Arbitrary-precision complex verification | HIGH |
| pytest | 7.4.0 | Unit, regression, demo, and verifier tests | HIGH |
| CUDA | unavailable locally | Not an MVP dependency | HIGH |
## Recommended Stack
### Core Runtime
| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| Python | Use current 3.11.5 locally; declare `>=3.11,<3.13` initially | Main implementation language, CLI, experiment orchestration | The repo is greenfield, the local environment is already ready, and Python is the fastest path for numerical research iteration. |
| PyTorch | Start with local 2.10.0; pin a lower bound around the observed version once `pyproject.toml` exists | Differentiable complete EML master tree, logits, softmax gates, Adam optimization, batched evaluation | The paper's ML experiments explicitly use PyTorch with `torch.complex128`; `sources/NORTH_STAR.md` requires complex128 training, restarts, annealing, entropy regularization, hardening, and anomaly logging. |
| `torch.complex128` | Default dtype | Complex-valued EML semantics during training and verification | The paper says EML requires complex intermediates and reports PyTorch experiments using `DTYPE = torch.complex128`. Symbolic recovery is branch-sensitive, so `complex64` should be only an optional speed mode. |
| PyTorch eager mode | Default execution mode | First implementation of training and evaluation | Eager mode keeps anomaly inspection, per-node logging, and numerical debugging simple. Use graph compilation only after semantics stabilize. |
### Numerics and Verification
| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| NumPy | Local 1.26.4 is enough | Synthetic datasets, deterministic sampling, non-gradient reference evaluation | The paper notes EML works in NumPy and uses NumPy as one verification backend. It is the right lightweight CPU reference layer. |
| mpmath | Local 1.3.0 is enough | High-precision real/complex verification of snapped formulas | The project requirements say candidates must pass high-precision checks, not just training loss. mpmath gives this without a proprietary dependency. |
| Python `decimal` | Standard library only, optional | Decimal sanity checks for real-only simple demos | Useful for a small subset of real smoke tests, but not a replacement for mpmath complex evaluation. |
| Explicit anomaly logging | Project code, not a dependency | Count NaN, Inf, overflow clamps, branch-cut hits, and post-snap mismatch | The paper reports overflow and NaN issues from composed exponentials and complex arithmetic. Logging these is core product functionality. |
### Symbolic Layer
| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| SymPy | Local 1.14.0 is enough | Exact EML AST translation, ordinary-expression export, targeted rewrites | The MVP needs human-readable formulas. SymPy is available locally and avoids requiring Mathematica. |
| Python `dataclasses` / `enum` / `json` | Standard library | Exact snapped EML tree representation and deterministic JSON export | The tree format is simple: terminals, variables, and binary `eml` nodes. A standard-library AST is easier to audit than a heavy schema library. |
| Targeted rewrite passes | Project code using SymPy | Cleanup after snapping | SymPy's generic `simplify()` is useful interactively but too broad as a core algorithm. Use explicit passes such as `expand`, `factor`, `cancel`, `powsimp`, and project-specific EML identities. |
### CLI, Packaging, and Developer Tools
| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| `pyproject.toml` | Add in first implementation phase | Package metadata, dependencies, console script | The repo is greenfield; standard Python packaging is enough. |
| `argparse` | Standard library | MVP CLI | Avoid adding Typer/Click until the command surface is large enough to justify another dependency. |
| `logging` + JSONL artifacts | Standard library | Reproducible experiment records | Training diagnostics, snap decisions, and verification reports should be machine-readable from day one. |
| pytest | Local 7.4.0 is enough | Unit tests and demo regression tests | The project requires tests for semantics, tree construction, snapping, verification, and demos. pytest parametrization fits these cases directly. |
| uv | Optional dev workflow | Dependency locking and repeatable environments once `pyproject.toml` exists | Useful for a new Python project, but do not block MVP execution on adopting it. The current conda environment already has the required scientific stack. |
| Ruff | Optional dev dependency | Formatting and linting once code exists | Good default for a Python package, but secondary to mathematical correctness and verifier coverage. |
## Module-Level Stack Mapping
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
## Categorical Gates
## Data and Demo Stack
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
### Rust
- bounded exhaustive/local neighborhood search,
- deduplication of snapped candidates,
- batch evaluation of many exact EML trees,
- fast verifier kernels,
- shortest-form search helpers.
- PyO3 + maturin for Python extension modules,
- `serde`/JSON-compatible structs for exact tree exchange.
### CUDA
- symbolic snapping,
- tree serialization,
- SymPy cleanup,
- verifier decision logic.
## Version and Dependency Policy
## Installation
# Run tests in the current environment
# Optional once pyproject.toml exists
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
- `.planning/PROJECT.md` - active requirements: Python/PyTorch first, complex128 training, snapping, JSON/SymPy export, mpmath verification, demos, tests; custom CUDA and web UI out of scope.
- `sources/NORTH_STAR.md` - hybrid pipeline, train/evaluate split, complete master tree, optimizer requirements, hardening/snap, local cleanup, verifier, 2026 technology guidance.
- `sources/paper.pdf` - EML definition, complex-domain requirement, complete tree grammar, master formula, PyTorch `complex128` experiments, Adam/hardening/clamping, success-rate limits by depth, Rust verification speed note.
- `sources/FOR_DEMO.md` - demo ordering, normalization guidance, and warnings against high-depth/unit-heavy/special-function demos.
- `AGENTS.md` - repo source-of-truth pointers.
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
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
