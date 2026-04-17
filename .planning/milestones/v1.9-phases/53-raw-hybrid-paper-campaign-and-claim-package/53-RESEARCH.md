# Phase 53: Raw-Hybrid Paper Campaign and Claim Package - Research

**Researched:** 2026-04-17  
**Domain:** Python evidence synthesis, benchmark reporting, paper-facing claim boundaries, and documentation gating. [VERIFIED: 53-CONTEXT.md; VERIFIED: codebase rg]  
**Confidence:** HIGH for current implementation and committed artifact facts; MEDIUM for exact implementation slice names because those are recommended, not existing. [VERIFIED: codebase rg; VERIFIED: artifact JSON inspection]

<user_constraints>
## User Constraints (from 53-CONTEXT.md)

### Locked Decisions

The following locked decisions are copied verbatim from `53-CONTEXT.md`. [VERIFIED: 53-CONTEXT.md]

- Package and report existing measured evidence; do not silently rerun broad historical campaigns unless a focused Phase 53 suite requires it.
- Keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate in every claim table/report.
- Treat Arrhenius and Michaelis as exact compiler warm-start / same-AST basin evidence, not blind discovery.
- Treat Phase 52 repair output as repair-only negative evidence: expanded candidate pool preserves fallback behavior but did not improve the selected cases.
- Treat centered-family results as negative diagnostics under the missing same-family witness caveat, not as an impossibility theorem.
- Prefer a reproducible paper-facing suite/preset and durable artifacts under a v1.9 paper path rather than editing archived v1.5/v1.6/v1.8 evidence.

### Claude's Discretion

No `## Claude's Discretion` section is present in `53-CONTEXT.md`. [VERIFIED: 53-CONTEXT.md]

### Deferred Ideas (OUT OF SCOPE)

No `## Deferred Ideas` section is present in `53-CONTEXT.md`. [VERIFIED: 53-CONTEXT.md]

### Non-Goals

The following non-goals are copied verbatim from `53-CONTEXT.md`. [VERIFIED: 53-CONTEXT.md]

- Do not change verifier thresholds or reclassify historical outcomes.
- Do not present warm-start, scaffolded, or same-AST returns as blind discovery.
- Do not claim centered-family impossibility or completeness gaps beyond measured evidence.
- Do not add new scientific demos such as Planck/logistic as solved results unless evidence supports them; they can remain unsupported/diagnostic rows.
- Do not update README/docs before successful artifact generation.

### Open Questions From Context

The following open questions are copied verbatim from `53-CONTEXT.md`. [VERIFIED: 53-CONTEXT.md]

1. Should Phase 53 create one new v1.9 raw-hybrid paper suite/campaign artifact, or synthesize from existing committed aggregates plus focused v1.9 evidence?
2. Which report generator is closest: `campaign.py`, `paper_decision.py`, a new module, or an extension?
3. What is the minimal runnable suite that satisfies RHY-01 without duplicating broad historical proof campaigns?
4. Which scientific-law rows should be included for Beer-Lambert, Shockley, Arrhenius, Michaelis, and unsupported/stretch cases, and where should compile diagnostics be sourced?
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| RHY-01 | Paper-facing raw-hybrid suite/campaign preset includes shallow blind boundaries, perturbed basin evidence, Beer-Lambert, Shockley, Arrhenius, and Michaelis diagnostics. | Use a v1.9 paper package that references proof aggregates for shallow/blind/basin evidence and focused scientific-law run artifacts for Beer-Lambert, Shockley, Arrhenius, and Michaelis diagnostics. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifacts/proof/v1.6/campaigns; VERIFIED: artifacts/campaigns/v1.6-standard; VERIFIED: artifacts/campaigns/v1.9-arrhenius-evidence; VERIFIED: artifacts/campaigns/v1.9-michaelis-evidence] |
| RHY-02 | Reports keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate. | Existing benchmark classification already tracks `start_mode`, `evidence_class`, `return_kind`, `raw_status`, `repair_status`, and `refit_status`; Phase 53 should preserve those fields in a new paper report rather than collapsing them into one recovery rate. [VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| RHY-03 | Scientific-law tables include formula, compile support, compile depth, macro hits, warm-start status, verifier status, and artifact path. | Current campaign CSV/report columns do not expose all compile diagnostics as table columns, while run JSON payloads contain `compiled_eml.metadata`; Phase 53 needs a dedicated extractor for those fields. [VERIFIED: src/eml_symbolic_regression/campaign.py; VERIFIED: artifact JSON inspection] |
| RHY-04 | Centered-family results are reported only as negative diagnostics with same-family witness caveat. | The v1.8 paper decision package chose `publish_raw_eml_searchability_note` and documents that centered-family mathematical claims remain operator/geometry-level until constructive completeness exists. [VERIFIED: artifacts/paper/v1.8/decision-memo.json; VERIFIED: artifacts/paper/v1.8/completeness-boundary.md] |
| RHY-05 | README/docs update only after successful artifacts and avoid blind-discovery overclaims. | Current README and implementation docs already contain careful v1.9 evidence boundaries; Phase 53 should update them only after new v1.9 paper package artifacts exist. [VERIFIED: README.md; VERIFIED: docs/IMPLEMENTATION.md; VERIFIED: 53-CONTEXT.md] |
</phase_requirements>

## Summary

Phase 53 should be a synthesis-first paper package, not a broad rerun phase. [VERIFIED: 53-CONTEXT.md] The committed evidence already covers shallow pure-blind boundaries, scaffolded shallow recovery, perturbed true-tree basin recovery, depth degradation, centered-family negative diagnostics, Arrhenius same-AST evidence, Michaelis same-AST evidence, and repair-only negative evidence. [VERIFIED: artifacts/proof/v1.6/campaigns; VERIFIED: artifacts/paper/v1.8; VERIFIED: artifacts/campaigns/v1.9-arrhenius-evidence; VERIFIED: artifacts/campaigns/v1.9-michaelis-evidence; VERIFIED: artifacts/campaigns/v1.9-repair-evidence]

The safest implementation is a new raw-hybrid paper-package module and CLI command that reads locked source artifacts, validates their presence and expected regimes, writes manifest/source-lock files, renders regime-separated reports, writes scientific-law tables, and gates README/docs updates on successful package generation. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py; VERIFIED: src/eml_symbolic_regression/paper_decision.py; VERIFIED: src/eml_symbolic_regression/campaign.py] Existing `campaign.py` and `paper_decision.py` are useful patterns, but neither currently owns this exact synthesis responsibility. [VERIFIED: src/eml_symbolic_regression/campaign.py; VERIFIED: src/eml_symbolic_regression/paper_decision.py]

**Primary recommendation:** Add a dedicated `raw_hybrid_paper` package writer that synthesizes existing committed evidence into `artifacts/paper/v1.9/raw-hybrid/`, then update README/docs only in a final gated slice after the new package exists. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifacts directory inspection]

## Direct Answers To Open Questions

| Question | Implementation-Ready Answer |
|----------|-----------------------------|
| One v1.9 suite artifact or synthesis from existing aggregates? | Create one durable v1.9 paper package under `artifacts/paper/v1.9/raw-hybrid/` that synthesizes existing committed aggregates and focused v1.9 evidence; do not rerun broad v1.5/v1.6/v1.8 proof campaigns by default. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifacts/proof/v1.6/campaigns; VERIFIED: artifacts/campaigns/v1.9-arrhenius-evidence; VERIFIED: artifacts/campaigns/v1.9-michaelis-evidence] |
| Which report generator is closest? | Use a new module and borrow patterns from `proof_campaign.py` for bundled source aggregates and from `campaign.py` for tabular output; do not extend `paper_decision.py` directly because it is v1.8 centered-family decision-specific. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py; VERIFIED: src/eml_symbolic_regression/campaign.py; VERIFIED: src/eml_symbolic_regression/paper_decision.py] |
| Minimal runnable suite for RHY-01? | The minimal runnable path is a synthesis command that validates existing source artifacts and writes the paper package; add an optional focused `v1.9-raw-hybrid-paper` benchmark suite only if Phase 53 must regenerate Beer-Lambert/Shockley/Arrhenius/Michaelis current-law run artifacts under the v1.9 paper root. [VERIFIED: 53-CONTEXT.md; VERIFIED: src/eml_symbolic_regression/benchmark.py] |
| Which scientific-law rows? | Include Beer-Lambert, Shockley, Arrhenius, Michaelis as current supported diagnostics; include Planck and logistic only as unsupported/stretch compile diagnostics; optionally include historical Michaelis unsupported as a before/after diagnostic when clearly labeled historical. [VERIFIED: artifact JSON inspection; VERIFIED: 53-CONTEXT.md] |

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Source evidence validation | Python package/backend | CLI | Source artifact existence, JSON parsing, and regime checks belong in reusable Python code, with CLI as a thin entry point. [VERIFIED: src/eml_symbolic_regression/cli.py; VERIFIED: src/eml_symbolic_regression/proof_campaign.py] |
| Paper package generation | Python package/backend | Filesystem artifacts | Report, table, manifest, and claim-boundary rendering are local artifact generation responsibilities. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py; VERIFIED: src/eml_symbolic_regression/paper_decision.py] |
| Focused rerun suite | Benchmark/campaign layer | CLI | Existing benchmark suite definitions and campaign runners own reproducible case execution. [VERIFIED: src/eml_symbolic_regression/benchmark.py; VERIFIED: src/eml_symbolic_regression/campaign.py] |
| Scientific-law table extraction | Paper package module | Benchmark artifact schema | Compile depth, macro hits, warm-start status, verifier status, and artifact paths should be extracted from run JSON payloads and rendered into CSV/JSON/Markdown. [VERIFIED: artifact JSON inspection; VERIFIED: src/eml_symbolic_regression/campaign.py] |
| README/docs update | Documentation | Paper package artifacts | Documentation changes are gated by successful package artifacts to avoid pre-claiming results. [VERIFIED: 53-CONTEXT.md; VERIFIED: README.md; VERIFIED: docs/IMPLEMENTATION.md] |

## Project Constraints

No `CLAUDE.md` exists at repo root. [VERIFIED: test -f CLAUDE.md] `AGENTS.md` requires paper fidelity to `sources/paper.pdf` and `sources/NORTH_STAR.md`, complex128-first numerics, verification beyond training loss, realistic v1 scope, demos from `sources/FOR_DEMO.md`, and GSD workflow discipline before source edits. [CITED: AGENTS.md] No project skills exist under `.claude/skills/` or `.agents/skills/`. [VERIFIED: filesystem inspection]

Nyquist validation is explicitly disabled in `.planning/config.json`, so this research omits a Validation Architecture section. [VERIFIED: .planning/config.json] Security enforcement is not explicitly disabled in `.planning/config.json`, so this research includes a Security Domain section for local artifact generation. [VERIFIED: .planning/config.json]

## Current Implementation Facts

| Area | Fact | Phase 53 Impact |
|------|------|-----------------|
| Built-in benchmark suites | `BUILTIN_SUITES` includes `v1.9-arrhenius-evidence`, `v1.9-michaelis-evidence`, and `v1.9-repair-evidence`; it does not include `v1.9-raw-hybrid-paper`. [VERIFIED: src/eml_symbolic_regression/benchmark.py] | Add a focused suite only if reruns are required; otherwise keep Phase 53 as synthesis. |
| Start modes | Benchmark start modes are `catalog`, `compile`, `blind`, `warm_start`, and `perturbed_tree`. [VERIFIED: src/eml_symbolic_regression/benchmark.py] | Reports can preserve pure blind, compile-only, warm-start, and perturbed-tree regimes using existing fields. |
| Evidence aggregation | `aggregate_evidence` groups by formula, start mode, evidence class, return kind, raw status, repair status, perturbation noise, depth, and seed group. [VERIFIED: src/eml_symbolic_regression/benchmark.py] | The raw-hybrid report should read these aggregate dimensions rather than recomputing a collapsed recovery number. |
| Regime classification | `classify_run` and `evidence_class_for_payload` distinguish repaired candidates, same-AST returns, compile, catalog, blind, and perturbed evidence classes. [VERIFIED: src/eml_symbolic_regression/benchmark.py] | RHY-02 can be satisfied without inventing new labels, but the report must preserve them. |
| Run metrics extraction | Existing run metric extraction includes `warm_start_status`, `repair_status`, `refit_status`, and `verifier_status`; campaign table columns do not expose `compile_support`, `compile_depth`, or `macro_hits` as first-class columns. [VERIFIED: src/eml_symbolic_regression/benchmark.py; VERIFIED: src/eml_symbolic_regression/campaign.py] | RHY-03 requires a new scientific-law table extractor over run JSON payloads. |
| Campaign reports | `campaign.py` has standard, showcase, proof, and family presets; it has no raw-hybrid paper preset. [VERIFIED: src/eml_symbolic_regression/campaign.py] | Add a new command/module for paper-package synthesis rather than relying only on campaign reports. |
| Proof campaign package | `proof_campaign.py` bundles proof presets, writes `proof-campaign.json`, `proof-report.md`, and anchor locks. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py] | Reuse its source-lock and multi-campaign report pattern for Phase 53. |
| Paper decision package | `paper_decision.py` defaults to `artifacts/paper/v1.8` and contains centered-family safe/unsafe claim text. [VERIFIED: src/eml_symbolic_regression/paper_decision.py] | Treat it as an input/source for centered-family diagnostics, not as the main raw-hybrid generator. |
| CLI surface | The CLI exposes benchmark, campaign, proof-campaign, and paper-decision commands; it does not expose a raw-hybrid-paper command. [VERIFIED: src/eml_symbolic_regression/cli.py] | Add a new CLI subcommand after implementing the package writer. |
| README and implementation docs | README and `docs/IMPLEMENTATION.md` already discuss v1.9 Arrhenius, Michaelis, repair evidence, and claim boundaries. [VERIFIED: README.md; VERIFIED: docs/IMPLEMENTATION.md] | Update docs only after the new v1.9 raw-hybrid artifacts are generated. |

## Existing Evidence Inventory

| Evidence Source | Current Fact | Use In Phase 53 |
|-----------------|--------------|-----------------|
| `artifacts/proof/v1.6/campaigns/proof-shallow-pure-blind/aggregate.json` | The pure-blind shallow proof aggregate has 18 runs, 3 verifier-recovered runs overall, 2 threshold-passing pure-blind recoveries, 1 repaired candidate, 1 failed run, and 14 snapped-but-failed runs. [VERIFIED: aggregate JSON inspection] | Report shallow blind boundaries and keep repaired candidate separate from pure blind recovery. |
| `artifacts/proof/v1.6/campaigns/proof-shallow/aggregate.json` | The scaffolded shallow proof aggregate has 18 runs and 18 scaffolded blind-training recoveries. [VERIFIED: aggregate JSON inspection] | Report scaffolded recovery separately from pure blind. |
| `artifacts/proof/v1.6/campaigns/proof-basin/aggregate.json` | The perturbed true-tree basin aggregate has 9 runs and 9 same-AST perturbed true-tree recoveries. [VERIFIED: aggregate JSON inspection] | Report bounded perturbed-basin evidence. |
| `artifacts/proof/v1.6/campaigns/proof-basin-probes/aggregate.json` | The Beer high-noise probe aggregate has 4 recovered runs, with 1 perturbed true-tree recovery and 3 repaired candidates. [VERIFIED: aggregate JSON inspection] | Use as diagnostic perturbed/repaired evidence, not as pure basin evidence. |
| `artifacts/proof/v1.6/campaigns/proof-depth-curve/aggregate.json` | The depth curve aggregate has 20 runs, 14 verifier-recovered runs, 10 same-AST returns, and blind recovery drops to 0/2 at depths 4, 5, and 6 in the measured curve. [VERIFIED: aggregate JSON inspection] | Report depth degradation and shallow blind boundary. |
| `artifacts/paper/v1.8/decision-memo.json` | The centered-family decision is `publish_raw_eml_searchability_note`, with raw recovery rate 0.8 and best centered recovery rate 0.0 across the decision package inputs. [VERIFIED: artifacts/paper/v1.8/decision-memo.json] | Report centered-family only as negative diagnostics with same-family witness caveat. |
| `artifacts/campaigns/v1.9-arrhenius-evidence/.../aggregate.json` | Arrhenius v1.9 focused evidence has 1 run, 1 same-AST return, and 1 verifier recovery. [VERIFIED: aggregate JSON inspection] | Use as exact compiler warm-start/same-AST evidence. |
| `artifacts/campaigns/v1.9-michaelis-evidence/.../aggregate.json` | Michaelis v1.9 focused evidence has 1 run, 1 same-AST return, and 1 verifier recovery. [VERIFIED: aggregate JSON inspection] | Use as exact compiler warm-start/same-AST evidence. |
| `artifacts/campaigns/v1.9-repair-evidence/.../aggregate.json` | Repair v1.9 focused evidence has 4 snapped-but-failed runs and 0 verifier recoveries. [VERIFIED: aggregate JSON inspection] | Report Phase 52 as repair-only negative evidence with preserved fallback behavior. |
| `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.json` | Expanded repair candidate pool has 0 default repairs, 0 expanded repairs, 0 improvements, 0 final status regressions, and fallback manifests preserved. [VERIFIED: repair-evidence-summary.json inspection] | Use as repair boundary evidence, not as recovery evidence. |

## Scientific-Law Table Plan

| Law | Formula | Compile Support | Compile Depth | Macro Hits | Warm-Start Status | Verifier Status | Artifact Path | Reporting Boundary |
|-----|---------|-----------------|---------------|------------|-------------------|-----------------|---------------|--------------------|
| Beer-Lambert | `exp(-0.8*x)` [VERIFIED: artifact JSON inspection] | Recovered [VERIFIED: artifact JSON inspection] | 9 [VERIFIED: artifact JSON inspection] | `[]` [VERIFIED: artifact JSON inspection] | `same_ast_return` [VERIFIED: artifact JSON inspection] | `recovered` [VERIFIED: artifact JSON inspection] | `artifacts/campaigns/v1.6-standard/runs/v1.3-standard/v1-3-standard-beer-perturbation-sweep-c671cedf25f1.json` [VERIFIED: filesystem inspection] | Warm-start/same-AST diagnostic, not blind discovery. [VERIFIED: 53-CONTEXT.md] |
| Shockley diode | `0.2*exp(1.4*x) - 0.2` [VERIFIED: artifact JSON inspection] | Recovered [VERIFIED: artifact JSON inspection] | 13 [VERIFIED: artifact JSON inspection] | `scaled_exp_minus_one_template` [VERIFIED: artifact JSON inspection] | `same_ast_return` [VERIFIED: artifact JSON inspection] | `recovered` [VERIFIED: artifact JSON inspection] | `artifacts/campaigns/v1.6-standard/runs/v1.3-standard/v1-3-standard-shockley-warm-316f98a5b1fb.json` [VERIFIED: filesystem inspection] | Warm-start/same-AST diagnostic, not blind discovery. [VERIFIED: 53-CONTEXT.md] |
| Arrhenius | `exp(-0.8/x)` [VERIFIED: artifact JSON inspection] | Recovered [VERIFIED: artifact JSON inspection] | 7 [VERIFIED: artifact JSON inspection] | `direct_division_template` [VERIFIED: artifact JSON inspection] | `same_ast_return` [VERIFIED: artifact JSON inspection] | `recovered` [VERIFIED: artifact JSON inspection] | `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/v1-9-arrhenius-evidence-arrhenius-warm-75f6e9c1764d.json` [VERIFIED: filesystem inspection] | Exact compiler warm-start/same-AST evidence, not blind discovery. [VERIFIED: 53-CONTEXT.md] |
| Michaelis-Menten | `2*x/(x + 0.5)` [VERIFIED: artifact JSON inspection] | Recovered [VERIFIED: artifact JSON inspection] | 12 [VERIFIED: artifact JSON inspection] | `saturation_ratio_template` [VERIFIED: artifact JSON inspection] | `same_ast_return` [VERIFIED: artifact JSON inspection] | `recovered` [VERIFIED: artifact JSON inspection] | `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/v1-9-michaelis-evidence-michaelis-warm-a67d8ccfb108.json` [VERIFIED: filesystem inspection] | Exact compiler warm-start/same-AST evidence, not blind discovery. [VERIFIED: 53-CONTEXT.md] |
| Planck diagnostic | `x**3/(exp(x) - 1)` [VERIFIED: artifact JSON inspection] | Unsupported under strict depth because compiled depth 20 exceeds `max_depth=13`; relaxed diagnostics contain depth 20 and macro hits `scaled_exp_minus_one_template` and `direct_division_template`. [VERIFIED: artifact JSON inspection] | 20 relaxed [VERIFIED: artifact JSON inspection] | `scaled_exp_minus_one_template`, `direct_division_template` [VERIFIED: artifact JSON inspection] | N/A unless run through warm-start diagnostics. [VERIFIED: artifact JSON inspection] | Unsupported diagnostic, not solved. [VERIFIED: 53-CONTEXT.md] | `artifacts/campaigns/v1.6-standard/runs/v1.3-standard/v1-3-standard-planck-diagnostic-2309e6363fc8.json` [VERIFIED: filesystem inspection] | Unsupported/stretch row only. [VERIFIED: 53-CONTEXT.md] |
| Logistic diagnostic | `1/(1 + 2*exp(-1.3*x))` [VERIFIED: artifact JSON inspection] | Unsupported under strict depth because compiled depth 27 exceeds `max_depth=13`; relaxed diagnostics contain depth 27 and no macro hits. [VERIFIED: artifact JSON inspection] | 27 relaxed [VERIFIED: artifact JSON inspection] | `[]` [VERIFIED: artifact JSON inspection] | N/A unless run through warm-start diagnostics. [VERIFIED: artifact JSON inspection] | Unsupported diagnostic, not solved. [VERIFIED: 53-CONTEXT.md] | `artifacts/campaigns/v1.6-standard/runs/v1.3-standard/v1-3-standard-logistic-compile-a99c41f57b97.json` [VERIFIED: filesystem inspection] | Unsupported/stretch row only. [VERIFIED: 53-CONTEXT.md] |
| Historical Michaelis diagnostic | `2*x/(x + 0.5)` [VERIFIED: artifact JSON inspection] | Historical strict compile unsupported because compiled depth 14 exceeded `max_depth=13`; relaxed diagnostics had depth 14 and `direct_division_template`. [VERIFIED: artifact JSON inspection] | 14 relaxed [VERIFIED: artifact JSON inspection] | `direct_division_template` [VERIFIED: artifact JSON inspection] | Diagnostic historical row only. [VERIFIED: artifact JSON inspection] | Unsupported historical diagnostic. [VERIFIED: artifact JSON inspection] | `artifacts/campaigns/v1.6-standard/runs/v1.3-standard/v1-3-standard-michaelis-warm-diagnostic-9917f8383370.json` [VERIFIED: filesystem inspection] | Use only as before/after context for the Phase 51 compiler improvement. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-03-SUMMARY.md] |

## Recommended Implementation Slices

1. Add a dedicated paper package writer, recommended as `src/eml_symbolic_regression/raw_hybrid_paper.py`, with typed source definitions for aggregate paths, run artifact paths, expected regimes, and output files. [ASSUMED] The module should read JSON with `json.loads`, validate required keys, and fail closed when a required evidence file or required table field is missing. [VERIFIED: Python stdlib availability; VERIFIED: artifact JSON schema inspection]
2. Add a CLI subcommand, recommended as `raw-hybrid-paper`, that writes `manifest.json`, `source-locks.json`, `raw-hybrid-report.md`, `scientific-law-table.csv`, `scientific-law-table.json`, `scientific-law-table.md`, `claim-boundaries.md`, and `centered-negative-diagnostics.md` under `artifacts/paper/v1.9/raw-hybrid/`. [ASSUMED] This mirrors the artifact package pattern used by `proof_campaign.py` and `paper_decision.py`. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py; VERIFIED: src/eml_symbolic_regression/paper_decision.py]
3. Add a source-lock helper that hashes specific source files rather than whole directories. [ASSUMED] Specific-file locks are more stable for paper packaging because proof and campaign directories contain many historical run files that are not all Phase 53 inputs. [VERIFIED: artifacts directory inspection]
4. Add a scientific-law extractor that pulls formula, compile support, compile depth, compile node count, macro hits, warm-start status, verifier status, evidence class, regime label, and artifact path from run payloads. [VERIFIED: artifact JSON inspection] The extractor must keep unsupported relaxed compile diagnostics separate from recovered strict compile support. [VERIFIED: artifact JSON inspection; VERIFIED: 53-CONTEXT.md]
5. Add a regime report renderer that contains separate sections for pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed basin evidence. [VERIFIED: 53-CONTEXT.md; VERIFIED: src/eml_symbolic_regression/benchmark.py]
6. Add an optional focused benchmark suite only if the planner wants current v1.9 run artifacts for Beer-Lambert and Shockley instead of citing v1.6 standard run artifacts. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifacts/campaigns/v1.6-standard] If added, recommended cases are Beer-Lambert warm-start, Shockley warm-start, Arrhenius warm-start, Michaelis warm-start, and compile-only unsupported diagnostics for Planck/logistic. [ASSUMED]
7. Update README and `docs/IMPLEMENTATION.md` only after the raw-hybrid package command succeeds and the new paper artifacts exist. [VERIFIED: 53-CONTEXT.md; VERIFIED: README.md; VERIFIED: docs/IMPLEMENTATION.md]

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11.5 local [VERIFIED: local command output] | Artifact synthesis, CLI wiring, JSON/CSV/Markdown rendering. [VERIFIED: codebase rg] | Existing project runtime is Python and current package modules are Python. [VERIFIED: AGENTS.md; VERIFIED: src/eml_symbolic_regression] |
| Python stdlib `json`, `csv`, `hashlib`, `pathlib`, `dataclasses` | Python 3.11.5 local [VERIFIED: local command output] | Parse source artifacts, write tables, hash locks, and model simple records. [VERIFIED: codebase rg] | No new dependency is needed for Phase 53 artifact packaging. [VERIFIED: dependency inspection] |
| Existing `benchmark.py` classification and aggregate schema | Project code [VERIFIED: src/eml_symbolic_regression/benchmark.py] | Source regime labels and aggregate dimensions. [VERIFIED: src/eml_symbolic_regression/benchmark.py] | This avoids reclassifying historical results. [VERIFIED: 53-CONTEXT.md] |
| Existing `campaign.py` table/report conventions | Project code [VERIFIED: src/eml_symbolic_regression/campaign.py] | Reuse Markdown/CSV/report style. [VERIFIED: src/eml_symbolic_regression/campaign.py] | Existing campaign reports are the closest table/report precedent. [VERIFIED: src/eml_symbolic_regression/campaign.py] |
| Existing `proof_campaign.py` bundle pattern | Project code [VERIFIED: src/eml_symbolic_regression/proof_campaign.py] | Reuse multi-source report and source-lock pattern. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py] | Phase 53 is a multi-evidence paper package rather than one benchmark run. [VERIFIED: 53-CONTEXT.md] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | 7.4.0 local [VERIFIED: local command output] | Unit and CLI smoke tests for the package writer. [VERIFIED: tests directory inspection] | Use for implementation tests once the module exists. [VERIFIED: tests directory inspection] |
| NumPy | 1.26.4 local [VERIFIED: local command output] | Only needed if a focused benchmark rerun is added. [VERIFIED: AGENTS.md; VERIFIED: src/eml_symbolic_regression/datasets.py] | Do not require it for synthesis-only table generation beyond existing project dependency. [VERIFIED: codebase rg] |
| PyTorch | 2.10.0 local [VERIFIED: local command output] | Only needed if a focused benchmark rerun is added. [VERIFIED: AGENTS.md; VERIFIED: src/eml_symbolic_regression/benchmark.py] | Synthesis-only package generation should not invoke training. [VERIFIED: 53-CONTEXT.md] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| New `raw_hybrid_paper.py` module | Extend `paper_decision.py` | `paper_decision.py` is centered-family v1.8-specific and defaults to `artifacts/paper/v1.8`, so extending it risks mixing raw-hybrid reporting with centered decision logic. [VERIFIED: src/eml_symbolic_regression/paper_decision.py] |
| Synthesis command over existing artifacts | Rerun broad proof campaigns | Broad proof evidence already exists and the context says not to silently rerun it unless focused Phase 53 suite requires it. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifacts/proof/v1.6/campaigns] |
| Dedicated scientific-law extractor | Reuse campaign CSV as-is | Campaign columns do not currently expose compile support, compile depth, or macro hits as required scientific-law table fields. [VERIFIED: src/eml_symbolic_regression/campaign.py] |

**Installation:** no new packages are required for the synthesis path. [VERIFIED: stdlib usage; VERIFIED: existing dependency inspection]

## Architecture Patterns

### System Architecture Diagram

```text
Committed evidence artifacts
  |-- proof v1.6 aggregates
  |-- v1.8 centered decision package
  |-- v1.9 Arrhenius/Michaelis/repair aggregates
  |-- selected scientific-law run JSON files
        |
        v
Raw-hybrid paper package writer
  |-- validate required paths and expected regimes
  |-- read aggregate/run JSON with structured parsers
  |-- extract regime-separated metrics
  |-- extract scientific-law compile diagnostics
  |-- hash source files into source-locks
        |
        v
Paper artifact outputs under artifacts/paper/v1.9/raw-hybrid/
  |-- manifest/source-locks
  |-- raw-hybrid-report
  |-- scientific-law tables
  |-- claim-boundaries
  |-- centered negative diagnostics
        |
        v
Documentation gate
  |-- update README/docs only after outputs exist and validate
```

The diagram follows the Phase 53 decision to package existing measured evidence and avoid silent broad reruns. [VERIFIED: 53-CONTEXT.md]

### Recommended Project Structure

```text
src/eml_symbolic_regression/
├── raw_hybrid_paper.py   # recommended paper-package synthesis module [ASSUMED]
├── cli.py                # add raw-hybrid-paper subcommand [VERIFIED: existing file]
├── benchmark.py          # source suite/regime schema [VERIFIED: existing file]
└── campaign.py           # source report/table style [VERIFIED: existing file]

tests/
├── test_raw_hybrid_paper.py        # recommended unit/contract tests [ASSUMED]
└── test_raw_hybrid_paper_cli.py    # recommended CLI smoke coverage [ASSUMED]

artifacts/paper/v1.9/raw-hybrid/
├── manifest.json
├── source-locks.json
├── raw-hybrid-report.md
├── scientific-law-table.csv
├── scientific-law-table.json
├── scientific-law-table.md
├── claim-boundaries.md
└── centered-negative-diagnostics.md
```

### Pattern 1: Synthesis Over Immutable Inputs

**What:** Read existing aggregate/run artifacts and emit a new paper package that records source paths and source hashes. [VERIFIED: artifacts directory inspection; VERIFIED: src/eml_symbolic_regression/proof_campaign.py]  
**When to use:** Use this for RHY-01 through RHY-05 because the context locks existing evidence as the primary input. [VERIFIED: 53-CONTEXT.md]  
**Example:**

```python
from pathlib import Path
import hashlib
import json


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
```

This pattern uses stdlib APIs already available in the local Python runtime. [VERIFIED: local Python 3.11.5]

### Pattern 2: Regime Labels Are Data, Not Prose

**What:** Store regime labels and evidence classes as explicit fields in JSON/CSV tables, then render human-readable prose from those fields. [VERIFIED: src/eml_symbolic_regression/benchmark.py]  
**When to use:** Use this for RHY-02 because prose-only labels are easy to accidentally collapse into overclaims. [VERIFIED: 53-CONTEXT.md]

### Pattern 3: Fail Closed On Missing Evidence

**What:** If a required source artifact is missing, or if a required table field cannot be extracted, the paper package command should fail rather than emit a partial claim package. [VERIFIED: 53-CONTEXT.md]  
**When to use:** Use this for all paper-facing outputs because README/docs are gated on successful artifacts. [VERIFIED: 53-CONTEXT.md]

### Anti-Patterns To Avoid

- **Collapsing all verifier recoveries into one recovery rate:** This would mix pure blind, scaffolded, same-AST, repaired, and perturbed regimes in violation of RHY-02. [VERIFIED: 53-CONTEXT.md]
- **Calling Arrhenius or Michaelis blind discoveries:** Both are locked as exact compiler warm-start / same-AST basin evidence. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifacts/campaigns/v1.9-arrhenius-evidence; VERIFIED: artifacts/campaigns/v1.9-michaelis-evidence]
- **Treating centered-family failures as an impossibility theorem:** The v1.8 decision package documents missing same-family constructive witnesses, not impossibility. [VERIFIED: artifacts/paper/v1.8/completeness-boundary.md]
- **Updating README before package artifacts exist:** The context explicitly forbids documentation updates before successful artifact generation. [VERIFIED: 53-CONTEXT.md]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Regime classification | A new ad hoc status taxonomy | Existing `classify_run`, `evidence_class_for_payload`, aggregate dimensions, and run payload fields. [VERIFIED: src/eml_symbolic_regression/benchmark.py] | Existing labels already distinguish the required regimes. [VERIFIED: src/eml_symbolic_regression/benchmark.py; VERIFIED: 53-CONTEXT.md] |
| JSON artifact parsing | Regex or line-based parsing | `json.loads` over committed JSON artifacts. [VERIFIED: Python stdlib; VERIFIED: artifact JSON inspection] | Compile diagnostics and nested metadata are structured JSON fields. [VERIFIED: artifact JSON inspection] |
| Proof threshold recomputation | New threshold math in Phase 53 | Read threshold results from existing proof aggregate JSON. [VERIFIED: artifacts/proof/v1.6/campaigns] | Recomputing historical classifications risks drift from committed evidence. [VERIFIED: 53-CONTEXT.md] |
| Broad campaign orchestration | A bespoke runner | Existing benchmark/campaign/proof-campaign runners. [VERIFIED: src/eml_symbolic_regression/benchmark.py; VERIFIED: src/eml_symbolic_regression/campaign.py; VERIFIED: src/eml_symbolic_regression/proof_campaign.py] | Phase 53 is packaging-first, and broad proof campaigns already have artifacts. [VERIFIED: 53-CONTEXT.md] |
| Markdown table formatting | Handwritten one-off table strings spread across modules | One renderer function fed by structured row dictionaries. [ASSUMED] | RHY-03 requires the same fields in CSV, JSON, and Markdown outputs. [VERIFIED: 53-CONTEXT.md] |

**Key insight:** The hard part of Phase 53 is preserving claim boundaries across already-measured evidence, not discovering new formulas. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifact inventory]

## Testing And Evidence Strategy

| Test/Evidence Layer | Recommended Check | Requirement Coverage |
|---------------------|-------------------|----------------------|
| Unit tests for source loading | Build temp aggregate/run JSON fixtures and verify missing required paths or missing required fields fail closed. [ASSUMED] | RHY-01, RHY-03, RHY-05 |
| Unit tests for regime separation | Feed mixed synthetic rows covering pure blind, scaffolded, compile-only, warm-start, same-AST, repaired, refit, and perturbed-basin regimes, then assert separate report sections. [ASSUMED] | RHY-02 |
| Unit tests for scientific-law table | Assert required columns include formula, compile support, compile depth, macro hits, warm-start status, verifier status, and artifact path. [VERIFIED: 53-CONTEXT.md] | RHY-03 |
| Fixture-backed artifact test | Use committed Arrhenius and Michaelis v1.9 run JSON files to verify compile depth and macro-hit extraction. [VERIFIED: artifacts/campaigns/v1.9-arrhenius-evidence; VERIFIED: artifacts/campaigns/v1.9-michaelis-evidence] | RHY-03 |
| Centered-family report test | Use v1.8 decision artifacts and assert centered-family output is labeled negative diagnostic with same-family witness caveat. [VERIFIED: artifacts/paper/v1.8] | RHY-04 |
| CLI smoke test | Run the new command into a temp output directory and assert all package outputs exist. [ASSUMED] | RHY-01 through RHY-05 |
| Documentation gate test | Before docs update, assert `artifacts/paper/v1.9/raw-hybrid/manifest.json` and report/table files exist. [ASSUMED] | RHY-05 |

Recommended verification commands after implementation:

```bash
PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py tests/test_benchmark_contract.py tests/test_campaign.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir artifacts/paper/v1.9/raw-hybrid --require-existing
```

`PYTHONPATH=src` is required for direct local module execution unless the package is installed. [VERIFIED: local command behavior]

## Risks

| Risk | Why It Matters | Mitigation |
|------|----------------|------------|
| Existing campaign reports lack RHY-03 compile columns | Reusing campaign CSV as-is would omit compile support, compile depth, and macro hits. [VERIFIED: src/eml_symbolic_regression/campaign.py] | Add a dedicated scientific-law table extractor over run JSON payloads. [VERIFIED: artifact JSON inspection] |
| v1.6 Beer-Lambert and Shockley artifacts predate v1.9 focused evidence | A paper-facing v1.9 package might prefer all scientific-law rows under a v1.9 output root. [VERIFIED: artifacts/campaigns/v1.6-standard; VERIFIED: artifacts/campaigns/v1.9-arrhenius-evidence] | Either cite the v1.6 source artifacts explicitly or add a focused current rerun suite for Beer-Lambert and Shockley. [ASSUMED] |
| Historical Michaelis unsupported row can conflict with v1.9 success | The historical row says unsupported while the v1.9 row says recovered. [VERIFIED: artifact JSON inspection] | Label the historical row as before/after compiler-motif context only. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-03-SUMMARY.md] |
| Centered-family diagnostics can be overread | v1.8 centered-family artifacts show negative diagnostics but not impossibility. [VERIFIED: artifacts/paper/v1.8/completeness-boundary.md] | Include the same-family witness caveat in every centered-family table/report section. [VERIFIED: 53-CONTEXT.md] |
| Repair evidence can be mistaken for recovery evidence | Phase 52 repair evidence has 0 recovered runs and 0 improvements. [VERIFIED: artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.json] | Place repair results in a repair-only negative-evidence section. [VERIFIED: 53-CONTEXT.md] |
| Docs already contain v1.9 language | Updating docs before package generation would violate the Phase 53 gate. [VERIFIED: README.md; VERIFIED: docs/IMPLEMENTATION.md; VERIFIED: 53-CONTEXT.md] | Make docs update the final slice after artifact validation. [VERIFIED: 53-CONTEXT.md] |

## Execution Unknowns

1. Whether the planner wants Beer-Lambert and Shockley regenerated under the v1.9 paper root or is comfortable citing their committed v1.6 standard run artifacts. [VERIFIED: 53-CONTEXT.md; VERIFIED: artifacts/campaigns/v1.6-standard]
2. Whether `artifacts/paper/v1.9/raw-hybrid/` is the final desired output path or whether the project prefers a different v1.9 paper subdirectory name. [ASSUMED]
3. Whether source locks should include only files used in final tables/reports or also adjacent aggregate Markdown reports. [ASSUMED]
4. Whether README/docs updates should be committed in the same phase after artifact generation or left as a separate docs-only follow-up. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Synthesis module and CLI | Yes [VERIFIED: local command output] | 3.11.5 [VERIFIED: local command output] | None needed |
| pytest | Implementation tests | Yes [VERIFIED: local command output] | 7.4.0 [VERIFIED: local command output] | Manual artifact inspection, but automated tests are recommended |
| NumPy | Optional focused reruns | Yes [VERIFIED: local command output] | 1.26.4 [VERIFIED: local command output] | Not needed for synthesis-only path |
| PyTorch | Optional focused reruns | Yes [VERIFIED: local command output] | 2.10.0 [VERIFIED: local command output] | Not needed for synthesis-only path |
| SymPy | Existing compiler/simplifier path if reruns happen | Yes [VERIFIED: local command output] | 1.14.0 [VERIFIED: local command output] | Not needed for synthesis-only path |
| mpmath | Existing verifier path if reruns happen | Yes [VERIFIED: local command output] | 1.3.0 [VERIFIED: local command output] | Not needed for synthesis-only path |

**Missing dependencies with no fallback:** none found for the synthesis path. [VERIFIED: local command output]  
**Missing dependencies with fallback:** CUDA is unavailable locally and is not required for Phase 53. [VERIFIED: AGENTS.md; VERIFIED: local stack context]

## Security Domain

Phase 53 is local artifact generation and documentation packaging; it does not introduce authentication, sessions, remote user input, database access, or network services. [VERIFIED: 53-CONTEXT.md; VERIFIED: codebase rg] The relevant security concern is input validation for local file paths and JSON schemas. [VERIFIED: proposed CLI scope; VERIFIED: artifact JSON inspection]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | No [VERIFIED: phase scope] | No authentication surface is introduced. [VERIFIED: 53-CONTEXT.md] |
| V3 Session Management | No [VERIFIED: phase scope] | No session surface is introduced. [VERIFIED: 53-CONTEXT.md] |
| V4 Access Control | No [VERIFIED: phase scope] | Local developer CLI only; no multi-user authorization boundary is introduced. [VERIFIED: codebase rg] |
| V5 Input Validation | Yes [VERIFIED: proposed CLI scope] | Validate required source paths, expected JSON keys, and output directory behavior before writing paper claims. [VERIFIED: 53-CONTEXT.md] |
| V6 Cryptography | Limited [VERIFIED: proposed source-lock scope] | Use SHA-256 only for source integrity locks, not for security-sensitive secrets. [ASSUMED] |

### Known Threat Patterns

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Path confusion causing the report to cite the wrong evidence file | Tampering | Resolve and record source paths, hash locked source files, and fail closed on missing files. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py; ASSUMED] |
| Malformed or partial JSON source artifact | Tampering | Parse with `json.loads`, validate required keys, and raise before writing final reports. [VERIFIED: Python stdlib; VERIFIED: artifact JSON inspection] |
| Accidental overclaim in docs | Information integrity risk [ASSUMED] | Gate README/docs changes on successful artifact generation and required claim-boundary sections. [VERIFIED: 53-CONTEXT.md] |

## State Of The Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single campaign recovery summaries | Regime-separated paper package with source locks and claim boundaries. [VERIFIED: 53-CONTEXT.md; VERIFIED: src/eml_symbolic_regression/proof_campaign.py] | Phase 53 target. [VERIFIED: 53-CONTEXT.md] | Prevents warm-start, repaired, perturbed, and blind evidence from being conflated. [VERIFIED: 53-CONTEXT.md] |
| Centered-family comparison as a possible positive claim | Centered-family reported only as negative diagnostic with missing same-family witness caveat. [VERIFIED: artifacts/paper/v1.8/completeness-boundary.md] | v1.8 decision package. [VERIFIED: artifacts/paper/v1.8/decision-memo.json] | Avoids unsupported centered-family theorem claims. [VERIFIED: 53-CONTEXT.md] |
| Michaelis unsupported historical diagnostic | Michaelis v1.9 exact compiler warm-start same-AST evidence. [VERIFIED: artifacts/campaigns/v1.6-standard; VERIFIED: artifacts/campaigns/v1.9-michaelis-evidence] | Phase 51 and v1.9 evidence. [VERIFIED: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-03-SUMMARY.md] | Report as compiler motif improvement, not blind discovery. [VERIFIED: 53-CONTEXT.md] |

**Deprecated/outdated:** Treating a verifier recovery as a paper claim without regime label is outdated for Phase 53 because RHY-02 requires separate pure blind, scaffolded, compile-only, warm-start, same-AST, repaired, refit, and perturbed-basin regimes. [VERIFIED: 53-CONTEXT.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Recommended module name `raw_hybrid_paper.py` and command name `raw-hybrid-paper`. | Recommended Implementation Slices | Low; planner can rename without changing architecture. |
| A2 | Recommended output root `artifacts/paper/v1.9/raw-hybrid/`. | Summary, Direct Answers, Recommended Implementation Slices | Medium; artifact paths in docs/tests must match final planner decision. |
| A3 | Optional focused suite case list for Beer-Lambert, Shockley, Arrhenius, Michaelis, Planck, and logistic. | Recommended Implementation Slices | Medium; unnecessary reruns could increase execution time, while omitting them may leave Beer/Shockley sourced from v1.6. |
| A4 | Source locks should hash specific source files rather than whole directories. | Recommended Implementation Slices | Low; whole-directory locks are more complete but less stable. |
| A5 | README/docs update timing can be planned as a final slice in the same phase. | Execution Unknowns | Low; a separate docs phase would also satisfy the gate if artifacts exist. |

## Open Questions (RESOLVED)

1. **Should Beer-Lambert and Shockley be rerun under a v1.9 paper output path?**  
   Resolution: cite the existing v1.6 standard source artifacts in the v1.9 paper package; do not rerun them in Phase 53.  
   What we know: committed Beer-Lambert and Shockley run artifacts already contain the required compile and warm-start diagnostics. [VERIFIED: artifacts/campaigns/v1.6-standard]  
   What's unclear: whether the paper package should cite v1.6 source artifacts or regenerate focused v1.9 copies for all scientific-law rows. [VERIFIED: 53-CONTEXT.md]  
   Recommendation: cite existing artifacts by default and add a focused rerun only if the planner wants all scientific-law run artifacts under v1.9. [ASSUMED]

2. **Should unsupported Planck/logistic rows be in the main scientific-law table or a separate diagnostic table?**  
   Resolution: include them as explicitly unsupported/stretch diagnostic rows with regime/status fields, not as solved rows.  
   What we know: Planck and logistic strict compiles are unsupported due depth limits in committed diagnostics. [VERIFIED: artifact JSON inspection]  
   What's unclear: table placement, not claim status. [VERIFIED: 53-CONTEXT.md]  
   Recommendation: include them in a separate `unsupported_diagnostics` section or flag column so supported law rows remain visually separate. [ASSUMED]

3. **Should repair-only negative evidence be a table row or a report section?**  
   Resolution: report it as a separate repair-only negative-evidence section/regime bucket; do not create a scientific-law success row for repair.  
   What we know: v1.9 repair evidence has zero improvements and preserved fallback behavior. [VERIFIED: artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.json]  
   What's unclear: final report layout. [ASSUMED]  
   Recommendation: make repair a report section and include no scientific-law success row for repair. [VERIFIED: 53-CONTEXT.md]

## Sources

### Primary (HIGH confidence)

- `53-CONTEXT.md` - phase decisions, non-goals, success criteria, and open questions. [VERIFIED: .planning/phases/53-raw-hybrid-paper-campaign-and-claim-package/53-CONTEXT.md]
- `src/eml_symbolic_regression/benchmark.py` - built-in suites, start modes, aggregate schema, evidence classification, and metrics extraction. [VERIFIED: codebase rg]
- `src/eml_symbolic_regression/campaign.py` - campaign presets, report generation, and existing run table columns. [VERIFIED: codebase rg]
- `src/eml_symbolic_regression/proof_campaign.py` - proof package pattern, source locks, and multi-campaign report rendering. [VERIFIED: codebase rg]
- `src/eml_symbolic_regression/paper_decision.py` - centered-family v1.8 paper decision package behavior. [VERIFIED: codebase rg]
- `src/eml_symbolic_regression/cli.py` - current CLI command surface. [VERIFIED: codebase rg]
- `artifacts/proof/v1.6/campaigns/*/aggregate.json` - shallow blind, scaffolded, perturbed basin, basin probe, and depth curve evidence. [VERIFIED: artifact JSON inspection]
- `artifacts/paper/v1.8/*` - centered-family paper decision and completeness caveat. [VERIFIED: artifact inspection]
- `artifacts/campaigns/v1.9-arrhenius-evidence/*` - Arrhenius focused evidence. [VERIFIED: artifact JSON inspection]
- `artifacts/campaigns/v1.9-michaelis-evidence/*` - Michaelis focused evidence. [VERIFIED: artifact JSON inspection]
- `artifacts/campaigns/v1.9-repair-evidence/*` - repair-only negative evidence. [VERIFIED: artifact JSON inspection]
- `README.md` and `docs/IMPLEMENTATION.md` - current documentation state. [VERIFIED: file inspection]

### Secondary (MEDIUM confidence)

- `.planning/phases/50-arrhenius-exact-warm-start-demo/50-03-SUMMARY.md` - Arrhenius implementation summary. [VERIFIED: file inspection]
- `.planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-03-SUMMARY.md` - Michaelis compiler motif summary. [VERIFIED: file inspection]
- `.planning/phases/52-verifier-gated-exact-cleanup-expansion/52-03-SUMMARY.md` and `52-VERIFICATION.md` - repair evidence summary and verification status. [VERIFIED: file inspection]
- `sources/FOR_DEMO.md` and `sources/NORTH_STAR.md` - demo and architecture constraints. [CITED: sources/FOR_DEMO.md; CITED: sources/NORTH_STAR.md]

### Tertiary (LOW confidence)

- None. [VERIFIED: no web search used]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - Phase 53 needs no new package for the synthesis path, and local versions were verified. [VERIFIED: local command output]
- Architecture: HIGH - existing proof/campaign/paper-decision modules show the relevant patterns and boundaries. [VERIFIED: src/eml_symbolic_regression/proof_campaign.py; VERIFIED: src/eml_symbolic_regression/campaign.py; VERIFIED: src/eml_symbolic_regression/paper_decision.py]
- Artifact facts: HIGH - committed aggregate and run JSON files were inspected directly. [VERIFIED: artifact JSON inspection]
- Exact module/command/output names: MEDIUM - these are recommendations, not existing project decisions. [ASSUMED]
- Pitfalls: HIGH - risks are directly tied to locked context decisions and current artifact/report schema gaps. [VERIFIED: 53-CONTEXT.md; VERIFIED: src/eml_symbolic_regression/campaign.py]

**Research date:** 2026-04-17  
**Valid until:** 2026-05-17, assuming no benchmark artifact schema changes before implementation. [ASSUMED]
