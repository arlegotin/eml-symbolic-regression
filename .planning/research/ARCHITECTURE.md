# Architecture Patterns: v1.11 Paper-Strength Evidence and Figure Package

**Domain:** Verifier-gated EML symbolic-regression evidence pipeline  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-19  
**Overall confidence:** HIGH for integration points and data flow; MEDIUM for exact external-baseline scope because baseline dependencies are intentionally not established.

## Executive Summary

v1.11 should extend the existing benchmark -> aggregate -> campaign -> paper-package pipeline. The repo already has the right trust boundary: `benchmark.py` owns run execution and verifier-owned evidence classification, `campaign.py` owns tables/reports/quick SVGs, and `raw_hybrid_paper.py` owns synthesis-only package generation from locked source artifacts. Do not create a parallel evidence system for the paper package.

The main architectural change is versioning the paper package layer and adding a dedicated paper-asset derivation layer. v1.9's `raw_hybrid_paper.py` is hard-coded to v1.9 paths and stale v1.6 Planck/logistic diagnostic runs; v1.11 needs source specs that include the v1.10 focused logistic and Planck artifacts plus the new v1.11 real-training, ablation, and baseline outputs. The package writer should still not run training or campaigns.

The safest data contract is: run artifacts are the source of truth, aggregate JSON is the portable summary, campaign CSVs are derived inspection tables, paper assets are deterministic derivations from locked aggregate/run files, and the final package locks every evidence input file it depends on. Figures should never recompute claim status or infer recovery from loss; they should visualize fields already classified by `benchmark.aggregate_evidence()`.

Baseline diagnostics should stay separate from EML benchmark denominators. Add scoped local/conventional baseline artifacts as their own schema and source-lock them into the package, but do not add a baseline `start_mode` to `BenchmarkRun` unless it can satisfy the same dataset/provenance/verification contract without confusing EML recovery rates.

## Recommended Architecture

```text
BenchmarkSuite / CampaignPreset
  -> BenchmarkRun artifacts: eml.benchmark_run.v1
  -> suite-result.json
  -> aggregate.json / aggregate.md: eml.benchmark_aggregate.v1
  -> campaign tables + quick campaign figures
  -> paper asset derivation: tables/*.csv + figures/*.svg + asset-manifest.json
  -> v1.11 paper package: source-locks.json + regime/scientific-law reports + figures/tables
```

The paper package is a terminal synthesis step. It may generate deterministic tables and SVGs from loaded source artifacts, but it must not call `run_benchmark_suite()`, `run_campaign()`, `fit_eml_tree()`, external baselines, or proof-campaign execution.

## Component Boundaries

| Component | v1.11 Action | Responsibility | Important Boundary |
|-----------|--------------|----------------|--------------------|
| `benchmark.py` | Modify | Add v1.11 suite IDs for claim-safe training, logistic/Planck probes, and ablation cases; keep run execution and evidence classification here. | It may classify evidence; it must not write paper narrative. |
| `campaign.py` | Modify | Add v1.11 campaign presets and any general CSV exports needed by paper assets. Keep campaign-local reports and quick SVGs. | It should not know final paper-package source inventory. |
| `raw_hybrid_paper.py` | Modify | Make the package writer version-aware and add a v1.11 preset/source inventory. Preserve v1.9 compatibility. | Synthesis-only; no training, no campaign execution. |
| `cli.py` | Modify | Expose v1.11 suite/preset/package commands and possibly `paper-assets` / `baseline-diagnostics`. | CLI commands should route to modules, not implement evidence logic inline. |
| `compiler.py` | Small modify | Expose compiler macro toggles through benchmark config for motif ablations. `CompilerConfig.enable_macros` already exists. | Do not add formula-name recognizers or silent gate relaxation. |
| `datasets.py` | Usually unchanged | Existing demo specs should remain the dataset/provenance source. Add only if v1.11 needs explicit baseline sampling metadata. | Do not fork scientific-law definitions for paper-only code. |
| `paper_assets.py` | New | Pure derivation of paper tables and publication SVGs from aggregates, run artifacts, scientific-law rows, and baseline summaries. | Reads locked inputs; never runs training. |
| `baseline_diagnostics.py` | New, scoped | Local/conventional baseline diagnostics with separate schema and explicit limitations. | Baselines are comparison diagnostics, not EML recovery evidence. |
| `tests/test_paper_assets.py` | New | Fixture-driven table/SVG determinism tests. | Use tiny fixture aggregates, not expensive real campaigns. |
| `tests/test_baseline_diagnostics.py` | New if baseline module ships | Schema, failure-mode, and limitation wording tests. | External tools must fail soft or be marked unavailable. |

## Existing Contracts to Preserve

| Contract | Current Owner | v1.11 Rule |
|----------|---------------|------------|
| Verifier-owned recovery | `verify.py`, called by `benchmark.py` | Figures and paper tables must consume `claim_status`, `classification`, and `evidence_class`, not infer from loss. |
| Regime separation | `benchmark.evidence_class_for_payload()`, `raw_hybrid_paper.build_regime_summary()` | Pure blind, scaffolded, warm-start, same-AST, repair, refit, compile-only, and perturbed-basin stay separate. |
| Fail-closed compiler support | `compiler.py`, `_compile_demo()` | Logistic/Planck remain unsupported unless strict gates pass; relaxed depth diagnostics can be reported but not promoted. |
| Stable artifact paths | `BenchmarkRun.run_id`, `BenchmarkSuite.expanded_runs()` | New suite IDs and case IDs should be deterministic and explicit. |
| Non-destructive artifact output | `campaign.py`, `raw_hybrid_paper.py` | Stable labels must refuse overwrite unless explicitly requested; package overwrite must remain managed-file only. |
| File-level source locks | `raw_hybrid_paper.py` | v1.11 should continue hashing files, not directories. |

## Modified Modules

### `benchmark.py`

Add v1.11 suites as first-class built-ins rather than external JSON fixtures for the main milestone outputs:

| Suite | Purpose | Notes |
|-------|---------|-------|
| `v1.11-paper-training` | Claim-safe real training runs across shallow pure-blind, scaffolded blind, warm-start/same-AST, and perturbed-basin regimes. | Reuse existing start modes and proof-style claim metadata where possible. |
| `v1.11-logistic-planck-probes` | Low-budget focused training/compile probes for logistic and Planck. | Unsupported rows stay in denominator with clear `depth_exceeded` or training failure reasons. |
| `v1.11-ablation-motifs` | Compiler macro on/off depth and support comparisons. | Add `enable_macros` to `OptimizerBudget` or a nested compiler config; default remains `True`. |
| `v1.11-ablation-repair-refit` | Candidate-pool, cleanup, and refit behavior. | Reuse existing `BenchmarkRepairConfig` and refit metrics. |
| `v1.11-paper-smoke` | CI-scale fixture for CLI/package tests. | Should finish quickly and avoid expensive real-training budgets. |

Recommended schema additions:

- Add `OptimizerBudget.enable_macros: bool = True` and pass it into `CompilerConfig(enable_macros=...)`.
- Add runtime directly into aggregate run summaries, e.g. `timing_elapsed_seconds`, because current campaign figure/table helpers sometimes reread raw run files through `artifact_path`. A paper package should either lock those raw run files or use a self-contained aggregate. Prefer self-contained aggregates and keep file rereads as backward-compatible fallback.
- Add aggregate groups for `claim_id`, `threshold_policy_id`, and possibly `tags` if paper assets need them. Avoid changing the meaning of existing counts.

### `campaign.py`

Add campaign presets only for workflows that should produce reportable folders:

| Preset | Suite | Output Label |
|--------|-------|--------------|
| `paper-training` | `v1.11-paper-training` | `artifacts/campaigns/v1.11-paper-training/` |
| `paper-ablations` | `v1.11-ablation-motifs` plus repair/refit suite if kept separate | `artifacts/campaigns/v1.11-paper-ablations/` |
| `paper-probes` | `v1.11-logistic-planck-probes` | `artifacts/campaigns/v1.11-logistic-planck-probes/` |
| `paper-smoke` | `v1.11-paper-smoke` | test-only or manually generated smoke label |

Keep existing campaign plots for quick review, but do not rely on them as final paper figures. They are useful run diagnostics, while v1.11 needs paper-specific figure composition and an asset manifest.

### `raw_hybrid_paper.py`

Refactor toward versioned presets instead of a single v1.9 constant set:

```text
PaperPackagePreset(
  preset_id,
  output_dir,
  expected_outputs,
  sources,
  title,
)
```

Keep `write_raw_hybrid_paper_package()` backward-compatible for v1.9 tests. Add a v1.11 writer or a `preset=` parameter:

```text
write_raw_hybrid_paper_package(preset="v1.11", output_dir=artifacts/paper/v1.11/raw-hybrid)
```

v1.11 source inventory should include:

- v1.6 proof aggregates that still define historical shallow/depth/perturbed boundaries.
- v1.8 centered-family decision files for negative diagnostics and same-family witness caveat.
- v1.9 Arrhenius, Michaelis, and repair evidence.
- v1.10 logistic and Planck focused aggregate and run artifacts, replacing stale v1.6 logistic/Planck rows in the scientific-law table.
- v1.11 real-training campaign aggregate, suite result, and raw run artifacts used by figures.
- v1.11 ablation aggregate/table outputs.
- v1.11 scoped baseline diagnostics, if generated.

New package outputs should add:

| Output | Purpose |
|--------|---------|
| `figures/*.svg` | Publication-ready deterministic SVG figures. |
| `tables/regime-recovery.csv` | Regime recovery source table for figures. |
| `tables/scientific-law-support.csv` | Paper-facing law support rows, including v1.10 logistic/Planck depths. |
| `tables/motif-depth-deltas.csv` | Macro/motif depth and node deltas. |
| `tables/training-outcomes.csv` | Real-training outcome table by formula/regime/depth. |
| `tables/failure-taxonomy.csv` | Unsupported/failure reason counts. |
| `asset-manifest.json` | Derived asset inventory with source IDs for every table and figure. |

### `paper_assets.py` New

This should be a pure reader/renderer:

```text
load evidence inputs
  -> normalize rows by regime/evidence class/formula
  -> write CSV source tables
  -> write SVG figures from those CSV rows
  -> write asset-manifest.json
```

Recommended public API:

```python
write_paper_assets(
    sources: Mapping[str, Any],
    output_dir: Path,
    package_preset_id: str,
) -> PaperAssetPaths
```

Recommended figures:

| Figure | Input Table | Message |
|--------|-------------|---------|
| `regime-recovery.svg` | `regime-recovery.csv` | Recovery differs sharply by regime; do not merge denominators. |
| `depth-degradation.svg` | depth rows from aggregate | Blind depth degradation versus perturbed return. |
| `scientific-law-support.svg` | `scientific-law-support.csv` | Supported same-AST laws versus unsupported/stretch diagnostics. |
| `motif-depth-deltas.svg` | `motif-depth-deltas.csv` | v1.10 motif work reduced logistic/Planck relaxed depth without promotion. |
| `training-outcomes.svg` | `training-outcomes.csv` | Real training status by start mode and formula. |
| `failure-taxonomy.svg` | `failure-taxonomy.csv` | Unsupported/depth/training/recovery failures by reason. |

Use deterministic hand-written SVG like `campaign.py` does. Avoid matplotlib as a new runtime dependency unless the repo later chooses a plotting dependency explicitly.

### `baseline_diagnostics.py` New

Use a small, explicit schema:

```text
eml.baseline_diagnostics.v1
  dataset_manifest
  baseline_name
  baseline_type: local_conventional | external_unavailable | external_result
  fit_status
  train_error
  heldout_error
  extrapolation_error
  expression_or_model_summary
  limitations
```

Recommended first scope:

- Local conventional diagnostics that can run with existing dependencies.
- Optional external adapters only when installed; otherwise write an `external_unavailable` row with the attempted command/import and reason.
- No matched-budget competition claim in v1.11 unless the implementation really controls budget and search space.

Do not fold baseline rows into `benchmark.aggregate_evidence()` recovery rates. The paper package can include a separate baseline table/figure with explicit diagnostic wording.

## Artifact Flow

| Stage | Command Shape | Primary Outputs | Consumed By |
|-------|---------------|-----------------|-------------|
| Focused benchmark | `python -m eml_symbolic_regression.cli benchmark v1.11-... --output-dir artifacts/campaigns/...` | run JSONs, `suite-result.json`, `aggregate.json`, `aggregate.md` | Campaigns, paper package, tests |
| Campaign | `python -m eml_symbolic_regression.cli campaign paper-training --label v1.11-paper-training` | `campaign-manifest.json`, `tables/*.csv`, `figures/*.svg`, `report.md` | Human review, package source locks |
| Baseline diagnostics | `python -m eml_symbolic_regression.cli baseline-diagnostics ...` | `baseline-diagnostics.json`, `.csv`, `.md` | Paper package |
| Paper assets | called by package writer or `paper-assets` CLI | `tables/*.csv`, `figures/*.svg`, `asset-manifest.json` | Final package |
| Paper package | `python -m eml_symbolic_regression.cli raw-hybrid-paper --preset v1.11 --output-dir artifacts/paper/v1.11/raw-hybrid --require-existing` | `manifest.json`, `source-locks.json`, reports, tables, figures | Regression tests, paper writing |

Recommended final roots:

```text
artifacts/campaigns/v1.11-paper-training/
artifacts/campaigns/v1.11-paper-ablations/
artifacts/campaigns/v1.11-logistic-planck-probes/
artifacts/baselines/v1.11-scoped/
artifacts/paper/v1.11/raw-hybrid/
```

## Data Flow Details

### Run to Aggregate

`BenchmarkSuite.expanded_runs()` should remain the only mechanism that assigns run IDs and artifact paths. `execute_benchmark_run()` writes one `eml.benchmark_run.v1` JSON per run and assigns `evidence_class` by calling `evidence_class_for_payload()`. `aggregate_evidence()` converts those artifacts into a compact run list with counts, groups, depth-curve rows, and threshold summaries.

For v1.11, add only backward-compatible fields to aggregate run summaries. Paper assets should be able to derive figures from aggregate JSON plus explicitly locked run artifacts; they should not need hidden filesystem state.

### Aggregate to Tables

Campaign tables are useful, but paper tables need more stable semantics. Implement paper tables in `paper_assets.py` from aggregate/source payloads:

- `regime-recovery.csv`: one row per evidence regime with total, verifier recovered, same-AST, repaired, unsupported, failed, recovery rate, source IDs.
- `scientific-law-support.csv`: one row per law with formula, compile support, strict depth, relaxed depth if unsupported, macro hits, warm-start status, verifier status, evidence regime, artifact path.
- `motif-depth-deltas.csv`: one row per compiler diagnostic with baseline depth/node count, relaxed depth/node count, macro hits, depth delta, node delta, validation status.
- `training-outcomes.csv`: one row per formula/start mode/training mode/depth/seed group.
- `failure-taxonomy.csv`: one row per reason/classification/evidence class.

### Tables to Figures

Figures should read the paper CSV rows they cite, not raw JSON directly. This makes every figure auditable by opening the adjacent source table. Each SVG should include a title, axis labels, and short caption metadata in `asset-manifest.json`.

### Figures to Package

The final package manifest should list all derived tables and figures. `source-locks.json` should hash the input evidence artifacts; `asset-manifest.json` should map each output table/figure to the source IDs used to derive it. Do not hash generated outputs as if they were independent evidence inputs.

## Suggested Phase Order

1. **Phase 59: v1.11 Evidence Contract and Package Preset**
   - Add versioned paper-package preset support.
   - Add v1.10 logistic/Planck sources to the v1.11 scientific-law inventory.
   - Add fixture tests that generate a v1.11 package with small/local sources.
   - Rationale: fixes stale package architecture before expensive runs.

2. **Phase 60: Claim-Safe Real Training Suites**
   - Add `v1.11-paper-training` and `v1.11-logistic-planck-probes`.
   - Run and commit/report real artifacts under stable labels.
   - Rationale: evidence generation should use existing benchmark contracts and classification.

3. **Phase 61: Ablation and Baseline Diagnostics**
   - Add macro-on/off, warm-start/blind, repair/refit, and candidate-pool ablation outputs.
   - Add scoped baseline diagnostics with separate schema and honest unavailable/deferred rows.
   - Rationale: strengthens paper evidence without polluting EML recovery denominators.

4. **Phase 62: Paper Tables and Figures**
   - Add `paper_assets.py`.
   - Generate deterministic source CSVs and SVG figures from locked artifacts.
   - Rationale: figures should be a pure derivation layer after evidence exists.

5. **Phase 63: Final v1.11 Paper Package and Regression Locks**
   - Generate `artifacts/paper/v1.11/raw-hybrid/`.
   - Add file-backed regression tests for manifest, source locks, scientific-law rows, figures, tables, and forbidden claim wording.
   - Rationale: final package should be validated after all source artifacts are stable.

## Test Strategy

| Test Area | Files | Assertions |
|-----------|-------|------------|
| Benchmark suites | `tests/test_benchmark_runner.py` | v1.11 suites expand deterministically; start modes/training modes are claim-safe; logistic/Planck unsupported probes preserve strict gates. |
| CLI smoke | `tests/test_verifier_demos_cli.py` | `benchmark v1.11-paper-smoke`, focused probe commands, and package commands write expected outputs. |
| Paper assets | `tests/test_paper_assets.py` | Fixture aggregates produce deterministic CSV/SVG outputs; figures cite adjacent source tables; empty inputs produce explicit empty figures. |
| Paper package unit | `tests/test_raw_hybrid_paper.py` | v1.11 source inventory includes v1.10 logistic/Planck sources; missing required sources fail closed; overwrite remains managed-file only. |
| Paper package regression | new `tests/test_v111_paper_package_regression.py` | Committed package has expected files, source locks hash real files, scientific-law rows use v1.10 logistic depth 15 and Planck depth 14, claim boundaries contain "not blind discovery". |
| Baseline diagnostics | `tests/test_baseline_diagnostics.py` | Baseline schema is stable; unavailable external baseline rows are explicit; baseline rows are not counted as EML recovery. |
| Documentation locks | docs/README tests or `rg` checks | Docs mention v1.11 roots, package command, claim boundaries, and baseline scope. |

Use fixture aggregates for unit tests and one small smoke suite for CLI integration. Real v1.11 campaigns should be reproducible commands and committed artifacts, but pytest should not depend on long training runs.

## Anti-Patterns to Avoid

### Paper Package Runs Training

**What:** `raw_hybrid_paper.py` calls benchmark/campaign/training code when generating the package.  
**Why bad:** Source locks become ambiguous, package generation becomes expensive and nondeterministic, and failures are harder to audit.  
**Instead:** Generate evidence first, then synthesize from locked files.

### Figure Code Reclassifies Evidence

**What:** A plotting helper decides recovery from loss thresholds or string matches in formulas.  
**Why bad:** It bypasses verifier-owned recovery and can silently change claims.  
**Instead:** Figures consume `claim_status`, `classification`, `evidence_class`, and compiler diagnostics already emitted by benchmark artifacts.

### Baselines Mixed Into EML Recovery Denominators

**What:** External or conventional baselines become a `BenchmarkRun.start_mode`.  
**Why bad:** Benchmark counts are currently about EML regimes; mixing baselines makes recovery rates ambiguous.  
**Instead:** Separate `baseline_diagnostics` schema and separate package section.

### Stale Scientific-Law Rows

**What:** v1.11 package continues reading v1.6 Planck/logistic diagnostic run paths.  
**Why bad:** It misses the v1.10 motif-shortening evidence, which is an explicit v1.11 goal.  
**Instead:** v1.11 source inventory must prefer v1.10 focused aggregate/run artifacts for Planck and logistic.

### Aggregate Depends on Unlocked Run Files

**What:** Paper figures load runtime or metrics by following `artifact_path` from an aggregate, but source locks only hash the aggregate.  
**Why bad:** The package can change if raw run files change while the aggregate hash stays fixed.  
**Instead:** Put required figure metrics into aggregate summaries or lock every run artifact used by paper assets.

## Scalability Considerations

| Concern | Small v1.11 Runs | Larger Paper Runs | Future Broad Benchmarks |
|---------|------------------|-------------------|-------------------------|
| Runtime | Sequential benchmark execution is acceptable. | Use stable suite labels and run filters; do not add parallelism until artifacts are stable. | Add parallel runner only if run manifests remain deterministic. |
| Artifact size | JSON/CSV/SVG are fine. | Source locks should list exact files, not directories. | Consider compressed archives plus manifest if run count grows substantially. |
| Figure quality | Deterministic SVG helpers are sufficient. | Add paper-specific layout in `paper_assets.py`. | Add a plotting dependency only after deciding dependency policy. |
| Baselines | Local conventional diagnostics only. | External adapters fail soft if unavailable. | Matched-budget comparisons need a separate milestone. |

## Sources

- `.planning/PROJECT.md` - v1.11 goals, active requirements, claim boundaries, and artifact expectations.
- `docs/IMPLEMENTATION.md` - current architecture, recovery contract, benchmark evidence contract, campaign contract, and v1.9 raw-hybrid package contract.
- `src/eml_symbolic_regression/benchmark.py` - benchmark suite registry, run execution, metrics, aggregation, evidence classes, and v1.10 focused suites.
- `src/eml_symbolic_regression/campaign.py` - campaign presets, guarded output folders, CSV exports, SVG generation, and report assembly.
- `src/eml_symbolic_regression/raw_hybrid_paper.py` - synthesis-only paper package writer, source locks, regime summary, scientific-law table extraction, and claim-boundary docs.
- `src/eml_symbolic_regression/cli.py` - CLI integration points for benchmark, campaign, paper-decision, diagnostics, proof-campaign, and raw-hybrid package generation.
- `tests/test_benchmark_runner.py` - current benchmark, repair/refit, focused scientific-law, and v1.10 logistic/Planck contract tests.
- `tests/test_verifier_demos_cli.py` - demo, benchmark CLI, v1.10 focused artifact, and paper-decision CLI coverage.
- `tests/test_raw_hybrid_paper.py` and `tests/test_raw_hybrid_paper_regression.py` - existing paper-package source-lock and regression patterns that v1.11 should extend.
