# EML Symbolic Regression

## What This Is

This project implements a hybrid symbolic-regression engine based on the paper "All elementary functions from a single binary operator." It searches over complete depth-bounded EML trees, optimizes soft categorical choices with PyTorch, snaps the result into an exact EML tree, cleans it up symbolically, and verifies candidate formulas against held-out data and high-precision evaluators.

The current release is a research-grade Python package and CLI for recovering compact elementary laws from synthetic scientific datasets, with demos and benchmark campaigns drawn from `sources/FOR_DEMO.md`.

## Core Value

Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Current State: v1.4 Shipped

The project now includes a compiler-driven warm-start pipeline, repeatable benchmark evidence system, campaign reporting layer, targeted recovery improvements, and before/after comparison reports. Supported SymPy formulas can compile into exact EML ASTs, validate against ordinary evaluation, embed into soft master trees with literal constant catalogs, perturb/train through the existing optimizer, snap, and delegate recovery claims to the verifier.

v1.4 used the committed v1.3 standard/showcase campaigns as the scoreboard. It added failure triage, blind `exp`/`log` scaffold initializers, warm-start failure mechanisms, compiler diagnostics, a validated Shockley template, and a generated before/after comparison. The combined standard/showcase comparison improved verifier-owned recovery from 18/45 to 27/45.

## Last Completed Milestone: v1.4 Recovery Performance Improvements

**Goal shipped:** Improve real end-to-end recovery performance against committed v1.3 standard/showcase baselines, then rerun the same campaigns to produce before/after evidence.

**Shipped features:**
- Baseline triage reports and immutable locks for v1.3 standard/showcase campaign evidence.
- Generic blind scaffold initializers for paper primitive families, improving shallow blind recovery without changing the recovery contract.
- Warm-start perturbation diagnosis that distinguishes same-AST return, verified equivalent ASTs, active-slot perturbation, non-finite snaps, soft-fit-only, and verifier mismatch.
- Compiler diagnostics and a lower-depth Shockley `c*exp(a)-c` template validated before acceptance.
- v1.4 standard/showcase campaign folders plus a comparison report showing overall recovery improved from 18/45 to 27/45.

## Current Milestone: v1.5 Training Proof and Recovery Guarantees

**Goal:** Prove the paper-grounded EML training claims with real training runs, bounded 100% recovery targets, transparent failure boundaries, metrics, and reproducible datasets.

**Target features:**
- Convert the paper's implementation claims into executable training claim suites with clear pass/fail thresholds.
- Achieve 100% verifier-owned training recovery on a declared bounded shallow proof suite, including the current `radioactive_decay` blind failure family.
- Achieve 100% verifier-owned recovery for declared perturbed-true-tree basin suites, including repaired high-noise Beer-Lambert cases or a deliberately narrowed bound if evidence proves the larger bound is invalid.
- Reproduce the paper's qualitative depth behavior with real metrics: shallow blind recovery works, deeper blind recovery degrades, and perturbed true solutions recover much more reliably.
- Publish a self-contained proof report with raw run artifacts, datasets, metrics, plots, and explicit separation of blind, warm-start, compiler-assisted, and unsupported outcomes.

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
- ✓ Campaign presets with guarded output folders and reproducibility manifests — v1.3
- ✓ Tidy CSV exports for run-level metrics, grouped recovery summaries, headline metrics, and failure reason tables — v1.3
- ✓ Deterministic SVG figures for recovery, loss, perturbation, runtime, and failure taxonomy — v1.3
- ✓ Self-contained campaign reports with exact commands, figures, tables, limitations, and next experiments — v1.3
- ✓ Campaign CLI/docs coverage and committed v1.3 smoke evidence artifact — v1.3
- ✓ Baseline failure triage, representative run links, diagnostic subsets, and baseline locks — v1.4
- ✓ Blind optimizer scaffold initializers and diagnostics for remaining shallow blind failures — v1.4
- ✓ Warm-start perturbation mechanism reporting with campaign-level metrics — v1.4
- ✓ Compiler diagnostics and validated Shockley compiled recovery under the v1.4 gate — v1.4
- ✓ Before/after v1.4 standard/showcase campaigns and comparison report — v1.4

### Active

- [ ] Prove bounded shallow EML training recovery with verifier-owned results, not training loss alone.
- [ ] Repair blind `radioactive_decay` recovery and related scaled/signed exponential families.
- [ ] Repair or tightly bound perturbed warm-start basin recovery for Beer-Lambert and synthetic exact EML trees.
- [ ] Generate real training depth-curve evidence that matches the paper's qualitative claims without overselling deep blind recovery.
- [ ] Publish reproducible proof datasets, raw training artifacts, metrics, plots, and a claim report.

### Out of Scope

- Full blind recovery of arbitrary depth-6 formulas - the paper reports no blind recovery at depth 6 in 448 attempts, so this cannot be promised for v1.
- Universal 100% recovery over all elementary functions - v1.5 targets 100% recovery only over explicitly declared bounded proof suites and reports measured limits elsewhere.
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
| v1.3 prioritizes showcase evidence over optimizer changes | The user wants crisp numbers, graphs, and a real-life performance narrative before tuning the algorithm. | ✓ Good |
| Static reports before dashboards | CSV, SVG, and Markdown evidence proved the metrics before adding an interactive dashboard. | ✓ Good |
| v1.4 uses committed campaigns as the scoreboard | More baseline runs would mostly confirm the same weaknesses; the useful next step is targeted improvement followed by identical reruns. | ✓ Good |
| Primitive scaffolds are acceptable blind defaults | They encode paper-grounded primitive families and preserve verifier-owned recovery semantics. | ✓ Good |
| Diagnose Beer-Lambert before repairing it | High-perturbation failures needed mechanism-level evidence before deeper discrete repair work. | ✓ Good |
| Shockley template must validate before acceptance | Compiler expansion remains fail-closed and cannot emit invalid EML trees. | ✓ Good |
| Before/after comparison is the milestone gate | Recovery improvements are only credible when rerun through the same standard/showcase campaign contracts. | ✓ Good |
| v1.5 training proof must be bounded | The user wants 100% functional training, but the paper itself reports rapid blind degradation at depth; the defensible target is 100% over declared suites plus honest depth curves. | - Pending |
| Compile-only success does not prove training | v1.5 reports compiler-assisted cases separately and counts proof success only when actual training and verifier checks pass. | - Pending |

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
*Last updated: 2026-04-15 after starting milestone v1.5*
