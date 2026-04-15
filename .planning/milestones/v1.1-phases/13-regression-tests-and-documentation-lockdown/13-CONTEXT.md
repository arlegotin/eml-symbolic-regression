# Phase 13: Regression Tests and Documentation Lockdown - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Lock compiler, constant policy, embedding, warm-start, demo promotion, and documentation contracts with regression tests and public wording.

</domain>

<decisions>
## Implementation Decisions

### Tests and Docs
- Tests should cover positive and negative compiler behavior.
- Documentation must explain literal constants and warm-start provenance.
- Report wording must not imply blind discovery.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Existing pytest suite already covers semantics, master tree, optimizer, verifier, and CLI basics.

### Established Patterns
- README and implementation docs are concise and command-focused.

### Integration Points
- New tests live alongside existing pytest suite.

</code_context>

<specifics>
## Specific Ideas

Add CLI assertions for Beer-Lambert promotion and Michaelis-Menten unsupported depth.

</specifics>

<deferred>
## Deferred Ideas

No additional frontend/UI artifacts.

</deferred>
