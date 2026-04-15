# EML Symbolic Regression

## What This Is

This project implements a hybrid symbolic-regression engine based on the paper "All elementary functions from a single binary operator." It searches over complete depth-bounded EML trees, optimizes soft categorical choices with PyTorch, snaps the result into an exact EML tree, cleans it up symbolically, and verifies candidate formulas against held-out data and high-precision evaluators.

The first release is a research-grade Python package and CLI for recovering compact elementary laws from synthetic scientific datasets, with demos drawn from `sources/FOR_DEMO.md`.

## Core Value

Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Current Milestone: v1.1 EML Compiler and Warm Starts

**Goal:** Turn verified reference demos into actual EML-tree recovery workflows by compiling ordinary formulas into exact EML ASTs and using those trees as warm starts for training.

**Target features:**
- Implement a practical ordinary-expression-to-EML compiler subset for constants, variables, `exp`, `log`, negation/subtraction, addition, multiplication, and division where feasible.
- Embed compiled exact EML trees into compatible soft master trees and initialize logits near the compiled structure.
- Add perturbation/warm-start training that demonstrates recovery from near-correct EML trees.
- Promote Beer-Lambert and Michaelis-Menten from catalog showcase formulas to trained EML recovery demos when verification passes.
- Keep normalized Planck as a stretch showcase with honest success/failure reporting.

## Requirements

### Validated

- ✓ Canonical EML semantics, exact ASTs, and deterministic JSON artifacts — v1 implementation
- ✓ Complete soft EML master trees with PyTorch `complex128` evaluation and snapping — v1 implementation
- ✓ Verifier-owned recovery contract with train, held-out, extrapolation, and mpmath checks — v1 implementation
- ✓ Demo CLI and reports for examples from `sources/FOR_DEMO.md` — v1 implementation
- ✓ Pytest coverage and documentation for the MVP pipeline — v1 implementation

### Active

- [ ] Compile a defined subset of ordinary SymPy expressions into exact EML ASTs.
- [ ] Serialize compiler output with enough metadata to trace source expressions and compiler rules.
- [ ] Embed compiled EML ASTs into soft master trees as warm-start logits.
- [ ] Add controlled perturbation of warm-start logits to test return-to-solution behavior.
- [ ] Run and verify trained EML recovery demos for Beer-Lambert and Michaelis-Menten.
- [ ] Document which demo formulas are exact trained EML recoveries, warm-start recoveries, catalog showcases, or still unsupported.

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
| v1.1 focuses on compiler-driven warm starts | This is the shortest path from verified catalog demos to actual trained EML recovery without overpromising blind deep search. | - Pending |

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
*Last updated: 2026-04-15 after starting milestone v1.1*
