# Phase 38: Hybrid Recovery Evaluation and Regression Lockdown - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, phase 37 outputs, proof/campaign reporters, and diagnostics comparison tooling

<domain>
## Phase Boundary

Phase 38 should lock the milestone's scientific reporting layer. The hybrid pipeline now has exact-candidate pooling, target-free cleanup, post-snap refit, and audited compiler shortening. The remaining work is to make proof and campaign reports summarize those regimes honestly, preserve immutable anchors for archived evidence, and add regression tests that fail if hybrid-stage metadata or fallback-safe behavior disappears from the reported evidence surface.

</domain>

<decisions>
## Implementation Decisions

- **D-01:** Keep proof, blind, warm-start, compile-only, and perturbed-basin regimes visibly separate at the top level of proof/campaign bundles instead of relying only on scattered narrative text.
- **D-02:** Generalize campaign comparison outputs so they are not hardcoded to `v1.4` versus `v1.3`; labels and reproduction commands should derive from the provided directories.
- **D-03:** Preserve immutable lock manifests for archived anchors used in comparisons or proof bundles so future reruns can prove which baseline files were compared.
- **D-04:** Fix proof-claim verdict labeling so measured `reported` thresholds remain `reported` rather than being mislabeled as `bounded`.
- **D-05:** Add regression tests that lock hybrid-stage reporting fields such as selection, fallback, and refit metrics at the aggregate/report level.

</decisions>

<specifics>
## Specific Ideas

- Add a regime summary table to `campaign.py` reports and to `proof_campaign.py` proof bundles.
- Extend proof/campaign manifests with baseline or anchor lock sections using file hashes for archived comparison roots.
- Make diagnostics comparison markdown, JSON metadata, and CLI defaults use version-agnostic labels/output locations.
- Add a small aggregate/report regression test that asserts emitted run metrics preserve selected/fallback/refit fields needed to audit weak-dominance claims.
- Update README reproduction guidance so the comparison and proof-bundle commands match the new generic reporting surface.

</specifics>

<canonical_refs>
## Canonical References

- `.planning/REQUIREMENTS.md` - EVAL-01, EVAL-02, EVAL-03, EVAL-04.
- `.planning/ROADMAP.md` - Phase 38 goal and success criteria.
- `.planning/STATE.md` - Phase 37 completion and current milestone position.
- `.planning/phases/37-compiler-macro-shortening-and-warm-start-coverage/37-01-SUMMARY.md`
- `.planning/phases/37-compiler-macro-shortening-and-warm-start-coverage/37-VERIFICATION.md`
- `src/eml_symbolic_regression/campaign.py`
- `src/eml_symbolic_regression/diagnostics.py`
- `src/eml_symbolic_regression/proof_campaign.py`
- `README.md`
- `tests/test_proof_campaign.py`
- `tests/test_diagnostics.py`
- `tests/test_benchmark_reports.py`

</canonical_refs>

<code_context>
## Existing Code Insights

- Campaign reports already summarize headline counts and proof-threshold tables, but they do not expose a dedicated top-level regime summary.
- Diagnostics comparison tooling is structurally generic but still hardcodes `v1.4`/`v1.3` wording and default output paths.
- Proof bundles already ingest archived v1.4 campaign directories, but they do not emit immutable anchor-lock manifests for those comparison roots.
- Aggregate run metrics already expose selected/fallback/refit fields in `benchmark.py`, but there is no dedicated regression test that locks those fields at the reporting layer.

</code_context>

<deferred>
## Deferred Ideas

- Full new milestone proof/campaign reruns are downstream of this infrastructure work; Phase 38 should build the reporting and regression surface without claiming fresh empirical results yet.
- External baseline comparisons remain out of scope until after v1.6 ships.

</deferred>

---

*Phase: 38-hybrid-recovery-evaluation-and-regression-lockdown*
*Context gathered: 2026-04-16*
