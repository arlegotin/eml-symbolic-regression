# Phase 67: Bounded Baseline and Logistic Strict-Support Probes - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning
**Mode:** Auto-generated smart discuss for autonomous execution

<domain>
## Phase Boundary

Attempt two high-upside paper upgrades without making them milestone blockers: a locally bounded conventional symbolic-regression baseline status, and a logistic strict-support compiler probe.

</domain>

<decisions>
## Implementation Decisions

### Baseline Probe
- Check local Python modules only; do not install PySR or another SR package during this phase.
- If a conventional SR package is unavailable, write an explicit `unavailable` or `deferred` row with limitation text.
- If a package is available, keep the run diagnostic-only and outside EML recovery denominators.

### Logistic Strict-Support Probe
- Use the existing logistic demo expression and compiler diagnostics.
- Keep the strict gate at `max_depth=13`; do not relax the strict-support threshold.
- Record the strict result, relaxed result, macro hits, validation status, and promotion status.
- Logistic is promoted only if strict support and verifier-owned recovery evidence both pass; expected fail-closed outcome is still useful.

### the agent's Discretion
- Choose deterministic table names under `artifacts/paper/v1.11/draft/tables/`.
- Add a CLI command so the probe package is reproducible.
- Add focused tests that avoid dependency installation and avoid long training.

</decisions>

<code_context>
## Existing Code Insights

### Reusable APIs
- `get_demo("logistic")` provides the source expression and validation domains.
- `CompilerConfig`, `compile_and_validate`, and `diagnose_compile_expression` provide strict/relaxed compiler diagnostics.
- `paper_v112.py` already writes JSON/CSV/Markdown source tables and manifests.
- Phase 66 already writes negative-result rows under the draft package; Phase 67 should supplement rather than rewrite those rows.

### Existing Evidence
- v1.11 logistic diagnostics show strict depth exceeded at gate 13 and relaxed motif depth 15.
- The current motif hit for logistic is `exponential_saturation_template`.
- Logistic and Planck remain unsupported in `artifacts/paper/v1.11/raw-hybrid/scientific-law-table.json`.

</code_context>

<specifics>
## Specific Ideas

- Add `bounded-probes-manifest.json`.
- Add `tables/conventional-symbolic-baseline-probe.*`.
- Add `tables/logistic-strict-support-probe.*`.
- Include exact limitation text that baseline diagnostics are not EML recovery rows.

</specifics>

<deferred>
## Deferred Ideas

- Installing and tuning PySR or a Julia-backed baseline is beyond this bounded phase.
- Actual compiler work to shave logistic from depth 15 to 13 can be a future milestone if this probe confirms the remaining gap.

</deferred>
