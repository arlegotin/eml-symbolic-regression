# Phase 93: v1.16 Paper Decision Package and Claim Audit - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Assemble the final v1.16 paper decision package from the gate evaluation, pilot campaign, budget ladder, ablation assets, figure metadata, reproduction commands, and claim audit.

</domain>

<decisions>
## Implementation Decisions

### Final Decision
- Use the Phase 88 gate decision already materialized in `artifacts/paper/v1.16-geml/gate-evaluation.json`.
- The current result is `inconclusive`, so README and final guidance must explicitly block positive i*pi/GEML paper claims.
- Loss-only rows, negative controls, and incomplete denominators remain visible in the final package.

### Package Shape
- Write final decision artifacts under `artifacts/paper/v1.16-geml/final-decision/`.
- Write or refresh `artifacts/paper/v1.16-geml/README.md` as the human entry point.
- Source-lock package, campaign, ladder, ablation, figure, and reproduction inputs.

### Claim Audit
- Reuse the v1.16 claim-audit gate and add final-package checks for ablations, figures, reproduction, and negative-control visibility.
- The audit must fail if final text uses paper-positive language while the gate is not `paper_positive`.

</decisions>

<code_context>
## Existing Code Insights

- `paper_v116.py` already contains gate, claim-audit, source-lock, package, ladder, and ablation writers.
- `cli.py` has v1.16 commands grouped together.
- `tests/test_paper_v116.py` covers the focused v1.16 package behavior.

</code_context>

<specifics>
## Specific Ideas

Add `write_v116_final_decision_package` and a `geml-v116-final` CLI command. The writer should produce final decision JSON/Markdown, final claim audit JSON/Markdown, final source locks, a manifest, and package README.

</specifics>

<deferred>
## Deferred Ideas

Do not broaden the paper claim or rerun campaigns in Phase 93. This phase is packaging and audit only.

</deferred>
