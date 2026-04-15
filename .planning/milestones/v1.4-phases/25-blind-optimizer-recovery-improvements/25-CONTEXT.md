# Phase 25: Blind Optimizer Recovery Improvements - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase improves shallow blind recovery behavior without changing what `recovered` means. It may add generic optimizer initialization/scaffold strategies and comparison diagnostics, but verifier-owned recovery remains the only success contract.

</domain>

<decisions>
## Implementation Decisions

### Optimizer Scope
- Add generic paper-primitive scaffolds for blind optimization (`exp(variable)` and `log(variable)` when legal for the configured tree depth), not formula-specific target injection.
- Keep random restarts in place; scaffold attempts are additional candidate-generation attempts with explicit manifest provenance.
- Apply scaffolds only when no external initializer is supplied, so compiler warm starts keep their existing behavior.
- Do not promote a candidate based on soft loss or scaffold provenance; verification remains separate and unchanged.

### Comparison Evidence
- Compare v1.4 blind reruns against Phase 24's locked v1.3 baseline metrics.
- Report recovered, snapped-but-failed, soft loss, post-snap loss, snap margin, and verifier status per formula/seed.
- Treat radioactive decay remaining failures honestly because literal coefficients are still not handed to the blind terminal bank.

### the agent's Discretion
The exact manifest field names and helper function boundaries are at the agent's discretion, provided tests can distinguish scaffold attempts from random restarts and no verifier semantics are weakened.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `TrainingConfig` and `fit_eml_tree` in `optimize.py` centralize blind soft-tree training.
- `SoftEMLTree.force_exp` and `SoftEMLTree.force_log` already encode paper identities.
- `benchmark.py` already records training manifests and verifier-owned `claim_status`.
- Phase 24 diagnostics already produce locked v1.3 baseline metrics.

### Established Patterns
- Training manifests include per-restart logs with seeds, losses, anomalies, and initialization metadata.
- Benchmark status uses verifier-owned `claim_status` to classify blind recovery.

### Integration Points
- Add scaffold attempt provenance to optimizer manifests.
- Add blind comparison reporting in diagnostics so Phase 28 can reuse the same delta machinery.
- Add tests in optimizer and diagnostics coverage.

</code_context>

<specifics>
## Specific Ideas

Use generic primitive scaffolds because `exp` and `log` are paper-grounded shallow identities and the v1.3 blind failures show unstable snapping on exactly these formulas. Do not add radioactive-decay constants to the blind terminal bank in this phase.

</specifics>

<deferred>
## Deferred Ideas

Literal-constant blind discovery and broader discrete search are deferred until after v1.4 establishes whether generic primitive scaffolds and diagnostics improve the current campaign scoreboard.

</deferred>
