# Phase 97: Focused v1.17 Natural-Bias Recovery Sandbox - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Run the smallest useful v1.17 decision gate over Phase 96 ranked candidates. This phase determines whether the snap-first workflow produced at least one natural-family verifier-gated exact recovery signal. If exact signal is absent, broader pilot/full campaigns remain blocked.

</domain>

<decisions>
## Implementation Decisions

### Sandbox Gate
- Use the ranking output as the source of truth for candidate status.
- Treat negative controls as visible and claim-blocking, not discardable.
- Require at least one natural-family `exact_recovery` row to open the next campaign planning gate.
- Preserve matched raw/i*pi visibility through operator-family counts.

### Output
- Emit JSON/CSV/Markdown sandbox artifacts with exact signal counts, operator-family rows, negative-control rows, and a broader-campaign gate.
- The sandbox may be negative or inconclusive; that is an acceptable result.

### the agent's Discretion
Implementation details are flexible as long as the gate is deterministic and fail-closed.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 96 ranking artifacts already classify exact recovery versus loss-only/fallback/original rows.
- v1.16 package code uses fail-closed gate language and negative-control visibility.

### Established Patterns
- Artifact writers should include source locks and reproduction-friendly CLI commands.

### Integration Points
- Extend `paper_v117.py` with sandbox paths and writer.
- Register `geml-v117-sandbox` CLI.

</code_context>

<specifics>
## Specific Ideas

Use `target_family != negative_control` as the natural-family exact-signal denominator.

</specifics>

<deferred>
## Deferred Ideas

The final evidence package and next-campaign decision are Phase 98.

</deferred>
