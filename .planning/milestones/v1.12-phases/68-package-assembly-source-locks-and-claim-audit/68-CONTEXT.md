# Phase 68: Package Assembly, Source Locks, and Claim Audit - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning
**Mode:** Auto-generated smart discuss for autonomous execution

<domain>
## Phase Boundary

Assemble a v1.12 supplement to the v1.11 paper package, source-lock all new draft/evidence/probe artifacts, and audit that paper-facing claims remain source-backed and regime-separated.

</domain>

<decisions>
## Implementation Decisions

### Supplement Location
- Keep the immutable v1.11 package intact.
- Add a v1.12 supplement under `artifacts/paper/v1.11/v1.12-supplement/`.
- The supplement may reference `artifacts/paper/v1.11/draft/` and `artifacts/campaigns/v1.12-evidence-refresh/` rather than copying every large run artifact.

### Source Locks
- Source-lock draft sections, claim taxonomy, captions, paper-facing tables, pipeline figure, refresh summaries, bounded probes, and manifests.
- Include SHA-256 hashes, bytes, role, source path, and supplement path for every locked file.
- Lock the compact tables and manifests needed to regenerate the paper argument; avoid duplicating large run payloads unless needed for claim audit.

### Audit
- Check draft sections exist.
- Check claim taxonomy includes all evidence regimes.
- Check shallow refresh has 10 rows with 5 pure-blind and 5 scaffolded rows.
- Check depth refresh covers depths 2-5 with at least two rows per depth.
- Check logistic/Planck negative rows retain `promotion: no`.
- Check bounded probes record baseline status and logistic `promotion: no`.
- Check every v1.12 artifact family has source locks.

### the agent's Discretion
- Choose supplement filenames and exact audit check names.
- Add CLI wiring for deterministic regeneration.
- Add focused tests against temporary output directories.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Patterns
- `paper_package.py` already has package/audit/source-lock patterns for v1.11.
- `paper_v112.py` has helpers for JSON/CSV/Markdown table writing and SHA-256 source locks.
- The v1.12 draft root now contains draft sections, taxonomy, captions, motif/negative tables, pipeline assets, and bounded probes.
- The v1.12 evidence refresh root contains compact shallow/depth tables plus aggregate manifests.

### Integration Points
- Extend `paper_v112.py` with a supplement writer and claim audit.
- Add a `paper-supplement` CLI command.
- Add tests in `tests/test_paper_v112.py`.

</code_context>

<specifics>
## Specific Ideas

- Add `artifacts/paper/v1.11/v1.12-supplement/manifest.json`.
- Add `source-locks.json`.
- Add `claim-audit.json` and `claim-audit.md`.
- Add `reproduction.md`.

</specifics>

<deferred>
## Deferred Ideas

- Full manuscript prose expansion is a future manuscript-polish milestone.
- Matched-budget external symbolic-regression comparison is a future baseline milestone.

</deferred>
