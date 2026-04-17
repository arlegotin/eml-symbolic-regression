# Phase 44: Centered-Family Smoke Triage and Full-Run Gate - Context

**Gathered:** 2026-04-17
**Status:** Ready for planning
**Mode:** Auto-selected defaults from `$gsd-autonomous`

<domain>
## Phase Boundary

Convert the current `family-smoke` signal into reproducible artifacts: a smoke campaign path, classification of centered failures and unsupported gates, focused `exp`/`log` calibration probes, and a go/no-go memo before larger family campaigns.

</domain>

<decisions>
## Implementation Decisions

### Evidence Discipline
- Use committed campaign and diagnostic artifacts as the source of truth, not console-only observations.
- Keep unsupported centered paths in denominators with reason codes.
- Classify raw baseline behavior separately from centered-family behavior.
- Do not launch expensive full campaigns until smoke and calibration artifacts say what evidence can be trusted.

### Triage Scope
- Classify centered blind failures as training/budget/operator behavior unless an explicit missing-integration reason is present.
- Classify centered warm-start unsupported rows as missing same-family seed support unless a verified centered seed exists.
- Treat Planck compile depth gates as accepted stretch-target exclusions, not centered-family evidence.
- Produce a memo that downstream phases can consume mechanically.

### the agent's Discretion
Implementation format, exact table shape, and helper module boundaries are at the agent's discretion, provided artifact paths are stable and reproducible.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `eml_symbolic_regression.campaign.run_campaign` already writes campaign manifests, aggregate JSON, CSVs, comparison Markdown, figures, and reports.
- `eml_symbolic_regression.benchmark` already records operator-family metadata for trained candidates.
- `artifacts/campaigns/v1.8-family-smoke-triage/` contains the current reproduced smoke output.

### Established Patterns
- Campaign presets are registry-driven and expose reproducibility commands in manifests.
- Failure/unsupported reasons flow through `aggregate.json`, `tables/failures.csv`, and report Markdown.
- GSD milestone evidence should be additive and must not overwrite archived v1.4-v1.7 anchors.

### Integration Points
- Add diagnostic helpers under `src/eml_symbolic_regression/`.
- Add CLI access through `diagnostics`.
- Add tests under `tests/` for triage payloads and artifact references.

</code_context>

<specifics>
## Specific Ideas

Use the reproduced smoke command:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign family-smoke --output-root artifacts/campaigns --label v1.8-family-smoke-triage --overwrite
```

</specifics>

<deferred>
## Deferred Ideas

Full raw-vs-centered campaign execution belongs to Phase 47 after integration gates and calibration artifacts are in place.

</deferred>
