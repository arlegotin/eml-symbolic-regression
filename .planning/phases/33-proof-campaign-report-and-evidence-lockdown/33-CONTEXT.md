# Phase 33: Proof Campaign Report and Evidence Lockdown - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, prior proof phases, and the new depth-curve/campaign contracts

<domain>
## Phase Boundary

Phase 33 assembles the full v1.5 proof bundle. It must take the Phase 29 claim contract, the Phase 30 shallow split, the Phase 31 perturbed basin evidence, and the Phase 32 measured depth curve, then produce one command that writes raw runs, aggregate files, plots, and a Markdown proof report under a stable proof root.

The report must be honest about denominators. Bounded proof suites, measured blind boundaries, probe diagnostics, and older v1.4 showcase campaigns cannot be blended into one recovery number.

</domain>

<decisions>
## Implementation Decisions

- **D-01:** The proof bundle root is `artifacts/proof/v1.5/`.
- **D-02:** The bundle runs a fixed campaign preset set covering shallow pure-blind, shallow scaffolded proof, perturbed basin, basin probes, and the measured depth curve.
- **D-03:** The proof report must include passed/bounded/failed/out-of-scope claim language with links back to campaign reports and raw run roots.
- **D-04:** v1.4 baseline context is comparative only; its denominators stay separate from v1.5 proof claims.
- **D-05:** The milestone is not complete until the proof bundle is generated reproducibly and the report/tests lock the workflow.

</decisions>

<specifics>
## Specific Ideas

- The proof bundle should write a machine-readable `proof-campaign.json` manifest and a human-readable `proof-report.md`.
- The perturbed basin bound report from Phase 31 should be preserved inside the final proof root rather than rewritten from scratch.
- README reproduction commands should point directly at the proof bundle root so future reruns are obvious.

</specifics>

<canonical_refs>
## Canonical References

- `.planning/REQUIREMENTS.md` - EVID-01 through EVID-05.
- `.planning/ROADMAP.md` - Phase 33 goal and success criteria.
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-VERIFICATION.md`
- `.planning/phases/30-bounded-shallow-blind-training-recovery/30-VERIFICATION.md`
- `.planning/phases/31-perturbed-basin-training-and-local-repair/31-VERIFICATION.md`
- `.planning/phases/32-paper-depth-curve-training-evidence/32-VERIFICATION.md`
- `src/eml_symbolic_regression/campaign.py`
- `src/eml_symbolic_regression/proof.py`
- `src/eml_symbolic_regression/cli.py`
- `README.md`

</canonical_refs>

<code_context>
## Existing Code Insights

- Campaign presets and reporting already exist and can be orchestrated instead of reimplemented.
- Phase 31 already produces a machine-readable basin-bound report that can be embedded in the proof bundle.
- Phase 32 already produces a campaign-ready depth curve, so this phase mainly needs orchestration, aggregation, and workflow lockdown.

</code_context>

<deferred>
## Deferred Ideas

- External noisy datasets and external symbolic-regression baselines remain out of scope after the proof bundle is complete.
- Starting a v1.6 milestone belongs after v1.5 is audited and marked shipped.

</deferred>

---

*Phase: 33-proof-campaign-report-and-evidence-lockdown*
*Context gathered: 2026-04-16*
