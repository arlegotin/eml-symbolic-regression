# Phase 95: Bounded Exact Neighborhood Generator - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Generate deterministic one-slot and two-slot exact alternatives around snapped candidates using Phase 94 low-margin diagnostics. This phase owns target-agnostic candidate enumeration and provenance. It does not rank candidates for promotion; Phase 96 owns verifier-first ranking.

</domain>

<decisions>
## Implementation Decisions

### Candidate Generation
- Use existing `master_tree.expand_snap_neighborhood()` semantics for replayable exact alternatives.
- Emit original snapped candidates and fallback candidates as explicit provenance rows before generated alternatives.
- Cap candidate growth with deterministic per-seed budget, beam width, max moves, and max slots.
- Stable ordering is part of the contract and must not depend on filesystem or dictionary iteration order.

### Leakage Boundary
- Candidate generation may read snapped ASTs, slot alternatives, operator family, variables, constants, and source candidate IDs.
- Candidate generation must not read target formula names as candidate templates, exact target trees, or hidden oracle simplification.
- Manifests must include `target_formula_leakage: false`.

### the agent's Discretion
Implementation details are flexible if the output remains deterministic, bounded, and source-lockable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/master_tree.py` already provides `expand_snap_neighborhood`, `slot_map_from_snap`, and replay helpers.
- `src/eml_symbolic_regression/expression.py` can parse serialized AST documents via `expr_from_document`.
- Phase 94 `paper_v117.py` writes `snap-neighborhood-seeds.json`.

### Established Patterns
- Package artifacts are written as JSON/CSV/Markdown plus source locks.
- Tests should use synthetic candidates and fixture directories rather than heavy optimizer runs.

### Integration Points
- Extend `paper_v117.py` with neighborhood path helpers and writer.
- Add CLI command for deterministic neighborhood generation.
- Add tests that reject target formula leakage fields.

</code_context>

<specifics>
## Specific Ideas

Keep Phase 95 usable even when a source artifact lacks serialized candidate ASTs: preserve original/fallback provenance rows and mark generated alternatives as zero for that seed rather than failing the package.

</specifics>

<deferred>
## Deferred Ideas

Verifier-owned ranking and promotion are Phase 96.

</deferred>
