# Phase 34: Exact Candidate Pool and Checkpoint Snapping - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, requirements, current optimizer/verifier code, and v1.5 proof constraints

<domain>
## Phase Boundary

Phase 34 upgrades training from "pick the restart with the lowest soft loss, then snap once" to "emit and rank an exact-candidate pool." The phase must add an explicit late hardening stage, preserve exact snaps from restarts and hardening checkpoints, and let verifier-owned ranking choose the final exact tree while keeping the old soft-loss selector available as a fallback reference.

This phase is about candidate generation, provenance, and exact-candidate selection. It is not yet the phase for neighborhood beam search, target-free repair, post-snap refit, or compiler shortening.

</domain>

<decisions>
## Implementation Decisions

- **D-01:** `fit_eml_tree()` remains the central candidate-generation entry point for blind, warm-start, and perturbed-basin training, so the new pooling and selection behavior should live there rather than in one benchmark-only wrapper.
- **D-02:** The hardening stage should be explicit and late: finish the existing soft search first, then run a short lower-temperature sharpening window that can emit exact snaps at configured checkpoints without changing faithful verification semantics after snapping.
- **D-03:** Every emitted exact candidate should carry stable provenance: attempt kind, restart/seed, hardening or fallback source, checkpoint step, snap margins, active-node statistics, and post-snap training loss.
- **D-04:** Final exact-candidate selection should be verifier-gated when verification splits are available. Ranking order is: verifier outcome, extrapolation error, high-precision error, held-out error, post-snap train loss, complexity, then soft-loss tie-breaks.
- **D-05:** The legacy selector must remain serializable as an explicit fallback candidate so v1.6 can prove weak dominance over the v1.5 single-final-snap behavior.

</decisions>

<specifics>
## Specific Ideas

- Candidate IDs should be stable and human-readable so benchmark/campaign artifacts can say exactly which restart/checkpoint produced the winner.
- The selected candidate and the legacy fallback should both be visible in manifests without making downstream consumers relearn the entire artifact schema.
- Warm-start and perturbed-basin flows should inherit the new selector automatically once they route verification splits into `fit_eml_tree()`.

</specifics>

<canonical_refs>
## Canonical References

- `.planning/REQUIREMENTS.md` - HARD-01 through HARD-04.
- `.planning/ROADMAP.md` - Phase 34 goal and success criteria.
- `.planning/STATE.md` - v1.6 weak-dominance and fallback-preservation direction.
- `sources/NORTH_STAR.md` - hardening/discretization and verifier-first recovery contract.
- `docs/IMPLEMENTATION.md` - current architecture and recovery contract.
- `src/eml_symbolic_regression/optimize.py`
- `src/eml_symbolic_regression/master_tree.py`
- `src/eml_symbolic_regression/verify.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/warm_start.py`
- `src/eml_symbolic_regression/basin.py`
- `src/eml_symbolic_regression/cli.py`

</canonical_refs>

<code_context>
## Existing Code Insights

- The current optimizer records restart provenance but keeps only one winning restart and one final snap.
- `SnapResult` already exposes per-slot probabilities, margins, and active-node counts, which can seed the candidate provenance required by this phase.
- Benchmark and campaign reports already extract metrics from `trained_eml_candidate`, so the new selector should extend that manifest rather than replace it with a disconnected artifact format.
- Warm-start and perturbed-basin training both already pass through `fit_eml_tree()`, making it practical to add exact-candidate pooling once at the optimizer layer.

</code_context>

<deferred>
## Deferred Ideas

- Low-margin beam expansion and target-free local repair belong to Phase 35.
- Literal-constant refit and expanded domain/numerical controls belong to Phase 36.
- Compiler macro shortening and warm-start coverage expansion belong to Phase 37.

</deferred>

---

*Phase: 34-exact-candidate-pool-and-checkpoint-snapping*
*Context gathered: 2026-04-16*
