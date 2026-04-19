# Phase 66: Paper-Facing Figures, Captions, and Negative Results - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning
**Mode:** Auto-generated smart discuss for autonomous execution

<domain>
## Phase Boundary

Add paper-facing captions, motif evolution artifacts, a visual pipeline figure, and an explicit logistic/Planck negative-results table under the v1.11 draft package.

</domain>

<decisions>
## Implementation Decisions

### Paper Artifacts
- Keep all new paper-facing outputs under `artifacts/paper/v1.11/draft/`.
- Use the existing v1.11 motif diagnostics and scientific-law table as the source of motif before/after values.
- Use the v1.11 logistic/Planck probe aggregate plus scientific-law rows for the negative-results table.
- Include Phase 65 refresh artifacts in captions where relevant, but do not merge them into v1.11 denominators silently.

### Visual Figure
- Generate a deterministic SVG pipeline figure as a source-controlled artifact.
- Include adjacent metadata with source paths and claim boundaries.
- Keep the figure functional and diagrammatic: data -> soft complete EML tree -> snap -> candidate pool/repair/refit -> verifier.

### Claim Honesty
- State `promotion: no` for logistic and Planck unless strict support and verifier recovery pass.
- Note Planck depth-convention differences explicitly: v1.11 diagnostic framing uses 24 -> 14, while older relaxed references used 20.
- Captions should describe what the artifacts support, not overclaim recovery.

### the agent's Discretion
- Choose Markdown/JSON/CSV table names and SVG layout details.
- Add a CLI command so artifacts are reproducible.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `artifacts/diagnostics/v1.11-paper-ablations/motif-depth-deltas.json` contains motif before/after rows.
- `artifacts/paper/v1.11/raw-hybrid/scientific-law-table.json` contains support and unsupported law rows.
- `artifacts/campaigns/v1.11-logistic-planck-probes/aggregate.json` contains negative probe outcomes.
- `paper_v112.py` already writes draft and refresh artifacts.

### Established Patterns
- Existing artifact generators write JSON, CSV, Markdown, manifest, and metadata sidecars.
- SVGs in `paper_assets.py` are deterministic plain-text outputs.

### Integration Points
- Extend `paper_v112.py` with paper-facing asset generation.
- Add a `paper-figures` CLI command.
- Add tests for motif rows, negative rows, pipeline SVG, captions, and CLI registration.

</code_context>

<specifics>
## Specific Ideas

- Add `figure-captions.md` and `table-captions.md`.
- Add `tables/motif-library-evolution.*`.
- Add `tables/logistic-planck-negative-results.*`.
- Add `figures/pipeline.svg` and `figures/pipeline.metadata.json`.

</specifics>

<deferred>
## Deferred Ideas

- Source-locking and final audit coverage are Phase 68.
- Optional baseline and strict logistic probe outcomes are Phase 67.

</deferred>
