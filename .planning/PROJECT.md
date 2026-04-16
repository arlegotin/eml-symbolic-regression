# EML Symbolic Regression

## What This Is

This project implements a hybrid symbolic-regression engine based on the paper "All elementary functions from a single binary operator." It searches over complete depth-bounded EML trees, optimizes soft categorical choices with PyTorch, snaps the result into an exact EML tree, cleans it up symbolically, and verifies candidate formulas against held-out data and high-precision evaluators.

The current release is a research-grade Python package and CLI for recovering compact elementary laws from synthetic scientific datasets, with demos, benchmark campaigns, and proof artifacts drawn from `sources/FOR_DEMO.md`. The next milestone focuses on improving blind-discovery search quality without weakening the repo's verifier-owned recovery contract or replacing any archived evidence.

## Core Value

Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Current State: v1.6 In Progress

The repo now has strong representation, verification, and reproducibility foundations. Exact EML ASTs, soft master trees, compiler-driven warm starts, deterministic benchmark suites, campaign reports, and a one-command proof bundle are all in place and archived through v1.5.

The v1.5 proof results make the next bottleneck clear. Pure random shallow blind recovery is still weak (`2/18`), while scaffolded shallow proof is bounded and strong (`18/18`), perturbed true-tree basin recovery is strong (`9/9`), and blind depth performance drops after depth 3. That evidence supports the paper's claim that representation is not the main failure mode; search and post-processing are.

v1.6 therefore shifts the project from proving training boundaries to upgrading the recovery algorithm itself. The milestone targets a verifier-gated hybrid discrete-continuous pipeline: hardening and checkpoint snaps, exact-candidate ranking, low-margin discrete cleanup, post-snap constant refit, shorter compiler macros, and numerics/reporting changes that preserve scientific honesty.

## Last Completed Milestone: v1.5 Training Proof and Recovery Guarantees

**Goal shipped:** Prove the paper-grounded EML training claims with real training runs, bounded 100% recovery targets, transparent failure boundaries, metrics, and reproducible datasets.

**Shipped features:**
- Stable paper-claim matrix, deterministic proof datasets, proof-aware benchmark artifacts, and explicit threshold policies.
- Honest shallow proof split between measured pure-blind recovery and bounded scaffolded recovery.
- First-class perturbed true-tree basin recovery, local repair provenance, and Beer-Lambert basin-bound diagnostics.
- Deterministic depth-curve evidence across EML depths 2 through 6 with separate blind and perturbed reporting.
- One-command `artifacts/proof/v1.5/` bundle with raw runs, aggregates, plots, claim report, and milestone audit.

## Current Milestone: v1.6 Hybrid Search Pipeline and Exact Candidate Recovery

**Goal:** Turn the current MVP optimizer into a verifier-gated hybrid recovery pipeline that can improve exact candidate quality without weakening the repo's evidence contract or discarding existing artifacts.

**Target features:**
- Select the final answer from a pool of exact snapped candidates gathered across restarts and late hardening checkpoints, not only from the minimum soft-loss winner.
- Generalize local discrete repair into a target-free snap-neighborhood cleanup stage driven by low-margin ambiguity and exact AST deduplication.
- Add post-snap constant refit plus stronger numerical and domain diagnostics for `exp` and `log` sensitive paths.
- Shorten compiled EML trees with validated macro rules so warm-start coverage expands without removing fail-closed fallback behavior.
- Re-run proof and campaign evidence with explicit pure-blind versus scaffolded separation and weak-dominance reporting against archived v1.5 and v1.4 baselines.

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
- ✓ Paper claim matrix, deterministic proof dataset manifests, proof-aware artifacts, evidence classes, and explicit threshold policies — v1.5 Phase 29
- ✓ Honest shallow proof split between pure-blind measurement and scaffolded proof — v1.5 Phase 30
- ✓ Perturbed basin recovery, repair provenance, and Beer-Lambert bound evidence — v1.5 Phase 31
- ✓ Deterministic blind-versus-perturbed depth-curve evidence — v1.5 Phase 32
- ✓ One-command proof bundle and milestone audit rooted at `artifacts/proof/v1.5/` — v1.5 Phase 33

### Active

- [ ] Replace soft-loss-only winner selection with verifier-gated exact candidate pooling and ranking.
- [ ] Add target-free low-margin discrete cleanup so near-miss snaps can recover exact trees without access to a ground-truth AST.
- [ ] Add post-snap constant refit and stronger training-time numerical/domain controls without changing faithful verification semantics.
- [ ] Shorten the compiler with validated macro rules and expand warm-start coverage while preserving fail-closed fallback behavior.
- [ ] Re-run proof and campaign evidence with explicit weak-dominance claims, archived baselines, and separate reporting for pure blind, scaffolded blind, compile, warm-start, and perturbed-basin regimes.

### Out of Scope

- Guaranteed improvement on every unseen future formula - the defensible promise for v1.6 is weak dominance on declared benchmark selection, not universal success.
- Full blind recovery of arbitrary depth-6 formulas - the paper and v1.5 depth curve both show sharp degradation beyond shallow depths.
- Claiming warm-start same-AST return or scaffolded recovery as pure blind discovery - those evidence classes remain separate by design.
- Replacing or rewriting archived v1.5 proof artifacts or v1.4 campaign baselines - the milestone must preserve them as comparison anchors.
- Matched-budget external baseline competitions - important, but deferred until the hybrid recovery pipeline is materially stronger.
- Custom CUDA kernels - use normal PyTorch execution first and profile before adding kernels.
- A web GUI - the first target remains a reproducible package, CLI, tests, and artifacts.
- Formal theorem-prover equivalence - numeric, high-precision, and targeted symbolic checks remain sufficient for this stage.

## Context

The uploaded paper defines `eml(x, y) = exp(x) - ln(y)` and shows that EML plus the constant `1` generates the paper's scientific-calculator basis. It also shows that EML expressions form a regular binary grammar `S -> 1 | eml(S, S)`, which makes a complete depth-bounded master tree possible.

`sources/NORTH_STAR.md` turns that paper result into an implementation blueprint. Its core recommendation is a hybrid pipeline: continuous search, hardening, symbolic snapping, local discrete cleanup, and verification. It also warns that pure gradient descent is not enough because the paper's blind recovery success drops sharply with depth, while warm starts recover reliably from perturbed correct solutions.

The committed v1.5 proof bundle now shows the same pattern in this implementation. Representation is strong, verifier ownership is strong, and perturbed-basin return is strong, but blind discovery remains bottlenecked by soft-to-hard mismatch, brittle greedy snapping, limited compiler coverage, missing constant refit, and partial numerical controls. The user supplied a detailed milestone brief that grounds v1.6 in weak-dominance upgrades: preserve the old exact candidate as fallback, search over a larger exact candidate set, and only promote new stages when they improve verifier-owned outcomes.

## Constraints

- **Paper fidelity**: EML semantics, complete-tree construction, snapping, hardening, and complex arithmetic must stay grounded in `sources/paper.pdf` and `sources/NORTH_STAR.md`.
- **Verification**: A candidate is not "recovered" based on training loss alone; final selection is verifier-owned and exact-candidate based.
- **Non-destructive evidence**: v1.4 and v1.5 artifacts stay archived and comparable; new results cannot overwrite the historical benchmark anchors.
- **Weak dominance first**: Candidate-pool selection, beam cleanup, refit, and compiler macros must keep the current exact candidate available as fallback on declared benchmark paths.
- **Numerics**: Training defaults to PyTorch `complex128`, with training-mode guards only where needed and faithful verification afterwards.
- **Scope realism**: v1.6 must improve blind-discovery quality without overselling deep blind recovery or universal guarantees.
- **Demos**: Showcase examples must remain drawn from `sources/FOR_DEMO.md`, favoring normalized, dimensionless, visually distinctive laws.
- **Repository state**: This project now has archived milestone planning and proof artifacts that must remain inspectable after the rollover.

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
| v1.3 prioritizes showcase evidence over optimizer changes | The user wanted crisp numbers, graphs, and a real-life performance narrative before tuning the algorithm. | ✓ Good |
| Static reports before dashboards | CSV, SVG, and Markdown evidence proved the metrics before adding an interactive dashboard. | ✓ Good |
| v1.4 uses committed campaigns as the scoreboard | More baseline runs would mostly confirm the same weaknesses; the useful next step is targeted improvement followed by identical reruns. | ✓ Good |
| Primitive scaffolds are useful optimizer defaults but not pure blind proof | Phase 30 review found exact scaffold starts can recover verifier-owned candidates while still failing the paper/NORTH_STAR definition of blind recovery from random initialization. | ✓ Good |
| Diagnose Beer-Lambert before repairing it | High-perturbation failures needed mechanism-level evidence before deeper discrete repair work. | ✓ Good |
| Shockley template must validate before acceptance | Compiler expansion remains fail-closed and cannot emit invalid EML trees. | ✓ Good |
| Before/after comparison is the milestone gate | Recovery improvements are only credible when rerun through the same standard/showcase campaign contracts. | ✓ Good |
| v1.5 training proof must be bounded | The paper itself reports rapid blind degradation at depth; the defensible target was 100% over declared suites plus honest depth curves. | ✓ Good |
| Compile-only success does not prove training | v1.5 reports compiler-assisted cases separately and counts proof success only when actual training and verifier checks pass. | ✓ Good |
| Proof evidence must be claim-labeled | Phase 29 established stable paper claim IDs, threshold policies, dataset manifests, and derived evidence classes before running proof campaigns. | ✓ Good |
| Treat the optimizer as a candidate generator, not the whole symbolic-regression algorithm | The strongest current gap is the mismatch between soft optimization and hard exact-tree claims. | - Pending |
| Preserve the current exact candidate as fallback in every new recovery stage | Weak-dominance upgrades should not make declared benchmark cases worse by construction. | - Pending |
| Separate pure blind, scaffolded blind, compile, warm-start, and perturbed-basin evidence in every report | Honest regime separation is part of the scientific contribution, not just documentation. | - Pending |
| Defer matched-budget external baselines until the hybrid pipeline is stronger | External comparisons matter, but they should follow a materially improved blind-discovery engine. | - Pending |

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
*Last updated: 2026-04-16 after starting milestone v1.6*
