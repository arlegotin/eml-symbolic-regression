# Phase 94: Snap-Mismatch Diagnostics and Low-Margin Inventory - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Add source-locked diagnostics that explain where v1.16 soft/loss-only candidates fail after snapping. This phase exposes candidate snap probabilities, margins, alternatives, soft-versus-hard deltas, and branch/verifier diagnostics in campaign tables and deterministic manifests. It does not weaken verifier recovery definitions or promote loss-only rows.

</domain>

<decisions>
## Implementation Decisions

### Diagnostic Surface
- Campaign run and paired-comparison rows should expose selected and fallback candidate IDs, snap minimum margin, active node count, low-margin slot count, lowest-margin slots, and low-confidence alternatives.
- JSON-heavy fields should be deterministic compact JSON strings in CSV tables and structured arrays in JSON manifests.
- Snap mismatch classification should add explanatory fields without replacing the existing exact-recovery and loss-only accounting columns.
- Raw EML and i*pi EML rows must use the same diagnostic columns and source-lock rules.

### Manifest Boundary
- The manifest should seed later neighborhood search from failed, fallback, neutral, and loss-only rows only.
- Ordering should be deterministic by outcome priority, margin, formula, seed, and operator family.
- The manifest may point to candidate artifacts, but must not include target formula seeds or recognizers.
- v1.16 package artifacts remain read-only inputs.

### the agent's Discretion
Implementation details are at the agent's discretion as long as diagnostics are deterministic, verifier definitions stay unchanged, and the output can feed Phase 95.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/optimize.py` already stores `ExactCandidate.snap`, `lowest_margin_slots`, and `slot_alternatives`.
- `src/eml_symbolic_regression/benchmark.py` extracts run metrics from selected/fallback candidate manifests.
- `src/eml_symbolic_regression/campaign.py` writes run tables and GEML paired comparison tables.
- `src/eml_symbolic_regression/paper_v116.py` already writes budget ladder, taxonomy, source locks, and final package artifacts.

### Established Patterns
- Package modules write JSON, CSV, Markdown, source locks, and manifest files from deterministic path helpers.
- Recovery accounting is verifier-owned; loss-only and same-AST evidence classes remain separate.
- Tests use fixture campaign directories instead of expensive campaign reruns.

### Integration Points
- Extend campaign/benchmark table fields for diagnostics.
- Add v1.17 package helpers for snap-diagnostic manifests.
- Add CLI entry points after package helpers exist.

</code_context>

<specifics>
## Specific Ideas

Use `artifacts/campaigns/v1.16-geml-pilot` as the default source. The diagnostic layer should also work on fixture campaign directories created by tests.

</specifics>

<deferred>
## Deferred Ideas

Candidate neighborhood generation and verifier-first promotion are handled by Phases 95 and 96.

</deferred>
