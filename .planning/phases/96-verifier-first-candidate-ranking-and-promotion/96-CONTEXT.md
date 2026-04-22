# Phase 96: Verifier-First Candidate Ranking and Promotion - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Make exact verifier status the first-class promotion rule for every Phase 95 candidate pool. This phase ranks and explains candidate selection; it does not broaden campaign scope or count loss-only rows as recovery.

</domain>

<decisions>
## Implementation Decisions

### Promotion Rule
- `recovered` and verified-equivalent statuses rank above every lower-loss failed candidate.
- Post-snap loss is diagnostic after verifier status, symbolic/equivalence evidence, and held-out/high-precision evidence.
- The ranking output must explain the winner and why lower-loss candidates were rejected.
- Pending/unverified rows cannot be promoted.

### Accounting Boundary
- Keep exact recovery, verified equivalence, repair-only, loss-only, compile-only, same-AST, fallback, and original-snap classes separate.
- The original snapped candidate and fallback candidate remain visible even when a neighborhood candidate wins.
- Ranking artifacts must be deterministic and source-lockable.

### the agent's Discretion
Implementation details are flexible if the verifier-first ordering and accounting separation are explicit and test-covered.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `optimize.py` already uses verifier status in `_candidate_ranking_key`.
- Phase 95 `neighborhood-candidates.json` provides candidate provenance and pending verifier status fields.
- v1.16 package code already separates loss-only evidence from exact recovery.

### Established Patterns
- Manifest writers emit JSON/CSV/Markdown and source locks.
- Tests should use small candidate-row fixtures to prove ranking semantics.

### Integration Points
- Extend `paper_v117.py` with ranking paths and writer.
- Add CLI command for ranking generated candidate pools.

</code_context>

<specifics>
## Specific Ideas

Ranking should remain useful if all rows are pending/failed: produce a `no_verified_candidate` winner state rather than fabricating a recovery.

</specifics>

<deferred>
## Deferred Ideas

Phase 97 runs the focused sandbox/gate using the ranking output.

</deferred>
