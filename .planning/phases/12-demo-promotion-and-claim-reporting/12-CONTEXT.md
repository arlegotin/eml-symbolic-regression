# Phase 12: Demo Promotion and Claim Reporting - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Expose compiler and warm-start demo stages in CLI reports while separating catalog, compiled seed, warm-start attempt, trained exact recovery, and unsupported statuses.

</domain>

<decisions>
## Implementation Decisions

### Reporting
- `--train-eml` remains a blind baseline.
- `--compile-eml` is compile-only.
- `--warm-start-eml` is compiler-seeded training.
- Top-level `claim_status` promotes only when trained exact recovery verifies.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Demo specs already expose source SymPy expressions via candidates.

### Established Patterns
- JSON reports are deterministic artifacts.

### Integration Points
- CLI writes stage statuses and demo artifacts.

</code_context>

<specifics>
## Specific Ideas

Beer-Lambert should promote to recovered. Michaelis-Menten and Planck should report unsupported under default gates.

</specifics>

<deferred>
## Deferred Ideas

Guaranteed Planck trained recovery.

</deferred>
