# Phase 35: Snap-Neighborhood Discrete Cleanup - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, Phase 34 outputs, current replay utilities, and the existing repair path

<domain>
## Phase Boundary

Phase 35 adds bounded target-free discrete cleanup around failed snapped candidates. The goal is to recover near misses by exploring low-margin alternatives and local exact-tree edits around the selected candidate from Phase 34, rather than trusting one slotwise argmax snap forever.

This phase must preserve the current selected exact candidate as fallback. It should improve the exact-candidate pool around ambiguous snaps, not change the verifier contract or introduce coefficient refit.

</domain>

<decisions>
## Implementation Decisions

- **D-01:** Discrete cleanup should operate on exact candidates produced by Phase 34, so the selected candidate and its legacy fallback remain first-class references throughout cleanup.
- **D-02:** `master_tree.py` should expose replayable slot alternatives and top-k categorical choices for ambiguous slots; phase logic should not reverse-engineer those choices from serialized top-1 snaps alone.
- **D-03:** The new cleanup path must be target-free. It may use candidate-local margins, replayable slot maps, subtree edits, and verifier-owned ranking, but it must not depend on known target ASTs or embedding assignments.
- **D-04:** Beam variants and local repairs should append new exact candidates with provenance and delta metadata rather than overwrite the original candidate in place.
- **D-05:** Reports must show what changed: which slots or subtrees were varied, their margins, and whether cleanup improved or failed relative to the preserved fallback candidate.

</decisions>

<specifics>
## Specific Ideas

- Use exact AST documents or stable serialized slot maps for deduplication before verifier work so bounded beam search does not waste time on duplicate trees.
- Start from low-margin active slots already exposed by Phase 34 and expand only a bounded number of alternatives per slot.
- Reuse the replay machinery in `repair.py`, but replace target-aware move generation with neighborhood moves derived from candidate-local alternatives and subtree toggles.

</specifics>

<canonical_refs>
## Canonical References

- `.planning/REQUIREMENTS.md` - DISC-01 through DISC-04.
- `.planning/ROADMAP.md` - Phase 35 goal and success criteria.
- `.planning/STATE.md` - Phase 34 completion and v1.6 fallback-preserving direction.
- `.planning/phases/34-exact-candidate-pool-and-checkpoint-snapping/34-01-SUMMARY.md`
- `.planning/phases/34-exact-candidate-pool-and-checkpoint-snapping/34-VERIFICATION.md`
- `src/eml_symbolic_regression/master_tree.py`
- `src/eml_symbolic_regression/optimize.py`
- `src/eml_symbolic_regression/repair.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/cli.py`

</canonical_refs>

<code_context>
## Existing Code Insights

- Phase 34 already serializes low-margin slot summaries and preserves the selected candidate plus explicit fallback candidate.
- `master_tree.py` knows the full categorical bank for each slot, but current public snapping only records the top-1 choice and margin.
- `repair.py` already provides slot-map replay and subtree replacement mechanics, but its move generator is target-aware and therefore not usable directly for this phase.
- `benchmark.py` is the right place to wire cleanup results into blind, warm-start, and perturbed-basin artifact/report paths once the target-free cleanup engine exists.

</code_context>

<deferred>
## Deferred Ideas

- Literal-constant refit and expanded anomaly logging remain Phase 36 work.
- Compiler macro shortening and warm-start coverage expansion remain Phase 37 work.
- Final evidence/report weak-dominance claims against archived baselines remain Phase 38 work.

</deferred>

---

*Phase: 35-snap-neighborhood-discrete-cleanup*
*Context gathered: 2026-04-16*
