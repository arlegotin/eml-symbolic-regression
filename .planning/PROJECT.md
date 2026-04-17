# EML Symbolic Regression

## What This Is

This project implements a hybrid symbolic-regression engine based on the paper "All elementary functions from a single binary operator." It searches over complete depth-bounded EML trees, optimizes soft categorical choices with PyTorch, snaps the result into an exact EML tree, cleans it up symbolically, and verifies candidate formulas against held-out data and high-precision evaluators.

The current release is a research-grade Python package and CLI for recovering compact elementary laws from synthetic scientific datasets, with demos, benchmark campaigns, proof artifacts, centered/scaled operator-family experiments, and paper-decision artifacts drawn from `sources/FOR_DEMO.md`.

## Core Value

Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Current State: v1.9 In Progress

The repo now has strong representation, verification, reproducibility, proof-bundle, hybrid-search, compiler, and paper-decision foundations. Exact EML ASTs, soft master trees, compiler-driven warm starts, deterministic benchmark suites, campaign reports, one-command proof bundles, centered/scaled operator-family experiments, and paper-decision artifacts are all in place and archived through v1.8.

The current evidence says raw EML is representationally viable but blind basin finding degrades sharply with depth. Perturbed true-tree recovery remains strong, scaffolded/warm-start regimes are useful when clearly labeled, and centered-family evidence is negative under the supplied v1.8 setup.

v1.9 pivots from trying to rescue centered families as the main story toward a raw-EML hybrid paper path: Phase 49 fixed the centered scaffold correctness confound with an explicit raw-only scaffold witness registry, Phase 50 added normalized Arrhenius exact compiler warm-start evidence, and the next phases shorten Michaelis-Menten through reusable compiler motifs, strengthen verifier-gated exact cleanup, and generate a regime-separated raw-hybrid paper suite.

## Last Completed Milestone: v1.8 Centered-Family Viability and Full Evidence Run

**Goal:** Determine whether centered/scaled operator families are actually viable improvements over raw EML after fixing missing integration support, calibrating the family grid, running full evidence campaigns, and regenerating the paper decision artifacts.

**Shipped features:**
- Triage the v1.7 `family-smoke` failures and identify which centered-family gaps are implementation blockers versus genuine operator behavior.
- Add or explicitly gate centered warm-start, compiler-seed, initializer, and continuation support so full campaigns do not waste budget on known unsupported paths.
- Expand the family experiment grid to include fixed `s` variants and continuation schedules needed for a defensible raw-vs-centered comparison.
- Run scoped family evidence with recovery, anomaly, repair/refit, unsupported-rate, and regression-lock artifacts.
- Regenerate the paper decision package from v1.8 centered-family aggregates and choose the raw-EML searchability note path.

## Current Milestone: v1.9 Raw-EML Hybrid Recovery and Paper Suite

**Goal:** Produce a stronger raw-EML hybrid paper package by fixing centered scaffold correctness, adding Arrhenius exact recovery, materially improving Michaelis-Menten support, expanding exact cleanup, and generating a regime-separated paper-facing campaign.

**Target features:**
- Explicit operator-family witness registry that prevents raw `exp`/`log` scaffolds from running under centered semantics until true same-family witnesses exist.
- Arrhenius normalized demo with strict compiler support, exact warm-start recovery, tests, and reproducible artifacts.
- Reusable reciprocal-shift and saturation-ratio compiler motifs aimed at bringing Michaelis-Menten under the supported depth gate.
- Broader verifier-gated post-snap exact cleanup with AST deduplication, more candidate sources, and targeted before/after evidence.
- Raw-hybrid paper suite/report that keeps pure blind, scaffolded, warm-start, perturbed, repaired, and centered-negative evidence regimes separate.

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
- ✓ Verifier-gated exact-candidate pooling across restarts and hardening checkpoints — v1.6 Phase 34
- ✓ Target-free low-margin discrete cleanup with fallback-preserving exact candidate artifacts — v1.6 Phase 35
- ✓ Post-snap constant refit and richer numerical/domain diagnostics — v1.6 Phase 36
- ✓ Macro-aware compiler shortening and conservative warm-start coverage expansion — v1.6 Phase 37
- ✓ Regime-aware proof/campaign reporting, immutable anchor locks, and aggregate-level hybrid regression locks — v1.6 Phase 38
- ✓ Final `artifacts/proof/v1.6/` evidence bundle regenerated and verified from the archived code state — v1.6 closeout
- ✓ Centered/scaled EML semantics, exact ASTs, serialization, mpmath/SymPy export, and shifted-singularity diagnostics — v1.7 Phase 39
- ✓ Family-aware training, snapping, repair/refit, benchmark budgets, schedules, and raw-default regression coverage — v1.7 Phase 40
- ✓ v1.7 raw-vs-centered family benchmark suites and campaign presets — v1.7 Phase 41
- ✓ Operator-family recovery tables, diagnostics tables, comparison Markdown, and regression-lock JSON outputs — v1.7 Phase 42
- ✓ Paper decision package with safe claims, unsafe claims, figure inventory, and incomplete completeness boundary — v1.7 Phase 43
- ✓ Expanded v1.8 family smoke triage, calibration, same-family seed gates, scoped evidence manifest, and raw-EML paper decision package — v1.8 Phases 44-48
- ✓ Explicit raw-only scaffold witness registry, centered-family scaffold exclusions, direct helper fail-closed guards, and artifact reason-code visibility — v1.9 Phase 49
- ✓ Normalized Arrhenius demo, strict `direct_division_template` compile support, exact same-AST warm-start return, and focused `v1.9-arrhenius-evidence` artifacts — v1.9 Phase 50

### Active

- [ ] Add reciprocal/saturation compiler motifs and materially reduce Michaelis-Menten compile depth, preferably to supported exact recovery.
- [ ] Strengthen verifier-gated exact post-snap cleanup without changing the recovery contract.
- [ ] Generate a raw-hybrid paper-facing campaign/report with regime-separated claims and centered-family caveats.

### Out of Scope

- Guaranteed improvement on every unseen future formula - the defensible promise for v1.7 is measured comparison on declared benchmark and proof suites, not universal success.
- Full blind recovery of arbitrary depth-6 formulas - the paper and v1.5/v1.6 depth curves both show sharp degradation beyond shallow depths.
- Claiming warm-start same-AST return or scaffolded recovery as pure blind discovery - those evidence classes remain separate by design.
- Claiming `CEML_s` is a full Sheffer successor family without constructive proof - v1.7 may search for evidence, but must not overclaim completeness.
- Treating `ZEML_s` as a formal terminal-1 completeness replacement - closed zero-terminal trees collapse to zero, so `ZEML_s` is a training-centered form.
- Replacing or rewriting archived v1.5 proof artifacts or v1.4 campaign baselines - the milestone must preserve them as comparison anchors.
- Matched-budget external baseline competitions - important, but deferred until the hybrid recovery pipeline is materially stronger.
- Custom CUDA kernels - use normal PyTorch execution first and profile before adding kernels.
- A web GUI - the first target remains a reproducible package, CLI, tests, and artifacts.
- Formal theorem-prover equivalence - numeric, high-precision, and targeted symbolic checks remain sufficient for this stage.

## Context

The uploaded paper defines `eml(x, y) = exp(x) - ln(y)` and shows that EML plus the constant `1` generates the paper's scientific-calculator basis. It also shows that EML expressions form a regular binary grammar `S -> 1 | eml(S, S)`, which makes a complete depth-bounded master tree possible.

`sources/NORTH_STAR.md` turns that paper result into an implementation blueprint. Its core recommendation is a hybrid pipeline: continuous search, hardening, symbolic snapping, local discrete cleanup, and verification. It also warns that pure gradient descent is not enough because the paper's blind recovery success drops sharply with depth, while warm starts recover reliably from perturbed correct solutions.

The committed v1.6 proof bundle now gives the stable evidence base for a research pivot. Representation is strong, verifier ownership is strong, scaffolded and perturbed-basin regimes are strong, and pure-blind discovery remains the honest weak point. v1.7 built the centered/scaled exp-log transport infrastructure, but did not run the full centered evidence matrix.

A quick post-v1.7 `family-smoke` run showed that full campaigns should not be launched blindly yet: raw EML recovered the smoke `exp` blind case and Beer-Lambert warm-start case, while centered `exp` blind variants failed and centered warm-start paths were explicitly unsupported. v1.8 fixed or gated those paths, ran scoped evidence, and selected the raw-EML searchability note path.

v1.8 found no positive centered-family recovery signal under the scoped local setup and identified a centered scaffold correctness confound: raw `exp`/`log` scaffold helpers are semantically raw witnesses and must not be silently reused for `CEML_s` or `ZEML_s`. Phase 49 resolved that by adding an explicit scaffold witness registry, raw-only `exp`/`log`/`scaled_exp` entries, centered-family `centered_family_same_family_witness_missing` exclusions, and fail-closed raw helper guards. v1.9 should continue treating centered families as a paused constructive-theory track while focusing empirical effort on raw-EML motif-guided exact recovery.

## Constraints

- **Paper fidelity**: EML semantics, complete-tree construction, snapping, hardening, and complex arithmetic must stay grounded in `sources/paper.pdf` and `sources/NORTH_STAR.md`.
- **Verification**: A candidate is not "recovered" based on training loss alone; final selection is verifier-owned and exact-candidate based.
- **Non-destructive evidence**: v1.4 and v1.5 artifacts stay archived and comparable; new results cannot overwrite the historical benchmark anchors.
- **Centered-family honesty**: `cEML_{s,t}`, `CEML_s`, and `ZEML_s` must be reported as operator-family experiments unless constructive interdefinability or completeness evidence is actually produced.
- **Numerics**: Training defaults to PyTorch `complex128`, with training-mode guards only where needed and faithful verification afterwards.
- **Scope realism**: v1.8 must compare search geometry without overselling deep blind recovery, universal guarantees, or unproved successor-family completeness.
- **Run discipline**: Full family campaigns should run only after smoke/calibration blockers are fixed or explicitly gated, so expensive artifacts answer the scientific question rather than restating known missing support.
- **Demos**: Showcase examples must remain drawn from `sources/FOR_DEMO.md`, favoring normalized, dimensionless, visually distinctive laws.
- **Repository state**: This project now has archived milestone planning and proof artifacts that must remain inspectable after the rollover.
- **Witness honesty**: Raw EML witness/scaffold helpers are raw-only unless a same-family centered witness is explicitly constructed and tested.
- **Reusable motifs**: Compiler improvements should target reusable structures such as reciprocal shifts and saturation ratios, not one-off formula recognizers.
- **Paper claims**: Warm-start, same-AST return, scaffolded recovery, repair, refit, and pure-blind discovery must remain separately labeled in all v1.9 outputs.

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
| Treat the optimizer as a candidate generator, not the whole symbolic-regression algorithm | The strongest current gap is the mismatch between soft optimization and hard exact-tree claims. | ✓ Good |
| Preserve the current exact candidate as fallback in every new recovery stage | Weak-dominance upgrades should not make declared benchmark cases worse by construction. | ✓ Good |
| Separate pure blind, scaffolded blind, compile, warm-start, and perturbed-basin evidence in every report | Honest regime separation is part of the scientific contribution, not just documentation. | ✓ Good |
| Defer matched-budget external baselines until the hybrid pipeline is stronger | External comparisons matter, but they should follow a materially improved blind-discovery engine. | ⚠️ Revisit for paper |
| v1.7 tests centered/scaled EML transports before writing the flagship paper | v1.6 evidence shows representation and basin return are strong while raw blind search geometry remains the dominant bottleneck. | ✓ Good |
| Use `CEML_s` for unit-terminal/formal successor claims and `ZEML_s` for training-centered comparisons | Zero-terminal centered trees do not generate new constants from closed trees, so training convenience and formal completeness must stay separate. | ✓ Good |
| v1.8 treats centered-family performance as unknown until blocker fixes and full campaigns run | The v1.7 infrastructure shipped without full centered evidence, and the quick smoke check showed centered failures and unsupported warm-start paths. | ✓ Good |
| v1.8 does not support a centered-family improvement paper from the supplied local evidence | Expanded smoke, calibration, and scoped standard aggregates show raw EML recovery at 80.0% and best centered recovery at 0.0%. | ✓ Good |
| The near-term paper path is a raw-EML searchability note | Centered variants are useful negative diagnostics but not an empirical improvement under v1.8 evidence. | ✓ Good |
| v1.9 pivots to raw-EML hybrid recovery rather than centered-family rescue | The strongest evidence is representation viability, blind-search depth limits, and reliable basin return near exact witnesses. | — Pending |
| Centered empirical scaling pauses until same-family witnesses exist | Current centered results are negative, and Phase 49 now blocks raw scaffold reuse under centered semantics while preserving the same-family witness caveat. | ✓ Good |
| Arrhenius exact warm-start evidence is same-AST evidence, not blind discovery | Phase 50 records `same_ast_return`, verifier `recovered`, and evidence class `same_ast` for `arrhenius-warm`. | ✓ Good |
| Focused scientific-law evidence should stay out of broad campaign denominators until paper packaging | Phase 50 isolates Arrhenius in `v1.9-arrhenius-evidence` rather than altering v1.3/v1.8 suites. | ✓ Good |
| Michaelis-Menten is the preferred next compiler/search win before Planck | Michaelis is near the support gate while Planck remains materially deeper under current compile diagnostics. | — Pending |
| Raw scaffold helpers are registry-gated by operator family | Phase 49 proved current `exp`, `log`, and `scaled_exp` scaffold witnesses are raw EML only; centered runs now record missing same-family witness exclusions instead of reusing raw helpers. | ✓ Good |

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
*Last updated: 2026-04-17 after completing Phase 50*
