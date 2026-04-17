# Phase 47: Full Family Evidence Campaigns - Context

**Gathered:** 2026-04-17
**Status:** Ready for planning
**Mode:** Auto-selected defaults from `$gsd-autonomous`

<domain>
## Phase Boundary

Execute or deliberately scope v1.8 family evidence campaigns based on the Phase 44/46 gate, preserving raw-vs-centered comparison artifacts and historical anchors.

</domain>

<decisions>
## Implementation Decisions

### Scope Gate
- Run enough v1.8 family evidence to support the paper decision, but avoid pretending known unsupported centered warm-starts are successful centered recovery.
- If a full campaign is scoped down, record the exact reason, filters, and artifact trail.
- Keep `family-showcase` skipped unless calibration or standard evidence shows a meaningful centered-family signal.
- Preserve all unsupported, failed, repair/refit, anomaly, and complexity rows in aggregate outputs.

### Evidence Outputs
- Produce a v1.8 evidence manifest that lists completed and deliberately scoped campaigns.
- Include regression-lock paths for all executed campaigns.
- Do not overwrite archived v1.4-v1.7 artifacts.

### the agent's Discretion
Choose local-budget-safe filters for large campaigns when the go/no-go memo indicates full execution would be low-information.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Campaign reports already include tables, figures, and operator-family locks.
- CLI filters can scope campaign execution by formula, case, start mode, seed, and perturbation noise.

### Established Patterns
- Campaign manifests store reproduction commands and filters.
- Negative evidence is accepted when reasons and artifacts are explicit.

### Integration Points
- `artifacts/campaigns/`
- `artifacts/diagnostics/v1.8-family-evidence/`
- `src/eml_symbolic_regression/family_triage.py`

</code_context>

<specifics>
## Specific Ideas

Run a scoped `family-standard` after calibration and record deliberate scope decisions for shallow, basin, depth-curve, and showcase paths if local budget or unsupported gates make full runs low-value.

</specifics>

<deferred>
## Deferred Ideas

Larger unfiltered family matrices can move to accelerated hardware after local contracts are stable.

</deferred>
