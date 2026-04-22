# Milestones

## v1.15 GEML family and i*pi EML exploration (Shipped: 2026-04-22)

**Phases completed:** 6 phases, 6 plans, 0 tasks

**Key accomplishments:**

- Added fixed-parameter `GEML_a` semantics with raw EML as `a = 1` and i*pi EML as `a = i*pi`.
- Created restricted-domain i*pi theory artifacts with explicit branch conventions, branch diagnostics, and non-claims.
- Threaded fixed GEML operator families through training, hardening, snapping, exact-candidate selection, verifier metrics, and manifests.
- Registered matched oscillatory, log-periodic, and negative-control benchmark suites for raw EML versus i*pi EML.
- Added paired campaign outputs with recovery, loss, gradient, anomaly, branch, runtime, and v1.14 recovery-accounting fields.
- Generated `artifacts/paper/v1.15-geml/` with source locks, benchmark manifests, target-family classification, reproduction commands, and a passing claim audit.

**Known deferred items at close:** The full 20-row `geml-oscillatory` campaign remains a reproduction command. The checked-in package is intentionally `inconclusive_smoke_only`: two smoke pairs, no verifier-gated exact recovery, one periodic i*pi loss-only signal, and one negative-control raw loss-only signal.

---

## v1.14 Evidence claim integrity and audit hardening (Shipped: 2026-04-21)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added two-axis recovery accounting so compile-only verified support cannot increment trained exact-recovery headlines.
- Regenerated public evidence surfaces with corrected package-level numbers: 8 trained exact recoveries, 1 compile-only verified support row, 15 unsupported rows, and 0 failed rows.
- Relabeled zero-perturbation same-AST warm-start positives as exact seed round-trips unless real perturbation evidence exists.
- Quarantined unavailable, unsupported, and denominator-excluded baseline rows from main comparison claims.
- Fixed multivariate high-precision verifier target matching by using full input-row keys when no `target_mpmath` evaluator is present.
- Regenerated `artifacts/paper/v1.14/` with source locks, passing claim audit, and release-gate checks.

**Known deferred items at close:** Real perturbation-grid robustness evidence and fixed-budget external baseline runs remain future work; v1.15 starts from the archived v1.14 planning artifacts.

---

## v1.13 Publication-grade reproduction and validation (Shipped: 2026-04-20)

**Phases completed:** 8 phases, 8 plans, 0 tasks

**Key accomplishments:**

- Added a clean-room publication rebuild path with lockfile/container provenance, source locks, and manifest validation.
- Upgraded verifier and split discipline with symbolic, dense randomized, adversarial, certificate, evidence-level, and final-confirmation labels.
- Added guarded versus faithful training semantics controls and published diagnostics for guard/anomaly/post-snap mismatch evidence.
- Hardened CI with algorithmic tests, evidence-regression coverage, and dev/public-snapshot branch-discipline validation.
- Added separated basis-only and literal-constant benchmark tracks, expanded dataset manifests, and a matched baseline harness.
- Regenerated the v1.13 release evidence package with a passing claim audit and release gate.

**Known deferred items at close:** 7 old quick-task bookkeeping records had missing or unknown open-artifact metadata; no debug sessions, todos, UAT gaps, verification gaps, or context questions were open. See `STATE.md` Deferred Items.

---

## v1.12 Paper draft skeleton and refreshed shallow evidence (Shipped: 2026-04-19)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added `artifacts/paper/v1.11/draft/` with abstract, methods, results, limitations, claim taxonomy, and paper-facing captions.
- Ran a current-code evidence refresh: 10/10 shallow verifier-recovered rows across separate pure-blind/scaffolded regimes, plus a depth 2-5 refresh with 4/8 recovered.
- Added motif-library evolution, logistic/Planck negative-results, and EML pipeline figure artifacts for the paper draft.
- Recorded bounded probes: conventional symbolic-regression baseline unavailable locally, and logistic strict support still unsupported at strict gate 13 with relaxed depth 15.
- Assembled `artifacts/paper/v1.11/v1.12-supplement/` with 49 source locks, reproduction commands, and a passing claim audit.

**Known deferred items at close:** conventional external SR baseline remains future BASE-02 work; logistic strict-support improvement remains future compiler work.

---

## v1.11 Paper-strength evidence and figure package (Shipped: 2026-04-19)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added a versioned v1.11 raw-hybrid paper package that uses current v1.10 logistic and Planck diagnostics instead of stale scientific-law rows.
- Ran real current-code paper training and probe campaigns: 8/8 verifier-recovered training rows across separated regimes, plus 0/4 recovered logistic/Planck probes with 2 unsupported and 2 failed rows kept visible.
- Generated motif-depth, regime-comparison, repair/refit, and prediction-only baseline diagnostics under `artifacts/diagnostics/v1.11-paper-ablations/`.
- Generated deterministic paper assets under `artifacts/paper/v1.11/assets/`: 7 SVG figures, 7 source tables, and per-figure metadata.
- Assembled the final `artifacts/paper/v1.11/` package with root manifest, 67 source-lock rows, reproduction commands, paper-readiness summary, and a passing 7-check claim audit.

---

## v1.10 Search-backed motif library and compiler shortening for logistic and Planck (Shipped: 2026-04-18)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Locked archived compiler baselines for logistic, Planck, Michaelis-Menten, Arrhenius, and Shockley before changing motif behavior.
- Generalized reciprocal and saturation motifs to validated compilable subexpressions with validation-visible macro diagnostics and fail-closed rejection.
- Added a structural exponential-saturation motif that lowers logistic relaxed compile depth from 27 to 15 while keeping strict unsupported status honest.
- Added bounded motif-search evidence plus validation-backed low-degree power compression, dropping Planck relaxed compile depth from 20 to 14 while preserving unsupported/stretch classification.
- Added focused v1.10 benchmark suites and campaign artifacts for logistic and Planck diagnostics under `artifacts/campaigns/`, with no warm-start promotion claimed.

---

## v1.9 milestone (Shipped: 2026-04-17)

**Phases completed:** 5 phases, 14 plans, 33 tasks

**Key accomplishments:**

- Raw-only scaffold witness registry with benchmark budget filtering that removes raw exp/log/scaled_exp scaffolds from centered-family variants.
- Registry-backed optimizer and helper guards that block raw exp/log/scaled_exp scaffolds under centered operators while preserving raw scaffold recovery artifacts.
- Normalized Arrhenius demo `exp(-0.8/x)` with strict direct-division compile and verified same-AST warm-start evidence
- Focused Arrhenius benchmark suite with same-AST warm-start artifact evidence for normalized `exp(-0.8/x)`
- Focused Arrhenius same-AST warm-start artifacts with README and implementation docs tied to validated JSON evidence
- Structural reciprocal-shift and saturation-ratio EML compiler macros with Michaelis-Menten same-AST warm-start recovery
- Focused Michaelis-Menten same-AST warm-start benchmark evidence with saturation macro artifact locks
- Validated Michaelis-Menten same-AST warm-start artifacts with regime-safe README and implementation documentation
- Opt-in candidate-pool repair over selected, fallback, and retained exact roots with verifier-gated AST-deduped promotion
- Benchmark opt-in for expanded verifier-gated cleanup with focused before/after repair evidence
- Focused v1.9 repair evidence measured expanded cleanup against selected-only cleanup while preserving fallback manifests
- Synthesis-only raw-hybrid paper package writer with file-level source locks, regime-separated reports, scientific-law tables, centered caveats, and a CLI entry point
- Committed v1.9 raw-hybrid paper package with source locks, regime-separated evidence, scientific-law tables, and claim boundaries
- Artifact-backed raw-hybrid package regression tests plus README and implementation documentation that preserve evidence boundaries

---

## v1.8 Centered-Family Viability and Full Evidence Run (Shipped: 2026-04-17)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Reproduced and classified expanded raw-vs-centered family smoke and calibration evidence with scoped go/no-go diagnostics.
- Made centered warm-start, perturbed-tree, compiler-seed, initializer, and scaffold unsupported paths explicit instead of hidden raw-family reuse.
- Expanded fixed-scale and continuation family suites, then scoped the full evidence run based on centered calibration failure.
- Archived v1.8 family evidence manifests, campaign aggregates, comparison tables, and regression locks without overwriting earlier proof anchors.
- Generated `artifacts/paper/v1.8/` and selected the raw-EML searchability note path after raw EML outperformed centered variants in supplied aggregates.

---

## v1.7 Centered-Family Baseline and Paper Decision (Shipped: 2026-04-16)

**Phases completed:** 5 phases, 5 plans, 20 requirements

**Key accomplishments:**

- Added centered/scaled operator-family semantics and exact AST support for `cEML_{s,t}`, `CEML_s`, and `ZEML_s` with `expm1`/`log1p` and shifted-singularity diagnostics.
- Threaded fixed-family and scheduled-continuation operators through the soft master tree, optimizer manifests, snapping, repair/refit, benchmark budgets, and campaign CSV rows.
- Added v1.7 raw-vs-centered family benchmark suites and campaign presets for smoke, shallow, basin, depth-curve, standard, and showcase-style matrices.
- Added operator-family recovery tables, diagnostic tables, comparison Markdown, and regression-lock JSON outputs for campaign reports.
- Generated `artifacts/paper/v1.7/` with the decision memo, safe/unsafe claim language, figure/table inventory, and an explicit incomplete completeness boundary.
- Audit decision: wait for centered-family campaign evidence before submitting the centered empirical paper; raw-EML searchability/geometry remains a viable note from archived proof evidence.

---

## v1.6 Hybrid Search Pipeline and Exact Candidate Recovery (Shipped: 2026-04-16)

**Phases completed:** 5 phases, 5 plans, 15 tasks

**Key accomplishments:**

- Late-hardening candidate pooling with verifier-ranked exact selection and legacy fallback provenance across blind, warm-start, basin, and CLI flows
- Bounded target-free cleanup over low-margin exact candidates with fallback-preserving benchmark artifacts
- Frozen exact-expression constant refit, fallback-preserving artifact wiring, and richer exp/log anomaly diagnostics
- Macro-aware compiler shortcuts, audited diagnostics, and conservative warm-start coverage expansion
- Regime-aware reporting, immutable comparison anchors, and aggregate-level hybrid regression locks
- Final `artifacts/proof/v1.6` evidence bundle regenerated from the latest code state and verified against campaign aggregates, with pure-blind, scaffolded, perturbed-basin, and depth-curve claims kept separate

---

## v1.5 Training Proof and Recovery Guarantees (Shipped: 2026-04-16)

**Phases completed:** 5 phases, 11 plans, 0 tasks

**Key accomplishments:**

- Converted the paper-grounded claim set into executable proof suites, deterministic dataset manifests, explicit threshold policies, and proof-aware benchmark artifacts.
- Split shallow training evidence into measured pure-blind recovery and bounded scaffolded recovery, preserving honest proof semantics for both.
- Added first-class perturbed true-tree basin recovery, verifier-gated local repair, and durable Beer-Lambert bound diagnostics.
- Added a deterministic exact depth-curve inventory and measured blind-versus-perturbed reporting across depths 2 through 6.
- Shipped the one-command proof bundle in `artifacts/proof/v1.5/` with claim status, depth-curve evidence, carried-forward basin-bound diagnostics, and v1.4 context that keeps denominators separate.

---

## v1.4 Recovery Performance Improvements (Shipped: 2026-04-15)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added v1.3 baseline triage, representative failure rows, immutable baseline locks, and focused diagnostic reruns.
- Improved shallow blind recovery with conservative `exp` and `log` scaffold initializers while preserving verifier-owned recovery semantics.
- Added warm-start perturbation diagnosis fields and campaign metrics that identify active-slot perturbation as the dominant Beer-Lambert high-noise failure mechanism.
- Added compiler diagnostics and a validated Shockley `c*exp(a)-c` template, moving Shockley into verified compiled coverage.
- Generated v1.4 standard/showcase campaign evidence and a before/after comparison report showing overall recovery improved from 18/45 to 27/45 against v1.3 baselines.

---

## v1.3 Benchmark Campaign and Evidence Report (Shipped: 2026-04-15)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added `smoke`, `standard`, and `showcase` campaign presets with guarded output folders and reproducibility manifests.
- Added tidy CSV exports for run-level metrics, grouped recovery summaries, headline metrics, and failed/unsupported reason tables.
- Generated deterministic SVG figures for recovery rates, losses, Beer-Lambert perturbations, runtime/budget, and failure taxonomy.
- Assembled campaign-root `report.md` files with headline metrics, figure/table links, raw artifact links, exact commands, limitations, and next experiments.
- Committed the v1.3 smoke campaign evidence bundle in `artifacts/campaigns/v1.3-smoke/` and verified the workflow with 45 passing tests.

---

## v1.2 Training Benchmark and Recovery Evidence (Shipped: 2026-04-15)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added deterministic benchmark suite contracts, built-in suite registry, fail-closed validation, stable run IDs, and deterministic artifact paths.
- Added benchmark CLI execution for catalog verification, compile diagnostics, blind optimizer training, and compiler warm-start training.
- Expanded formula coverage with `radioactive_decay`, shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten warm diagnostics, Planck stretch diagnostics, and selected FOR_DEMO formulas.
- Added normalized per-run metrics plus aggregate JSON/Markdown evidence reports with recovery rates, grouping, taxonomy, and code/environment provenance.
- Added CI-scale benchmark smoke coverage and generated smoke evidence artifacts in `artifacts/benchmarks/smoke/`.
- Updated documentation to explain benchmark commands, report artifacts, same-AST warm-start return, verifier-owned recovery rates, and unsupported/failure interpretation.

---

## v1.1 EML Compiler and Warm Starts (Shipped: 2026-04-15)

**Phases completed:** 6 phases, 6 plans, 0 tasks

**Key accomplishments:**

- Added a fail-closed SymPy-to-EML compiler with structured metadata, rule traces, unsupported reason codes, and independent validation.
- Extended soft master trees with finite literal constant catalogs and exact AST embedding with snap-back verification.
- Added deterministic compiler warm-start training through the existing optimizer while keeping `recovered` verifier-owned.
- Promoted Beer-Lambert to verified trained exact EML recovery through the compiler warm-start path.
- Added honest Michaelis-Menten default-depth diagnostics and explicit normalized Planck stretch reporting.
- Expanded regression coverage to 24 tests and documented literal constants, warm-start provenance, and non-blind scope.

---
