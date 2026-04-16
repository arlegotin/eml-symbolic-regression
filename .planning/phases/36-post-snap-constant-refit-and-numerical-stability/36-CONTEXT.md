# Phase 36: Post-Snap Constant Refit and Numerical Stability - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, Phase 35 outputs, current anomaly stats, and exact-candidate artifact contracts

<domain>
## Phase Boundary

Phase 36 adds a post-snap numerical stage on top of the exact-candidate and cleanup pipeline. The goal is to improve structurally correct exact candidates by refitting literal constants after discrete structure is frozen, while also making training-time `exp` and `log` failures more observable and optionally penalizing unsafe log-feeding branches.

This phase must preserve the current selected exact candidate and any cleanup-promoted candidate as fallback references. Refit can only promote a new exact candidate when verifier-owned ranking improves or matches the preserved fallback. Numerical controls must remain training-only and must not change faithful verification semantics after snapping.

</domain>

<decisions>
## Implementation Decisions

- **D-01:** Post-snap refit should operate on exact `Expr` trees, not soft logits, so discrete structure remains frozen throughout refit.
- **D-02:** Refit artifacts must keep both the pre-refit candidate and the post-refit candidate, with explicit accept/reject provenance tied back to the preserved fallback candidate from earlier phases.
- **D-03:** Numerical diagnostics should extend the existing `AnomalyStats` contract rather than invent a disconnected reporting channel, so optimizer restart logs and benchmark artifacts stay comparable.
- **D-04:** Positive-domain-safe log controls should be optional training-time penalties or parameterizations; verification and final exact evaluation must stay faithful to canonical EML semantics.
- **D-05:** Blind, warm-start, and perturbed-basin paths should share the same refit acceptance contract so Phase 38 can compare weak-dominance honestly across start modes.

</decisions>

<specifics>
## Specific Ideas

- Build a frozen exact-expression refit helper that replaces literal constants with trainable torch parameters, optimizes only those parameters against the training split, then snaps back to an exact `Expr`.
- Treat only user-meaningful literal constants as refittable at first; keep the canonical `1` basis constant fixed unless a clear justification emerges.
- Extend anomaly stats to expose `exp` real-part excursions, `log` small-magnitude or non-positive-real counts, and node-level summaries so benchmark artifacts can explain numerical failures better than a raw clamp count.
- Add an optional penalty for log inputs that drift toward unsafe real-domain regions on real-valued demos, but keep it disabled by default and clearly marked as training-only.

</specifics>

<canonical_refs>
## Canonical References

- `.planning/REQUIREMENTS.md` - REFI-01, REFI-02, STAB-01, STAB-02.
- `.planning/ROADMAP.md` - Phase 36 goal and success criteria.
- `.planning/STATE.md` - Phase 35 completion and fallback-preserving cleanup direction.
- `.planning/phases/35-snap-neighborhood-discrete-cleanup/35-01-SUMMARY.md`
- `.planning/phases/35-snap-neighborhood-discrete-cleanup/35-VERIFICATION.md`
- `src/eml_symbolic_regression/expression.py`
- `src/eml_symbolic_regression/semantics.py`
- `src/eml_symbolic_regression/optimize.py`
- `src/eml_symbolic_regression/repair.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/warm_start.py`
- `src/eml_symbolic_regression/basin.py`

</canonical_refs>

<code_context>
## Existing Code Insights

- Exact candidates and repaired candidates are now serialized with stable AST documents, selected/fallback provenance, and verifier-owned ranking data.
- `AnomalyStats` already records NaN/Inf counts, clamp counts, `max_abs`, and `max_exp_real`, but it does not yet distinguish `log`-domain stress or other branch-level failure modes.
- The benchmark runner already has a consistent place to preserve fallback candidates and append repair metadata, making it the natural place to append refit metadata as well.
- Literal constants already flow through compiler output, terminal banks, and exact AST serialization, so a frozen-structure refit step can reuse those existing representations.

</code_context>

<deferred>
## Deferred Ideas

- Compiler short-macro shortening and wider warm-start coverage remain Phase 37 work.
- Final weak-dominance evidence reruns and milestone regression lockdown remain Phase 38 work.

</deferred>

---

*Phase: 36-post-snap-constant-refit-and-numerical-stability*
*Context gathered: 2026-04-16*
