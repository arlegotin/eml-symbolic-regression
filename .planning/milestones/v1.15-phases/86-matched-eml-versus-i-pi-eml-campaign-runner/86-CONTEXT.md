# Phase 86: Matched EML versus i*pi EML Campaign Runner - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning
**Mode:** Smart discuss auto-defaults

<domain>
## Phase Boundary

Phase 86 turns the Phase 85 matched benchmark protocol into paired evidence artifacts. The existing campaign runner should remain the execution path; this phase adds the paired raw EML versus i*pi EML layer and ensures Phase 84 metrics survive into aggregate tables.

In scope:

- Preserve the existing `run_campaign("geml-oscillatory*")` command path.
- Emit pairwise rows for each declared formula and seed, comparing raw EML against i*pi EML.
- Include verifier-gated trained recovery, pre-snap and post-snap loss, gradient stats, anomaly counts, branch counts, timing, and resource metadata.
- Preserve v1.14 accounting fields: `verification_outcome`, `evidence_regime`, `discovery_class`, `warm_start_evidence`, and `ast_return_status`.

Out of scope:

- Running a full expensive campaign by default.
- Interpreting wins/losses as claim language; Phase 87 owns the final decision package and claim boundary.
</domain>

<decisions>
## Implementation Decisions

- Add paired tables to `write_campaign_tables()` rather than creating a separate runner.
- Keep pair keys conservative: formula, seed, start mode, training mode, depth, and constants policy.
- Treat recovery as verifier-gated trained exact recovery, not low loss.
- Use existing run artifacts for runtime where available; use optimizer manifest wall-clock as an additional metric.
- Always write paired artifacts, even if empty, so downstream Phase 87 packaging can rely on stable paths.
</decisions>

<code_context>
## Existing Code Insights

- `benchmark.py` already computes v1.14 accounting fields and stores `metrics` in every run payload.
- Phase 84 added optimizer-level `pre_snap_mse`, gradient summaries, branch trace counts, and optimizer timing, but `_extract_run_metrics()` needs to expose them.
- `campaign.py` already writes raw run CSVs, operator-family recovery/diagnostic CSVs, markdown comparison, and source-lock JSON.
- `tests/test_campaign.py` has table-writing tests using synthetic aggregate payloads; this is the right place to add paired artifact tests.
</code_context>

<specifics>
## Specific Ideas

- Add `geml-paired-comparison.csv`, `geml-paired-summary.json`, and `geml-paired-comparison.md`.
- Add `pre_snap_mse`, `post_snap_mse`, gradient maxima, branch proximity/crossing counts, and optimizer wall-clock columns to run CSV output.
- Add summary counts for i*pi wins, raw wins, both recovered, neither recovered, and negative-control pairs.
</specifics>

<deferred>
## Deferred Ideas

- Full evidence interpretation and claim audit are deferred to Phase 87.
</deferred>
