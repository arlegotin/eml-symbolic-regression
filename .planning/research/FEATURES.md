# Feature Landscape: v1.11 Paper-Strength Evidence and Figure Package

**Domain:** Evidence package for a verifier-gated hybrid EML symbolic-regression paper  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-19  
**Overall confidence:** HIGH for evidence-package scope and claim boundaries; MEDIUM for external baseline feasibility because dependencies may be absent locally.

## Executive Take

v1.11 should make the paper stronger by packaging the evidence already earned, rerunning real training only where the claim class is honest, and adding cheap ablations that explain why the hybrid pipeline matters. It should not try to turn logistic or Planck into solved rows by moving gates, and it should not pivot into a broad symbolic-regression benchmark competition.

The table-stakes product is a v1.11 paper package rooted under `artifacts/paper/v1.11/` that refreshes the v1.9 raw-hybrid package, adds the v1.10 logistic and Planck motif diagnostics, regenerates claim-safe training artifacts, and emits plot-ready JSON/CSV/SVG files. The best differentiators are provenance-rich claim ledgers, motif/depth ablations, candidate lifecycle plots, and explicit negative results that make the method credible rather than oversold.

Existing evidence to preserve:

| Evidence | Current Signal | Interpretation |
|----------|----------------|----------------|
| v1.6 shallow pure-blind proof | 2/18 recovered in the explicit shallow pure-blind claim row | Honest measured boundary, not a failed milestone. |
| v1.6 shallow scaffolded proof | 18/18 recovered | Strong scaffolded recovery, not pure blind discovery. |
| v1.6 perturbed-basin proof | 9/9 recovered in the bounded proof claim; broader v1.9 package reports 23/23 perturbed-basin recovered | Strong same-basin return evidence. |
| v1.6 depth curve | Blind 100% at depths 2 and 3, 0% at depths 4, 5, and 6; perturbed 100% at depths 2 through 6 | Paper-aligned depth degradation evidence. |
| v1.9 raw-hybrid package | Regime-separated package with 20 source locks and 7 scientific-law rows | Right structure, stale for v1.10 logistic/Planck diagnostics. |
| v1.10 logistic diagnostic | Unsupported under strict gate; relaxed compile depth 15, baseline depth 27, `exponential_saturation_template`, validation passed | Useful motif-shortening evidence, not support. |
| v1.10 Planck diagnostic | Unsupported under strict gate; relaxed compile depth 14, prior paper row stale at 20, current macro baseline 24, low-degree power plus direct division motifs, validation passed | Useful near-gate diagnostic, not support. |

## Table Stakes

Features users, reviewers, and roadmap phases should expect. Missing these makes the paper package hard to trust.

| Feature | Why Expected | Complexity | Required Output | Notes |
|---------|--------------|------------|-----------------|-------|
| v1.11 paper package refresh | v1.9 package is structurally right but stale for v1.10 logistic and Planck. | Medium | `manifest.json`, `source-locks.json`, `regime-summary.json`, `scientific-law-table.json/.csv/.md`, `claim-boundaries.md`, `raw-hybrid-report.md` under `artifacts/paper/v1.11/`. | Keep it synthesis-first. It may consume new v1.11 training artifacts, but package generation itself should not silently run training. |
| v1.10 scientific-law row updates | The paper-facing table still lists logistic depth 27 and Planck depth 20 from older diagnostics. | Low | Updated rows for logistic and Planck with strict status `unsupported`, relaxed depth, node count, macro hits, depth deltas, validation status, and artifact path. | Logistic: 27 -> 15 relaxed depth. Planck: paper-row 20 -> 14 relaxed depth; also record current no-macro baseline 24 to avoid baseline ambiguity. |
| Source locks and reproduction commands | A paper package needs stable provenance for every number and plot. | Medium | Hash locks for each source artifact plus exact CLI commands, code version, Python/platform, output root, and generation timestamp. | Follow v1.9 source-lock style, but add v1.10 focused evidence and v1.11-generated suites. |
| Claim-safe training suite matrix | The milestone asks for real training where honest. | High | Separate suite outputs for pure-blind, scaffolded, warm-start/same-AST, perturbed-tree, repair/refit, and logistic/Planck probes. | Reuse existing benchmark/campaign contracts instead of ad hoc notebooks. |
| Shallow pure-blind rerun | Reviewers need fresh current-code evidence for blind performance rather than only archived v1.6. | Medium | Aggregate JSON/Markdown, run JSON, CSV, and plots with scaffold initializers disabled. | Report as measured boundary. Do not promise improvement. |
| Scaffolded shallow rerun | The paper needs the strongest positive training evidence with honest label. | Medium | Same output format as pure-blind, grouped separately. | Existing evidence is 18/18; v1.11 should preserve the claim class, not merge it into blind. |
| Perturbed-basin rerun | The main positive training story is basin return from known nearby trees. | Medium | Bounded proof suite plus probe rows, with perturbation noise, return kind, repaired candidates, and verifier status visible. | Count bounded proof and high-noise probes separately. |
| Depth degradation suite | The paper needs the negative/limitation curve as much as the wins. | Medium | Depth 2 through 6 blind-vs-perturbed source table and figure. | Keep depth targets deterministic and exact EML, as in v1.6. |
| Warm-start/same-AST scientific-law suite | Beer-Lambert, Shockley, Arrhenius, and Michaelis-Menten are key public examples. | Medium | Per-law run artifacts, scientific-law support table, and regime summary. | Same-AST return is valuable but must remain non-blind. |
| Logistic/Planck low-budget probes | They are high-visibility laws and v1.10 has new compiler diagnostics. | Low-Medium | Compile-only and, if cheap, low-budget training/probe artifacts labeled unsupported unless strict verifier contract passes. | Do not promote rows merely because relaxed depth is close to the gate. |
| Motif/depth ablation table | v1.10 improvements came from reusable compiler motifs; the paper needs evidence that these motifs matter. | Medium | `motif-depth-deltas.csv/.json/.md` with law, motif hits/misses, baseline depth/nodes, motif depth/nodes, deltas, validation max error, and strict-gate status. | Prefer compiler metadata already present in run JSON. Add true motif-disabled reruns only if cheap and deterministic. |
| Warm-start versus blind ablation | The central story is not "gradient descent solves everything"; it is regime-dependent hybrid recovery. | Medium | Side-by-side table/plot by formula and start mode: blind, scaffolded, warm-start, perturbed-tree. | Make denominator and eligibility rules explicit. |
| Candidate-pool/repair/refit diagnostics | v1.6-v1.9 added candidate pools, repair, and refit; the paper should show whether they help and when they do not. | Medium | Default vs expanded cleanup table, repair/refit status counts, no-regression checks, selected/fallback preservation evidence. | No-improvement evidence is still useful if it proves fallback preservation and taxonomy honesty. |
| Plot-ready source tables | Figures should be reproducible from checked-in machine-readable data. | Medium | Tables for regime recovery, depth curve, scientific-law support, motif deltas, training outcomes, failure taxonomy, runtime/budget, loss/snap metrics, and baseline diagnostics. | Do not make SVGs the only source of truth. |
| Publication-quality figures | The current campaign layer already emits deterministic SVGs; v1.11 needs paper-focused composition. | Medium | Figure package with deterministic SVG and source CSV/JSON for each figure. | Good first set: regime recovery bars, blind-vs-perturbed depth curve, scientific-law support heatmap, motif depth delta bars, loss before/after snap, failure taxonomy, runtime/depth budget scatter. |
| Claim-boundary checks | The package must prevent accidental overclaiming. | Medium | Machine-readable claim ledger plus Markdown boundaries and tests that assert forbidden merges do not appear. | Guard phrases: warm-start, same-AST, scaffolded, repaired, refit, compile-only, and perturbed-basin evidence is not blind discovery. |
| Non-destructive archived anchors | v1.4/v1.5/v1.6/v1.9 artifacts remain comparison anchors. | Low | New output roots only; no overwriting archived paper/proof/campaign packages except with explicit v1.11 roots. | Use v1.6 and v1.9 as locked sources, not mutable work directories. |
| Low-risk baseline diagnostics | The paper needs context, but broad competition is deferred. | Medium | Local diagnostics that are easy to run and clearly scoped: catalog verifier, compile-only depth gate, pure-blind random-start baseline, and simple prediction-only conventional fits if implemented locally. | External PySR/SRBench-style comparisons should be optional and non-blocking. |

## Claim-Safe Training Suites

These are the training-facing features v1.11 should expose or regenerate.

| Suite | Table-Stakes Cases | Claim Class | What To Plot | Promotion Rule |
|-------|--------------------|-------------|--------------|----------------|
| `v1.11-shallow-pure-blind` | `exp`, `log`, shallow scaled exponentials, Beer-Lambert/radioactive-decay shallow cases with scaffold initializers disabled | measured pure-blind recovery | Recovery by formula, failure taxonomy, post-snap loss, runtime | Promote only verifier-owned exact EML recovery. |
| `v1.11-shallow-scaffolded` | Same shallow formulas with declared scaffold initializers | scaffolded blind training | Scaffolded vs pure-blind recovery bars | Never count as pure blind. |
| `v1.11-perturbed-basin` | Depth 1-3 basin targets and Beer-Lambert bounded perturbation | perturbed true-tree recovery | Recovery vs perturbation noise, same-AST vs repaired split | Count only declared nonzero `perturbed_tree` rows under this claim. |
| `v1.11-depth-curve` | Deterministic depth 2-6 exact EML targets with blind and perturbed starts | measured depth degradation | Blind vs perturbed depth curve | Report degradation as limitation evidence. |
| `v1.11-scientific-warm` | Beer-Lambert, Shockley, Arrhenius, Michaelis-Menten | same-AST or verified-equivalent warm-start | Law support table and start-mode comparison | Same-AST return is recovery from seed/basin, not blind discovery. |
| `v1.11-logistic-planck-probes` | Logistic and Planck compile diagnostics, optionally very low-budget warm-start probes | unsupported/stretch diagnostics unless strict contract passes | Motif depth deltas and strict-gate near-miss chart | No promotion unless strict compile/warm-start and verifier gates pass without gate relaxation. |
| `v1.11-repair-refit-ablation` | Focused near misses from existing repair/refit examples plus any new v1.11 near misses | repair/refit diagnostics | Selected-only vs expanded pool, refit accepted/rejected, no-regression counts | Repair/refit is never blind discovery. |
| `v1.11-smoke` | One blind, one warm-start, one unsupported compile row | CI sanity only | Not paper figure unless needed for reproducibility section | Must remain quick and deterministic. |

## Plot and Table Artifacts

The figure package should be generated from explicit source tables. Recommended artifact names:

| Artifact | Purpose | Required Columns or Fields |
|----------|---------|----------------------------|
| `tables/regime-summary.csv` | Main regime recovery table | regime, runs, verifier_recovered, same_ast_return, repaired_candidate, unsupported, failed, recovery_rate, source_ids |
| `tables/training-runs.csv` | Plot source for all real training runs | run_id, formula, suite, start_mode, seed, depth, steps, perturbation_noise, claim_status, evidence_class, return_kind, raw_status, repair_status, best_loss, post_snap_loss, high_precision_max_error, artifact_path |
| `tables/depth-curve.csv` | Blind-vs-perturbed depth figure | depth, start_mode, seeds, recovered, recovery_rate |
| `tables/scientific-law-support.csv` | Paper-facing law table | law, formula, strict_support, relaxed_depth, strict_gate, macro_hits, warm_start_status, verifier_status, evidence_regime, artifact_path |
| `tables/motif-depth-deltas.csv` | Compiler motif ablation figure | law, source_expression, baseline_depth, motif_depth, depth_delta, baseline_nodes, motif_nodes, node_delta, macro_hits, validation_status, max_abs_error |
| `tables/repair-refit-ablation.csv` | Candidate-pool and refit diagnostic | formula, mode, selected_only_status, expanded_pool_status, repair_variant_count, repaired, refit_status, refit_accepted, final_regressed |
| `tables/baseline-diagnostics.csv` | Low-risk conventional/local baselines | baseline_name, formula, split, metric, value, status, notes |
| `figures/regime-recovery.svg` | Shows what succeeds by regime | Must visually separate blind, scaffolded, warm-start, same-AST, perturbed, repair/refit, unsupported. |
| `figures/depth-degradation.svg` | Core limitation figure | Blind and perturbed curves on same axes. |
| `figures/scientific-law-support.svg` | Law support matrix | Rows are laws; columns are compile support, depth gate, training regime, verifier status. |
| `figures/motif-depth-deltas.svg` | v1.10/v1.11 compiler contribution | Bars for logistic and Planck, plus existing supported laws where metadata exists. |
| `figures/loss-snap-verifier.svg` | Training pipeline behavior | Best soft loss vs post-snap loss vs verifier result; useful for showing why loss alone is not recovery. |
| `figures/failure-taxonomy.svg` | Honest failure modes | Unsupported depth, snapped-but-failed, soft-fit-only, execution error, repaired, refit rejected. |

## Low-Hanging Differentiators

These are not strictly required to produce a package, but they are high-value and low-risk for a stronger paper.

| Feature | Value Proposition | Complexity | Why It Is Low-Hanging |
|---------|-------------------|------------|-----------------------|
| Claim ledger with one row per paper claim | Lets the paper map every sentence to source artifacts and eligible denominators. | Medium | Claim IDs, thresholds, and source locks already exist in proof and paper artifacts. |
| Stale-diagnostic correction table | Shows v1.11 improved the package honestly: logistic and Planck got shorter, but not solved. | Low | v1.9 and v1.10 artifacts already contain the needed fields. |
| Motif contribution narrative | Makes compiler work look scientific instead of like hidden formula hacks. | Medium | Current compiler metadata records macro hits, misses, baseline depth/node count, deltas, and validation. |
| Near-gate unsupported figure | Planck depth 14 and logistic depth 15 are close to the strict depth 13 gate; plotting this is more honest than hiding them. | Low | The v1.10 focused artifacts already expose strict and relaxed diagnostics. |
| Candidate lifecycle diagram from real artifacts | Shows soft optimization -> snap -> candidate pool -> cleanup/repair/refit -> verifier. | Medium | Existing run JSON exposes best loss, post-snap loss, selected/fallback candidates, repair/refit status, and high-precision errors. |
| No-regression repair/refit checks | Even when repair does not improve recovery, proving it preserves fallback behavior strengthens the engineering story. | Low | v1.9 repair evidence already measured no improvements and no final-status regressions. |
| Prediction-only conventional baseline | Helps reviewers separate "fits the curve" from "recovers a verified formula." | Medium | Can be implemented locally with NumPy/SymPy feature libraries and train/held-out/extrapolation errors. Must be labeled prediction-only. |
| External baseline smoke if already installed | Provides a sanity comparison without turning v1.11 into a benchmark race. | Low-Medium | Only run if dependency is already available or trivial to install; otherwise record as deferred. |
| Paper figure inventory with readiness status | Makes roadmap creation straightforward and prevents late missing-figure surprises. | Low | v1.7/v1.8 already used figure inventory artifacts. |
| Artifact completeness verifier | A single command can assert expected files exist, hashes are recorded, claim boundaries are present, and every plot has source data. | Medium | Mostly file/schema validation over generated outputs. |

## Low-Risk Baseline Diagnostics

Use these as diagnostics, not headline superiority claims.

| Baseline | Include? | What It Answers | Guardrail |
|----------|----------|-----------------|-----------|
| Catalog verifier baseline | Yes | Are datasets, domains, and verifier checks sane for the target formulas? | This is not EML discovery. |
| Compile-only EML baseline | Yes | Is the formula representable within strict or relaxed compiler gates? | Compile success is not training recovery. |
| Pure-blind random-start EML baseline | Yes | What does the current optimizer recover without scaffold help? | Keep scaffold initializers disabled and report failures. |
| Scaffolded/warm-start EML baseline | Yes | How much does structural prior/witness proximity matter? | Never merge with pure-blind denominators. |
| Simple prediction-only conventional fit | Optional but recommended | Can a simple local model fit the data without recovering a symbolic EML formula? | Label as prediction-only and avoid broad SR claims. |
| External SR package smoke | Optional, non-blocking | Does an off-the-shelf symbolic-regression tool solve one or two easy demos locally? | Run only if dependency is available; do not make paper package depend on it. |
| Matched-budget SRBench/PySR competition | No for v1.11 | Broad external competitiveness. | Defer until the hybrid search engine is stronger and benchmark protocol is planned. |

## Anti-Features and Out of Scope

Features to explicitly avoid in v1.11.

| Anti-Feature | Why Avoid | What To Do Instead |
|--------------|-----------|-------------------|
| Promoting logistic or Planck by relaxing the strict gate | This would violate the current paper contract and make the near-miss evidence look dishonest. | Report them as unsupported diagnostics with relaxed depth, macro hits, and validation. |
| Formula-name recognizers or exact-constant hacks | v1.10 constraints require reusable structural motifs, not law-specific branches. | Use motif metadata, validation gates, and source-expression-independent rules. |
| Calling warm-start, same-AST, scaffolded, repaired, refit, compile-only, or perturbed-basin evidence "blind discovery" | This is the main credibility failure to avoid. | Keep regime labels visible in every table, plot, report, and claim ledger. |
| Hiding unsupported or failed rows from denominators | Unsupported rows are part of the evidence and explain limits. | Keep failed/unsupported rows in aggregate tables with reason codes. |
| Using training loss as recovery | The repo's recovery contract is verifier-owned; loss-only claims would regress the science. | Plot loss as diagnostic only, with verifier result beside it. |
| Replacing archived v1.6/v1.9 artifacts | Historical anchors need to remain inspectable and comparable. | Generate v1.11 roots and lock old artifacts as sources. |
| Broad matched-budget external benchmark competition | Too much scope for this milestone and easy to do badly. | Include low-risk diagnostics and defer serious external baselines. |
| Full blind recovery of arbitrary deep formulas | Both the paper and local depth curves show degradation. | Present depth degradation as a core boundary result. |
| Centered-family rescue work | v1.8 evidence is negative under missing same-family witnesses. | Keep centered-family material as negative diagnostic/background only. |
| Full SymPy compiler or new special-function support | The paper package needs evidence, not a broad compiler expansion. | Use existing supported subset and motif diagnostics. |
| Custom CUDA/Rust acceleration | Not needed for paper-package correctness and would distract from evidence. | Use current Python/PyTorch artifacts unless profiling shows a blocker. |
| Web dashboard | Static reproducible artifacts are enough and better for paper review. | Generate Markdown, JSON, CSV, and SVG. |
| Formal theorem-prover equivalence | Out of scope for the repo and milestone. | Use current symbolic cleanup plus high-precision verifier checks. |

## Feature Dependencies

```text
v1.11 paper package refresh
  -> source lock expansion
  -> v1.10 logistic/Planck source ingestion
  -> v1.11 training suite ingestion
  -> regime summary rebuild
  -> scientific-law table refresh
  -> claim-boundary checks
  -> plot/table source export
```

```text
claim-safe training evidence
  -> benchmark suites with explicit start_mode
  -> deterministic dataset manifests
  -> run JSON artifacts
  -> aggregate JSON/Markdown
  -> verifier-owned recovery counts
  -> regime-separated paper package ingestion
```

```text
motif ablations
  -> compiler diagnostics with baseline depth/nodes
  -> macro hit/miss metadata
  -> validation status and max error
  -> strict gate status
  -> motif-depth-delta tables and figures
```

```text
baseline diagnostics
  -> local baseline runner or existing verifier/compile artifacts
  -> prediction-only status labels
  -> train/held-out/extrapolation metrics
  -> no merge into EML recovery denominators
```

## MVP Recommendation

Prioritize:

1. Refresh the raw-hybrid paper package into a v1.11 output root, with v1.10 logistic and Planck diagnostics included.
2. Regenerate claim-safe training suites for shallow pure-blind, scaffolded, perturbed-basin, and depth-curve evidence under current code.
3. Add paper-focused source tables and SVG figures for regime recovery, depth degradation, scientific-law support, motif depth deltas, failure taxonomy, and loss/snap/verifier behavior.
4. Add low-hanging ablation tables for motifs, warm-start versus blind, and candidate-pool/repair/refit behavior.
5. Include low-risk baseline diagnostics only where they are local, deterministic, and explicitly scoped as diagnostics.

Defer:

- Matched-budget external SR benchmarking.
- Any attempt to support logistic/Planck by changing gates or adding formula-specific recognition.
- New operator-family research.
- Major optimizer redesign.
- UI, acceleration, or formal proof work.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Paper package refresh requirements | HIGH | v1.9 package contract is implemented and v1.10 artifacts clearly identify stale rows to refresh. |
| Training suite split | HIGH | v1.6 proof report, v1.9 claim boundaries, README, and benchmark contracts all enforce regime separation. |
| Plot/table needs | HIGH | Existing campaign artifacts already emit CSVs and SVGs; v1.11 needs paper-specific composition. |
| Motif ablations | HIGH | v1.10 logistic and Planck run JSON contains baseline depth/node counts, motif depth/node counts, macro hits, and validation. |
| Repair/refit diagnostics | HIGH | Existing artifacts expose repair/refit status and v1.9 repair no-improvement evidence. |
| Low-risk local baselines | MEDIUM | Catalog, compile-only, and pure-blind baselines are available; prediction-only conventional baselines may need a small runner. |
| External baseline smoke | LOW-MEDIUM | Feasibility depends on installed dependencies/network access and should not block v1.11. |

## Sources

- `.planning/PROJECT.md` - v1.11 milestone goals, target features, constraints, out-of-scope items, and paper-claim decisions.
- `.planning/STATE.md` - current v1.11 position and baseline-diagnostic concern.
- `artifacts/paper/v1.9/raw-hybrid/raw-hybrid-report.md` - current regime-separated paper package.
- `artifacts/paper/v1.9/raw-hybrid/scientific-law-table.md` - stale paper-facing scientific-law rows.
- `artifacts/paper/v1.9/raw-hybrid/claim-boundaries.md` - explicit non-blind claim boundaries.
- `artifacts/proof/v1.6/proof-report.md` - proof bundle, shallow pure-blind/scaffolded claims, perturbed-basin proof, depth curve, and archived anchors.
- `artifacts/campaigns/v1.10-logistic-evidence/aggregate.md` and `v1-10-logistic-evidence-logistic-compile-c2af27a35e81.json` - logistic unsupported diagnostic with relaxed depth 15 and validated exponential-saturation motif.
- `artifacts/campaigns/v1.10-planck-diagnostics/aggregate.md` and `v1-10-planck-diagnostics-planck-compile-795067919a97.json` - Planck unsupported diagnostic with relaxed depth 14 and validated low-degree power/direct-division motifs.
- `README.md` and `docs/IMPLEMENTATION.md` - current CLI, benchmark, campaign, raw-hybrid package, repair/refit, and artifact contracts.
- `src/eml_symbolic_regression/raw_hybrid_paper.py`, `benchmark.py`, `campaign.py`, and `proof_campaign.py` - implemented package/suite/report structure used to scope v1.11 features.
