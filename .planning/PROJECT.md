# EML Symbolic Regression

## What This Is

This project implements a hybrid symbolic-regression engine based on the paper "All elementary functions from a single binary operator." It searches over complete depth-bounded EML trees, optimizes soft categorical choices with PyTorch, snaps the result into an exact EML tree, cleans it up symbolically, and verifies candidate formulas against held-out data and high-precision evaluators.

The current release is a research-grade Python package and CLI for recovering compact elementary laws from scientific datasets, with demos, benchmark campaigns, proof artifacts, centered/scaled/GEML operator-family experiments, publication evidence, claim audits, and release-gate artifacts drawn from `sources/FOR_DEMO.md`.

## Core Value

Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Current State: v1.17 Complete

The repo now has strong representation, verification, reproducibility, proof-bundle, hybrid-search, compiler, motif-library, paper-package, current-code training, diagnostics, figure-asset, CI, dataset, baseline, release-gate, claim-integrity, GEML-family, and i*pi evidence foundations. Exact EML ASTs, soft master trees, compiler-driven warm starts, deterministic benchmark suites, campaign reports, proof bundles, centered/scaled/GEML operator-family experiments, paper-decision artifacts, and source-locked publication packages are all in place and archived through v1.16.

The current evidence says raw EML is representationally viable but blind basin finding degrades sharply with depth. Perturbed true-tree recovery remains strong, scaffolded/warm-start regimes are useful when clearly labeled, centered-family evidence is negative under the supplied v1.8 setup, and v1.9 has a verified raw-hybrid paper package that keeps those regimes separate.

v1.10 expanded the compiler from a small set of useful macros into a search-backed reusable motif library. Logistic now has structural exponential-saturation compile support at relaxed depth 15, down from 27, but remains above the strict depth-13 gate. Planck now has validation-backed low-degree power compression and relaxed depth 14, down from 20, but also remains above the strict gate. Focused campaign artifacts record both outcomes as unsupported diagnostics with no warm-start promotion.

v1.11 adds the paper-strength evidence layer: real current-code training artifacts, low-hanging ablation and prediction-only baseline diagnostics, deterministic SVG/source-table assets, and a final source-locked package at `artifacts/paper/v1.11/` with a passing claim audit. The paper is now defensible as a verifier-gated hybrid EML symbolic-regression methods/evidence paper with explicit boundaries, not as broad blind symbolic-regression superiority.

v1.12 turns the evidence package into a paper-shaped argument. The repo now has `artifacts/paper/v1.11/draft/` with section skeletons, claim taxonomy, captions, motif evolution, negative-result tables, and a pipeline figure; `artifacts/campaigns/v1.12-evidence-refresh/` with current-code shallow/depth refreshes; and `artifacts/paper/v1.11/v1.12-supplement/` with 49 source locks and a passing claim audit. Conventional symbolic-regression comparison remains unavailable locally, and logistic remains unsupported at the strict gate, both recorded explicitly.

v1.13 hardens that paper-shaped evidence into a publication-grade release gate. The repo now has a clean-room `publication-rebuild` path, locked provenance, stronger verifier and split discipline, guarded/faithful semantics controls, CI/public snapshot validation, separated basis-only and literal-constant benchmark tracks, expanded dataset manifests, a matched baseline harness, and a committed v1.13 evidence package with a passing claim audit and release gate.

v1.14 repaired the public claim surface before further paper work. Compile-only verified support is no longer counted as trained exact recovery, zero-perturbation same-AST warm-start rows are labeled exact seed round-trips, unsupported baseline rows are quarantined from main comparison claims, and multivariate verifier target lookup now uses the full input row when needed. The corrected publication package is under `artifacts/paper/v1.14/`.

v1.15 added the parameterized `GEML_a(x, y) = exp(a*x) - log(y)/a` family with raw EML and i*pi EML named specializations, restricted i*pi theory and branch diagnostics, family-aware training/snap integration, matched oscillatory/negative-control protocols, paired campaign outputs, and a claim-safe package under `artifacts/paper/v1.15-geml/`. The package decision is `inconclusive_smoke_only`, not a positive i*pi EML paper-section claim.

v1.16 completed the paper-strength GEML/i*pi evidence workflow and produced a source-locked package under `artifacts/paper/v1.16-geml/`. The result is useful but not paper-positive: the final decision is `inconclusive`, `paper_claim_allowed` is `false`, the pilot evidence has 12 paired rows across 2 unique seeds, and both raw EML and i*pi EML have 0 verifier-gated exact recoveries. The full campaign was correctly stopped fail-closed because the signal remained loss-only.

v1.17 attacked the bottleneck exposed by v1.16: promising soft/loss behavior did not survive snapping into exact verified formulas. The milestone added snap-margin diagnostics, bounded exact-tree neighborhood search, verifier-first candidate ranking, a natural-bias recovery sandbox, and a source-locked package under `artifacts/paper/v1.17-geml/`. The final decision is `still_inconclusive`; broader i*pi/GEML campaigns remain blocked.

## Last Completed Milestone: v1.17 Snap-First Exact Recovery and Candidate Neighborhood Search

**Goal:** Determine whether snap-first diagnostics and target-agnostic exact-neighborhood search could turn v1.16 loss-only near misses into verifier-gated exact recovery before reopening broader i*pi/GEML campaigns.

**Shipped features:**

- Snap diagnostics for selected, fallback, failed, and loss-only candidates, including low-margin slot and soft-versus-hard mismatch payloads.
- Bounded exact-tree neighborhood generation with original/fallback provenance and target-leakage guards.
- Verifier-first candidate ranking that keeps exact recovery, equivalence, repair-only, loss-only, same-AST, compile-only, fallback, and original-snap classes separated.
- Focused sandbox gate for natural-bias exact-recovery signal with negative-control visibility.
- Final v1.17 package under `artifacts/paper/v1.17-geml/` with decision `still_inconclusive`, source locks OK, and passing claim audit.

## Current Milestone

None active. Start the next milestone with `$gsd-new-milestone` after choosing whether to address the v1.17 candidate-boundary blocker or pivot to another bounded research question.

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
- ✓ Reusable `reciprocal_shift_template` and `saturation_ratio_template` compiler motifs, Michaelis-Menten strict support, same-AST warm-start return, and focused `v1.9-michaelis-evidence` artifacts — v1.9 Phase 51
- ✓ Opt-in expanded candidate-pool cleanup over selected/fallback/retained exact roots, verifier-gated AST dedup, repair metrics, and focused `v1.9-repair-evidence` no-improvement evidence — v1.9 Phase 52
- ✓ Regime-separated raw-hybrid paper package with source locks, scientific-law tables, claim boundaries, docs, and regression locks — v1.9 Phase 53
- ✓ Archived compiler baselines for logistic, Planck, Michaelis-Menten, Arrhenius, and Shockley before motif-library changes — v1.10 Phase 54
- ✓ Generalized reciprocal and saturation motifs over validated compilable subexpressions with validation-visible diagnostics and fail-closed behavior — v1.10 Phase 55
- ✓ Structural exponential-saturation motif for logistic-like laws, lowering logistic relaxed depth from 27 to 15 while preserving strict unsupported status — v1.10 Phase 56
- ✓ Bounded motif-search evidence and validation-backed low-degree power compression, lowering Planck relaxed depth from 20 to 14 while preserving unsupported/stretch honesty — v1.10 Phase 57
- ✓ Focused logistic and Planck benchmark suites, CLI artifact paths, campaign evidence, and tests recording unsupported diagnostics with no warm-start promotion — v1.10 Phase 58
- ✓ Versioned v1.11 raw-hybrid paper package contract with source locks, claim ledger, and current v1.10 logistic/Planck scientific-law rows — v1.11 Phase 59
- ✓ Current-code v1.11 training campaigns covering pure blind, scaffolded, same-AST warm-start, perturbed-basin, and logistic/Planck probe regimes — v1.11 Phase 60
- ✓ v1.11 motif-depth, regime-comparison, repair/refit, and prediction-only baseline diagnostic tables with source locks — v1.11 Phase 61
- ✓ Deterministic v1.11 paper asset pipeline with source tables, SVG figures, per-figure metadata, and source locks — v1.11 Phase 62
- ✓ Final v1.11 paper package with root manifest, 67 source-lock rows, reproduction commands, paper-readiness summary, and passing claim audit — v1.11 Phase 63
- ✓ v1.12 paper draft skeleton with section files, claim taxonomy, figure captions, and table captions — v1.12 Phase 64/66
- ✓ Current-code shallow and depth evidence refresh with regime-separated source tables — v1.12 Phase 65
- ✓ Paper-facing motif evolution, pipeline figure, and logistic/Planck negative-result tables — v1.12 Phase 66
- ✓ Bounded conventional SR baseline status and logistic strict-support probe with no unsupported promotion — v1.12 Phase 67
- ✓ v1.12 supplement with 49 source locks, reproduction commands, and passing claim audit — v1.12 Phase 68
- ✓ Clean-room publication rebuild, locked provenance, source locks, and placeholder-metadata rejection — v1.13 Phase 69
- ✓ Layered verifier evidence and final-confirmation split isolation — v1.13 Phase 70
- ✓ Guarded/faithful training semantics controls and mismatch diagnostics — v1.13 Phase 71
- ✓ CI hardening, evidence-regression tests, and public snapshot validation — v1.13 Phase 72
- ✓ Basis-only and literal-constant benchmark tracks with separate denominators — v1.13 Phase 73
- ✓ Expanded dataset manifests for noisy, identifiability, multivariable, unit-aware, and real data — v1.13 Phase 74
- ✓ Matched baseline harness with fail-closed optional external adapters — v1.13 Phase 75
- ✓ Full v1.13 evidence package, claim audit, release gate, and milestone audit — v1.13 Phase 76
- ✓ Two-axis recovery accounting and corrected trained-recovery headlines excluding compile-only support — v1.14 Phase 77
- ✓ Warm-start evidence relabeling that distinguishes exact seed round-trips from robustness claims — v1.14 Phase 78
- ✓ Baseline claim-surface quarantine for unavailable or unsupported external baselines — v1.14 Phase 79
- ✓ Multivariate high-precision verifier target matching by full input row — v1.14 Phase 80
- ✓ Corrected v1.14 publication package, source locks, claim audit, and release gate — v1.14 Phase 81
- ✓ Fixed-parameter `GEML_a` semantics with raw and i*pi named specializations — v1.15 Phase 82
- ✓ Restricted i*pi theory artifacts, branch convention, and branch diagnostics — v1.15 Phase 83
- ✓ Family-aware training, snapping, verifier metrics, and raw-regression preservation — v1.15 Phase 84
- ✓ Matched oscillatory, log-periodic, and negative-control benchmark protocols — v1.15 Phase 85
- ✓ Paired raw EML versus i*pi EML campaign outputs and diagnostics — v1.15 Phase 86
- ✓ Final v1.15 GEML evidence package with claim audit and bounded decision — v1.15 Phase 87
- ✓ Paper-strength i*pi/GEML exact-recovery gate and matched campaign contract — v1.16 Phase 88
- ✓ Branch-safe i*pi initializer metadata and raw-regression preservation — v1.16 Phase 89
- ✓ Smoke/pilot budget ladder with fail-closed full-campaign gate — v1.16 Phase 90
- ✓ Full-campaign stop package with source-locked negative/inconclusive evidence — v1.16 Phase 91
- ✓ Ablations, failure taxonomy, and deterministic paper figures for v1.16 GEML evidence — v1.16 Phase 92
- ✓ Final v1.16 decision package, source locks, and passing claim audit — v1.16 Phase 93
- ✓ Snap-margin, active-slot, and soft-versus-hard mismatch diagnostics for loss-only and failed pilot candidates — v1.17 Phase 94
- ✓ Bounded exact-tree neighborhoods around snapped candidates without formula-name recognizers or exact target leakage — v1.17 Phase 95
- ✓ Verifier-first candidate ranking and promotion before post-snap loss can influence claims — v1.17 Phase 96
- ✓ Tiny matched natural-bias recovery sandbox with negative-control gate before broader campaign reopening — v1.17 Phase 97
- ✓ v1.17 evidence package with before/after exact-recovery signal, failure taxonomy reference, source locks, and claim-safe next-campaign decision — v1.17 Phase 98

### Active

None. The next milestone has not been defined yet.

### Out of Scope

- Guaranteed improvement on every unseen future formula - the defensible promise for v1.7 is measured comparison on declared benchmark and proof suites, not universal success.
- Full blind recovery of arbitrary depth-6 formulas - the paper and v1.5/v1.6 depth curves both show sharp degradation beyond shallow depths.
- Claiming warm-start same-AST return or scaffolded recovery as pure blind discovery - those evidence classes remain separate by design.
- Claiming `CEML_s` is a full Sheffer successor family without constructive proof - v1.7 may search for evidence, but must not overclaim completeness.
- Treating `ZEML_s` as a formal terminal-1 completeness replacement - closed zero-terminal trees collapse to zero, so `ZEML_s` is a training-centered form.
- Replacing or rewriting archived v1.5 proof artifacts or v1.4 campaign baselines - the milestone must preserve them as comparison anchors.
- Custom CUDA kernels - use normal PyTorch execution first and profile before adding kernels.
- A web GUI - the first target remains a reproducible package, CLI, tests, and artifacts.
- Broad blind symbolic-regression superiority claims - the publication can claim only what the locked evidence and matched baselines support.
- Formal theorem-prover equivalence as a release blocker - targeted symbolic equivalence, interval/certificate checks, and strong falsification are in scope; full theorem proving remains future work unless explicitly adopted.
- Manuscript prose that oversteps the v1.13 claim audit - prose can now proceed, but it must stay inside the verified evidence boundaries.
- Claiming full `GEML_a` or i*pi EML universality without a constructive proof - v1.15 targets restricted-domain theorems and empirical comparison first.
- Claiming i*pi EML is globally better than EML - any positive result must be tied to the declared oscillatory/phase-log benchmark class and balanced by negative controls.
- Treating branch behavior as an implementation detail - for i*pi EML the principal branch convention, cut diagnostics, and safe-domain restrictions are part of the operator contract.

## Context

The uploaded paper defines `eml(x, y) = exp(x) - ln(y)` and shows that EML plus the constant `1` generates the paper's scientific-calculator basis. It also shows that EML expressions form a regular binary grammar `S -> 1 | eml(S, S)`, which makes a complete depth-bounded master tree possible.

`sources/NORTH_STAR.md` turns that paper result into an implementation blueprint. Its core recommendation is a hybrid pipeline: continuous search, hardening, symbolic snapping, local discrete cleanup, and verification. It also warns that pure gradient descent is not enough because the paper's blind recovery success drops sharply with depth, while warm starts recover reliably from perturbed correct solutions.

The committed v1.6 proof bundle now gives the stable evidence base for a research pivot. Representation is strong, verifier ownership is strong, scaffolded and perturbed-basin regimes are strong, and pure-blind discovery remains the honest weak point. v1.7 built the centered/scaled exp-log transport infrastructure, but did not run the full centered evidence matrix.

A quick post-v1.7 `family-smoke` run showed that full campaigns should not be launched blindly yet: raw EML recovered the smoke `exp` blind case and Beer-Lambert warm-start case, while centered `exp` blind variants failed and centered warm-start paths were explicitly unsupported. v1.8 fixed or gated those paths, ran scoped evidence, and selected the raw-EML searchability note path.

v1.8 found no positive centered-family recovery signal under the scoped local setup and identified a centered scaffold correctness confound: raw `exp`/`log` scaffold helpers are semantically raw witnesses and must not be silently reused for `CEML_s` or `ZEML_s`. v1.9 resolved that confound, added focused Arrhenius and Michaelis-Menten same-AST warm-start evidence, measured expanded cleanup as repair-only no-improvement evidence, and generated a raw-hybrid paper package with locked source artifacts and regime-separated claims.

The v1.13 audit changed the priority from paper shaping to publication hardening. That work is now complete: a fresh checkout has a publication rebuild entrypoint, verifier evidence is layered and labeled, final confirmation is separated from model selection, training guard mismatch is surfaced in artifacts, and conventional baselines plus broader datasets are reported under standardized manifests and harnesses.

The post-v1.13 public-materials audit found a higher-priority claim-integrity issue: compile-only verified support was still counted inside the recovered headline even though the prose correctly says compiler output is not trained recovery. v1.14 fixes that accounting model before manuscript or release work continues. The same audit also flagged weak warm-start wording, baseline harness overexposure, and a latent multivariate verifier target-matching bug.

v1.15 shifted from claim-surface repair back to operator-family research. The repo now supports `GEML_a(x, y) = exp(a*x) - log(y)/a` as a fixed-parameter family around EML, with `a = i*pi` as a phase-log specialization whose real-axis sensitivity is bounded while its second-slot log branch is explicit. The milestone classified what is true on controlled domains and produced a claim-safe matched-protocol package; the current evidence is inconclusive rather than paper-section positive.

v1.16 tested whether that inconclusive state could become paper-strength evidence under matched raw/i*pi protocols. It did not find verifier-gated exact recovery: both raw and i*pi had 0 exact recoveries in the 12-row paired pilot, all useful signal remained loss-only, and the full campaign was stopped fail-closed. That result is a good engineering outcome but an inconclusive scientific outcome.

v1.17 responds by moving earlier in the failure chain. Before spending more budget on broader campaigns, it focuses on why soft candidates fail at the snap boundary, whether bounded exact-tree neighborhoods can repair near misses without target leakage, and whether verifier-first candidate ranking can surface any real exact-recovery signal on natural-bias targets.

## Constraints

- **Paper fidelity**: EML semantics, complete-tree construction, snapping, hardening, and complex arithmetic must stay grounded in `sources/paper.pdf` and `sources/NORTH_STAR.md`.
- **Verification**: A candidate is not "recovered" based on training loss alone; final selection is verifier-owned and exact-candidate based.
- **Non-destructive evidence**: v1.4 and v1.5 artifacts stay archived and comparable; new results cannot overwrite the historical benchmark anchors.
- **Centered-family honesty**: `cEML_{s,t}`, `CEML_s`, and `ZEML_s` must be reported as operator-family experiments unless constructive interdefinability or completeness evidence is actually produced.
- **Numerics**: Training defaults to PyTorch `complex128`, with training-mode guards only where needed and faithful verification afterwards.
- **Scope realism**: Future milestones must not oversell deep blind recovery, universal guarantees, or unproved successor-family completeness.
- **Run discipline**: Full family campaigns should run only after smoke/calibration blockers are fixed or explicitly gated, so expensive artifacts answer the scientific question rather than restating known missing support.
- **Demos**: Showcase examples must remain drawn from `sources/FOR_DEMO.md`, favoring normalized, dimensionless, visually distinctive laws.
- **Repository state**: This project now has archived milestone planning and proof artifacts that must remain inspectable after the rollover.
- **Witness honesty**: Raw EML witness/scaffold helpers are raw-only unless a same-family centered witness is explicitly constructed and tested.
- **Reusable motifs**: Compiler improvements should target reusable structures such as reciprocal shifts and saturation ratios, not one-off formula recognizers.
- **Paper claims**: Warm-start, same-AST return, scaffolded recovery, repair, refit, and pure-blind discovery must remain separately labeled in all v1.9 outputs.
- **Motif honesty**: Logistic and Planck improvements must come from reusable structural motifs or search-backed validated templates, not formula-name branches, exact-constant recognizers, or silent gate relaxation.
- **Clean-room publication**: Paper-facing artifacts must be regenerated from source commands in a locked environment; publication claims cannot depend on undeclared preexisting local files.
- **Provenance**: Placeholder snapshot metadata such as `1970-01-01T00:00:00+00:00` or `"snapshot"` cannot appear in final publication manifests except as explicitly labeled deterministic-test fixtures.
- **Split discipline**: Held-out, extrapolation, and final confirmation data must not rank or select candidates unless symbolic equivalence has already been established.
- **Verifier strength**: Numeric agreement alone is insufficient for publication claims; verifier outputs must label symbolic, randomized, adversarial, interval/certificate, and final-confirmation evidence separately.
- **Release branch discipline**: Work happens on `dev`; `main` receives only the intended public code, tests, CI, and publication artifacts after the full evidence rebuild passes.
- **Recovery accounting**: Compile-only verification may support representability, but `start_mode=compile` must never increment trained recovery headlines.
- **Warm-start honesty**: Zero-perturbation, one-step, same-AST warm-start rows are exact seed round-trips unless a nonzero perturbation grid with multiple seeds and enough optimization budget demonstrates basin robustness.
- **Baseline honesty**: Baseline harness rows with unavailable dependencies, unsupported adapters, or excluded denominators cannot carry main-text comparison claims.
- **GEML parameter domain**: `GEML_a` requires nonzero complex `a`; `a = 1` and `a = i*pi` must be explicit named cases, not magic constants hidden inside evaluators.
- **Theorem honesty**: v1.15 may prove restricted-domain identities and closure results, but must not claim the EML paper's full scientific-calculator completeness unless a constructive proof is present.
- **Matched comparison**: EML and i*pi EML comparisons must use the same depths, optimizer, initialization budget, snap rule, datasets, and verifier gates unless a deviation is recorded.
- **Branch discipline**: i*pi EML artifacts must state the log branch convention and expose branch-cut proximity/crossing diagnostics.
- **Paper-strength gate**: Positive i*pi/GEML claims still require exact verifier-gated recovery improving over raw EML on a declared natural-bias family under a matched protocol.
- **Negative-control discipline**: Negative controls remain in the denominator or in an explicit companion table; they cannot be hidden because they weaken the story.
- **Formula-leakage ban**: New initializers, priors, and candidate-pooling mechanisms must be generic to target families and cannot encode exact formula names or exact target trees.
- **Fail-closed paper package**: If the evidence remains weak, a milestone must produce a negative or inconclusive package rather than relaxing the recovery definition.
- **v1.16 package preservation**: `artifacts/paper/v1.16-geml/` is the source-locked record of the inconclusive result and must not be rewritten to imply a stronger claim.
- **Snap-first discipline**: v1.17 should not launch larger matched campaigns until snap/neighborhood work produces at least one verifier-gated exact-recovery signal under the tiny sandbox.
- **Exact-neighborhood honesty**: Local exact-tree search may repair candidates, but accepted moves must be provenance-labeled and verifier-owned; post-snap loss alone cannot promote a result.

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
| v1.9 pivots to raw-EML hybrid recovery rather than centered-family rescue | The strongest evidence is representation viability, blind-search depth limits, and reliable basin return near exact witnesses. | ✓ Good |
| Centered empirical scaling pauses until same-family witnesses exist | Current centered results are negative, and Phase 49 now blocks raw scaffold reuse under centered semantics while preserving the same-family witness caveat. | ✓ Good |
| Arrhenius exact warm-start evidence is same-AST evidence, not blind discovery | Phase 50 records `same_ast_return`, verifier `recovered`, and evidence class `same_ast` for `arrhenius-warm`. | ✓ Good |
| Focused scientific-law evidence should stay out of broad campaign denominators until paper packaging | Phase 50 isolates Arrhenius in `v1.9-arrhenius-evidence` rather than altering v1.3/v1.8 suites. | ✓ Good |
| Michaelis-Menten is the preferred next compiler/search win before Planck | Michaelis was near the support gate and Phase 51 brought it under the strict gate with reusable motifs while Planck remains stretch. | ✓ Good |
| Reciprocal and saturation macros must stay structural and validation-gated | Phase 51 review fixes enforced constant policy, finite derived constants, explicit unit-coefficient support, and non-unit rejection. | ✓ Good |
| Michaelis-Menten support is same-AST compiler warm-start evidence, not blind discovery | Phase 51 records `same_ast_return`, verifier `recovered`, and evidence class `same_ast` for `michaelis-warm`. | ✓ Good |
| Raw scaffold helpers are registry-gated by operator family | Phase 49 proved current `exp`, `log`, and `scaled_exp` scaffold witnesses are raw EML only; centered runs now record missing same-family witness exclusions instead of reusing raw helpers. | ✓ Good |
| Expanded exact cleanup is repair-only evidence | Phase 52 can opt into selected/fallback/retained candidate roots and records no-improvement focused evidence; repaired candidates remain `repaired_candidate`, not blind, compile-only, same-AST, or perturbed true-tree recovery. | ✓ Good |
| v1.10 prioritizes reusable compiler motifs over reporting work or gate changes | Logistic and Planck are high-visibility unsupported laws, and prior Shockley/Arrhenius/Michaelis wins came from reusable motif compression rather than looser recovery claims. | ✓ Good |
| v1.12 prioritizes paper-shaped argument over broad new algorithm work | v1.11 already organized the evidence; the highest-leverage next step is to turn it into a draft skeleton while refreshing small, credibility-critical evidence gaps. | ✓ Good |
| v1.12 treats conventional SR and logistic strict support as bounded probes | Both could help the paper, but dependency availability and compiler success are uncertain, so the milestone should record attempt/deferred/failure outcomes without blocking draft assembly. | ✓ Good |
| v1.13 is a publication gate, not a prose milestone | The audit surfaced reproducibility, validation, leakage, baseline, dataset, and release-branch gaps that had to be resolved before manuscript polish could be credible. | ✓ Good |
| Matched-budget baselines are now in scope | External SR comparison was deferred while the hybrid pipeline matured; publication now requires a standardized comparator harness or a clearly failed, source-locked attempt. | ✓ Good |
| Final confirmation is separate from candidate selection | Held-out/extrapolation performance can diagnose candidates, but publication recovery claims need untouched confirmation unless symbolic equivalence is proven. | ✓ Good |
| `main` updates only after the full rebuild passes | The public branch should receive publication-ready code and artifacts, not intermediate dev-only evidence. | ✓ Good |
| Direct local force-pushes are not part of release closeout | Phase 76 validates the public snapshot and records readiness for the publish workflow; remote publication remains a workflow action. | ✓ Good |
| v1.14 prioritizes claim-accounting repair before manuscript polish | Public materials must not mix compile-only support, same-AST seed retention, and trained recovery in one headline. | ✓ Good |
| v1.15 frames i*pi EML as a `GEML_a` specialization | The family story is stronger than presenting one isolated operator, and it keeps EML as the `a = 1` reference point. | ✓ Good |
| v1.15 proves restricted-domain theorems before making broad claims | The original EML paper has a constructive completeness result; this milestone should not imply the same for i*pi EML without proof. | ✓ Good |
| v1.15 benchmarks matched structural bias plus negative controls | i*pi EML is expected to help oscillatory/phase-log laws if it helps at all; credible reporting needs both its natural class and cases where EML may remain better. | ✓ Good |
| v1.16 optimized for paper-strength evidence but kept verifier-owned recovery | Strong results mattered for the paper, but weakening exact recovery would have made the result less publishable, not more. | ✓ Good |
| i*pi EML needs matched wins on its natural-bias family before positive claims | The v1.16 package found lower-loss diagnostics only, with 0 exact recoveries; full claims still need exact recovery and controls. | ✓ Good |
| Negative or inconclusive evidence is preferable to an overclaim | v1.16 produced a clean inconclusive package instead of relaxing the recovery definition. | ✓ Good |
| v1.17 works snap-first before spending campaign budget | v1.16 showed the blocker is not just training loss; exact recovery fails at the hard candidate boundary. | ✓ Good |
| Exact-neighborhood search must stay target-agnostic | Local repair is useful only if it avoids formula-name recognizers, exact target seeds, and verifier bypasses. | ✓ Good |
| Candidate ranking should be verifier-first | Post-snap loss and soft-loss metrics are diagnostics; exact recovery claims need symbolic/verifier status before fit quality. | ✓ Good |
| Broader i*pi/GEML campaigns remain blocked after v1.17 | The committed v1.17 package is `still_inconclusive`; no verifier-gated exact signal appeared. | ✓ Good |

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
*Last updated: 2026-04-22 after v1.17 milestone archive*
