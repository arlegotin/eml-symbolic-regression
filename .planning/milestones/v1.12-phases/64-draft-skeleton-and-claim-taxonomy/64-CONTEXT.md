# Phase 64: Draft Skeleton and Claim Taxonomy - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning
**Mode:** Auto-generated smart discuss for autonomous execution

<domain>
## Phase Boundary

Create the first paper-shaped draft scaffold inside `artifacts/paper/v1.11/draft/` and make claim taxonomy explicit before any refreshed evidence or new figures are added.

</domain>

<decisions>
## Implementation Decisions

### Draft Structure
- Use the requested `artifacts/paper/v1.11/draft/` root rather than a separate v1.12 paper root.
- Generate `abstract.md`, `methods.md`, `results.md`, and `limitations.md` as concise paper-section skeletons, not full manuscript prose.
- Root draft claims in existing v1.11 artifacts: `paper-readiness.md`, `claim-audit.json`, raw-hybrid claim ledger, scientific-law table, assets manifest, and source locks.
- Include placeholders for Phase 65 and Phase 66 additions so later phases can fill evidence-refresh and caption references without rewriting the skeleton.

### Claim Boundaries
- Treat pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed outcomes as separate evidence classes.
- Do not count loss-only rows, scaffolded starts, same-AST returns, warm starts, repair/refit outcomes, or perturbed true-tree basin returns as pure blind discovery.
- Keep logistic and Planck unsupported unless later strict compiler support and verifier recovery both pass.
- Use machine-readable taxonomy rows plus a Markdown table so the draft and audit can reference the same boundary definitions.

### the agent's Discretion
- Choose exact table columns, prose shape, and helper function names to match existing paper package style.
- Add a CLI command if that keeps draft generation reproducible and testable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/paper_package.py` assembles the v1.11 package and audits existing locked evidence.
- `src/eml_symbolic_regression/paper_assets.py` writes source tables, SVG figures, metadata, and source-lock style manifests.
- `artifacts/paper/v1.11/raw-hybrid/claim-ledger.json` already contains regime rows and safe public claim language.
- `artifacts/paper/v1.11/paper-readiness.md` contains the current evidence-position summary.

### Established Patterns
- Paper artifact writers return dataclass path bundles and write JSON with sorted keys.
- CLI commands are registered in `src/eml_symbolic_regression/cli.py`.
- Tests assert both command wiring and artifact contents.

### Integration Points
- Add draft-generation code near existing paper package modules.
- Add tests under `tests/` to verify generated draft files, taxonomy rows, and unsupported logistic/Planck language.

</code_context>

<specifics>
## Specific Ideas

- Draft skeleton must include abstract, methods, results, limitations, figure captions, and table captions eventually; this phase covers the section skeletons and taxonomy, while Phase 66 covers captions.
- The taxonomy table is a credibility artifact, not just documentation.

</specifics>

<deferred>
## Deferred Ideas

- Figure captions, table captions, motif evolution, pipeline figure, and negative-results table are Phase 66.
- Shallow/depth evidence refresh is Phase 65.
- Baseline and logistic strict-support probes are Phase 67.

</deferred>
