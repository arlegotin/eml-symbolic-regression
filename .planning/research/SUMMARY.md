# v1.11 Research Summary

**Milestone:** v1.11 Paper-strength evidence and figure package  
**Generated:** 2026-04-19  
**Inputs:** `.planning/research/STACK.md`, `.planning/research/FEATURES.md`, `.planning/research/ARCHITECTURE.md`, `.planning/research/PITFALLS.md`

## Synthesis

v1.11 should strengthen the paper by turning the existing evidence base into a current, source-locked, plot-ready package and by adding only claim-safe new evidence. The milestone should not chase a new algorithmic breakthrough before packaging the real state of the system.

The strongest path is:

1. refresh the paper package with current v1.10 logistic and Planck diagnostics,
2. run modest real training suites in separated regimes,
3. add one-variable ablations and scoped baseline diagnostics,
4. generate deterministic paper figures from machine-readable tables,
5. audit the final package so unsupported and non-blind evidence cannot be overclaimed.

## Key Decisions

- Keep the existing `benchmark.py -> campaign.py -> raw_hybrid_paper.py` evidence flow. Do not build a parallel paper evidence system.
- Add only small, local helpers for paper assets and optional baseline diagnostics. Avoid PySR, notebooks, dashboards, broad external benchmark infrastructure, Rust, CUDA, pandas, and seaborn for this milestone.
- Treat Matplotlib as optional paper tooling only if needed; deterministic hand-written SVGs remain acceptable and avoid runtime dependency churn.
- Keep logistic and Planck as unsupported diagnostics unless a new strict-gate, verifier-owned artifact actually passes. Compiler shortening is evidence, not recovery.
- Keep pure blind, scaffolded, warm-start, same-AST, repair, refit, compile-only, and perturbed-basin rows separated in every table and figure.
- Run real training where it answers a bounded question, not as open-ended compute. All runs must record budgets, seeds, start mode, verifier status, and failure class.

## Recommended Phase Shape

| Phase | Name | Purpose |
|-------|------|---------|
| 59 | Evidence Contracts and Source Locks | Define v1.11 claim schema, source inventory, suite plan, output roots, and source-lock rules before running new evidence. |
| 60 | Claim-Safe Training Campaigns | Run current-code training in shallow pure-blind, scaffolded, warm-start/same-AST, perturbed-basin, and focused logistic/Planck probe regimes. |
| 61 | Ablation and Baseline Diagnostics | Generate motif-depth, warm-start-versus-blind, repair/refit, and lightweight conventional baseline diagnostics with explicit limitations. |
| 62 | Paper Figure and Table Pipeline | Derive plot-ready CSV/JSON tables and deterministic SVG figures from locked evidence artifacts. |
| 63 | Paper Package Assembly and Claim Audit | Assemble `artifacts/paper/v1.11/`, lock sources, regenerate scientific-law rows, and audit claims against the evidence ledger. |

## Paper-Useful Figures

- Regime recovery by evidence class.
- Blind versus perturbed depth degradation.
- Scientific-law support matrix with unsupported logistic/Planck near-gate diagnostics visible.
- Motif depth and node deltas for reusable compiler templates.
- Training outcome/failure taxonomy.
- Loss/snap/verifier lifecycle diagnostics.
- Scoped baseline diagnostic comparison, clearly labeled as prediction-only or unavailable where applicable.

## Main Risks

- Mixing non-blind evidence into blind recovery rates.
- Promoting logistic or Planck from relaxed compile depth alone.
- Cherry-picking seeds or showing only best runs.
- Letting figure polish hide unsupported rows and negative diagnostics.
- Running broad, weak external baselines that create more credibility risk than value.

## Execution Rule

Every generated paper artifact must have a machine-readable source table, a source-lock entry, and a claim-class label. Recovery rates must come from verifier-owned evidence fields, never from loss thresholds.
