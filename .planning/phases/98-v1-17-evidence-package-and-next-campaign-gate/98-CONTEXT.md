# Phase 98: v1.17 Evidence Package and Next-Campaign Gate - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Assemble the source-locked v1.17 answer from snap diagnostics, neighborhood candidates, verifier-first ranking, and the focused sandbox. Decide whether broader i*pi/GEML paper campaigns are justified while preserving the v1.16 final package unchanged.

</domain>

<decisions>
## Implementation Decisions

### Final Decision
- Allowed decisions are `exact_signal_found`, `still_inconclusive`, and `negative`.
- `exact_signal_found` requires the Phase 97 sandbox to find clean natural-family exact recovery signal.
- If no exact signal appears but diagnostics and candidate artifacts are source-locked, classify as `still_inconclusive` unless the evidence is explicitly negative.
- Larger campaigns remain blocked unless `exact_signal_found`.

### Package Boundary
- The v1.16 package is an immutable input; v1.17 comparison must be additive.
- Include manifests, before/after table references, source locks, failure taxonomy references, reproduction commands, and claim audit.
- Claim audit must reject loss-only recovery language and positive campaign claims without the exact-signal gate.

### the agent's Discretion
Implementation details are flexible if package outputs are deterministic, source-locked, and claim-safe.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 94-97 v1.17 writers expose manifests and source-lock files.
- v1.16 final package already uses manifest, final-decision, README, and claim-audit patterns.

### Established Patterns
- Package command should write JSON/Markdown artifacts and return non-zero only for failed audits.

### Integration Points
- Extend `paper_v117.py` with final package paths/writer/audit.
- Register `geml-v117-package` CLI.

</code_context>

<specifics>
## Specific Ideas

The README should say broader campaigns remain blocked unless the sandbox gate is `allow_next_campaign_planning`.

</specifics>

<deferred>
## Deferred Ideas

Any broader campaign is future work and only justified after this gate.

</deferred>
