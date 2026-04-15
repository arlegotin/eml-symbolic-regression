# EML Symbolic Regression

## What This Is

This project implements a hybrid symbolic-regression engine based on the paper "All elementary functions from a single binary operator." It searches over complete depth-bounded EML trees, optimizes soft categorical choices with PyTorch, snaps the result into an exact EML tree, cleans it up symbolically, and verifies candidate formulas against held-out data and high-precision evaluators.

The first release is a research-grade Python package and CLI for recovering compact elementary laws from synthetic scientific datasets, with demos drawn from `sources/FOR_DEMO.md`.

## Core Value

Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Current State: v1.2 Shipped

The project now includes a compiler-driven warm-start pipeline and a repeatable benchmark evidence system. Supported SymPy formulas can compile into exact EML ASTs, validate against ordinary evaluation, embed into soft master trees with literal constant catalogs, perturb/train through the existing optimizer, snap, and delegate recovery claims to the verifier.

v1.2 added deterministic benchmark suites, CLI suite execution, per-run artifacts, aggregate JSON/Markdown evidence reports, formula coverage for shallow baselines and FOR_DEMO diagnostics, and smoke artifacts that keep same-AST warm-start return separate from blind discovery. Beer-Lambert remains the verified compiler warm-start recovery; Michaelis-Menten and normalized Planck remain honest diagnostic/stretch cases under the default gates.

## Last Completed Milestone: v1.2 Training Benchmark and Recovery Evidence

**Goal shipped:** Turn anecdotal training runs into a repeatable benchmark harness that measures when EML recovery works, when it fails, and how strong the evidence is.

**Shipped features:**
- Reproducible benchmark suite definitions for blind starts, compiler warm starts, perturbation sweeps, and demo/stretch diagnostics.
- Per-run JSON artifacts and aggregate reports covering loss, snap outcome, verifier status, recovery rate, active slot changes, runtime, and failures.
- Formula coverage for shallow blind baselines, Beer-Lambert perturbation levels, Michaelis-Menten and Planck depth diagnostics, and selected `sources/FOR_DEMO.md` showcase formulas.
- Documentation and tests that separate promising infrastructure from actual measured recovery performance.

## Requirements

### Validated

- ✓ Canonical EML semantics, exact ASTs, and deterministic JSON artifacts — v1 implementation
- ✓ Complete soft EML master trees with PyTorch `complex128` evaluation and snapping — v1 implementation
- ✓ Verifier-owned recovery contract with train, held-out, extrapolation, and mpmath checks — v1 implementation
- ✓ Demo CLI and reports for examples from `sources/FOR_DEMO.md` — v1 implementation
- ✓ Pytest coverage and documentation for the MVP pipeline — v1 implementation
- ✓ Defined SymPy subset compiler into exact EML ASTs with metadata and validation — v1.1
- ✓ Literal constant catalogs and AST embedding into soft master trees — v1.1
- ✓ Deterministic perturbation and compiler warm-start training manifests — v1.1
- ✓ Beer-Lambert trained exact EML recovery via compiler warm start — v1.1
- ✓ Michaelis-Menten and Planck honest unsupported/stretch reporting under default gates — v1.1
- ✓ Regression tests and documentation for compiler/warm-start claim taxonomy — v1.1
- ✓ Deterministic benchmark suite schema, built-in registry, validation, stable run IDs, and artifact paths — v1.2
- ✓ Benchmark CLI execution for catalog, compile, blind, and compiler warm-start modes — v1.2
- ✓ Formula matrix covering shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten/Planck diagnostics, and selected FOR_DEMO formulas — v1.2
- ✓ Aggregate JSON/Markdown evidence reports with recovery rates, taxonomy, metrics, and provenance — v1.2
- ✓ CI-scale benchmark smoke coverage and documentation for interpreting recovery evidence — v1.2

### Active

- [ ] Decide the next milestone scope.
- [ ] Use v1.2 benchmark evidence to guide optimizer robustness improvements for slot-changing perturbations.
- [ ] Consider reducing compiled arithmetic tree depth so Michaelis-Menten can promote under practical warm-start gates.
- [ ] Consider pure `{1, eml}` synthesis or coefficient fitting for literal constants in a later milestone.

### Out of Scope

- Full blind recovery of arbitrary depth-6 formulas - the paper reports no blind recovery at depth 6 in 448 attempts, so this cannot be promised for v1.
- High-noise real-world scientific datasets without priors - v1 focuses on noiseless or modest-noise demonstration problems.
- Custom CUDA kernels - use normal PyTorch execution first and profile before adding kernels.
- A web GUI - the first target is a reproducible package, CLI, tests, and demos.
- Formal theorem-prover equivalence - v1 uses numeric, high-precision, and targeted symbolic checks.

## Context

The uploaded paper defines `eml(x, y) = exp(x) - ln(y)` and shows that EML plus the constant `1` generates the paper's scientific-calculator basis. It also shows that EML expressions form a regular binary grammar `S -> 1 | eml(S, S)`, which makes a complete depth-bounded master tree possible.

`sources/NORTH_STAR.md` turns that paper result into an implementation blueprint. Its core recommendation is a hybrid pipeline: continuous search, hardening, symbolic snapping, local discrete cleanup, and verification. It also warns that pure gradient descent is not enough because the paper's blind recovery success drops sharply with depth, while warm starts recover reliably from perturbed correct solutions.

`sources/FOR_DEMO.md` defines the showcase strategy. The highest-probability sequence starts with Beer-Lambert or radioactive decay, then Michaelis-Menten, logistic growth, Shockley diode, damped oscillator, and normalized Planck spectrum. The strongest public-facing set is Michaelis-Menten, damped harmonic oscillator, and normalized Planck spectrum.

## Constraints

- **Paper fidelity**: EML semantics, complete-tree construction, snapping, and complex arithmetic must be grounded in `sources/paper.pdf` and `sources/NORTH_STAR.md`.
- **Numerics**: Training defaults to PyTorch `complex128`, with clamps only in training mode and faithful verification mode afterwards.
- **Verification**: A candidate is not "recovered" based on training loss alone; it must pass held-out, extrapolation, and high-precision checks.
- **Scope realism**: v1 must avoid overselling blind deep recovery because the paper reports rapid degradation beyond shallow depths.
- **Demos**: Showcase examples must come from `sources/FOR_DEMO.md`, favoring normalized, dimensionless, visually distinctive laws.
- **Repository state**: This started as a greenfield repo with only source documents and `AGENTS.md`.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use Python and PyTorch first | The paper's ML proof of concept uses PyTorch and `torch.complex128`, and the local environment already has the needed packages. | - Pending |
| Keep Rust/CUDA as later acceleration targets | The north-star doc recommends Rust and CUDA after profiling, but v1 can validate semantics and pipeline in Python first. | - Pending |
| Build a package and CLI before any UI | The strong MVP needs reproducible experiments, verification, and demos more than a frontend. | - Pending |
| Use YOLO GSD defaults | The user asked to implement start to end and this session cannot use interactive GSD questions. | - Pending |
| v1.1 focuses on compiler-driven warm starts | This is the shortest path from verified catalog demos to actual trained EML recovery without overpromising blind deep search. | ✓ Good |
| Literal constants are explicit provenance | v1.1 demos need fixed coefficients, but those are not pure `{1, eml}` synthesis claims. | ✓ Good |
| Planck remains stretch reporting | The compiled Planck tree exceeds default warm-start gates; false promotion would weaken the recovery contract. | ✓ Good |
| v1.2 focuses on evidence before algorithm expansion | The last training check showed shallow and same-basin successes but strong perturbation failure, so measurement had to precede optimizer claims. | ✓ Good |
| Same-AST warm-start return is not blind discovery | Benchmark reports count same-AST return separately from verifier-owned recovery rate and unsupported cases. | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-15 after shipping milestone v1.2*
