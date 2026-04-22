# Phase 88: Paper-Strength Success Gate and Campaign Contract - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Define the paper-strength decision gate for v1.16 before optimizer/search changes can move the target. This phase produces machine-readable success criteria and campaign-denominator contracts for raw EML versus i*pi EML evidence.

</domain>

<decisions>
## Implementation Decisions

### Evidence Gate
- `paper_positive`, `promising_preliminary`, `negative`, and `inconclusive` must be explicit machine-readable outcomes.
- Verifier-gated trained exact recovery is the only positive recovery numerator.
- Loss-only improvements, same-AST seed returns, repaired candidates, compile-only rows, and unsupported rows remain diagnostic classes.
- The gate must fail closed when denominator completeness, negative-control discipline, source locks, or verifier-owned exact recovery are missing.

### Campaign Contract
- Matched raw/i*pi rows must share formula, seed, depth, budget, split, constants policy, snap rule, verifier gate, and resource metadata.
- Negative controls must remain visible and must block a positive i*pi claim if i*pi wins there.
- v1.16 should preserve v1.14/v1.15 accounting fields so public claim surfaces remain comparable.
- Contract outputs should be JSON plus Markdown for review and paper-package consumption.

### the agent's Discretion
Implementation can reuse `geml_package.py`, `campaign.py`, and existing benchmark manifests if the new v1.16 contract is source-locked and fail-closed.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/geml_package.py` already writes v1.15 claim-safe GEML package artifacts.
- `src/eml_symbolic_regression/campaign.py` already writes raw/i*pi paired comparison tables with branch and recovery diagnostics.
- `src/eml_symbolic_regression/benchmark.py` already defines v1.15 GEML target families and matched raw/i*pi suites.

### Established Patterns
- Paper-facing packages use deterministic JSON/CSV/Markdown artifacts plus source locks.
- Claim audits are pure Python functions with explicit checks and pytest coverage.
- Campaign rows distinguish trained exact recovery from loss-only and unsupported outcomes.

### Integration Points
- New contract artifacts should feed later package generation and tests without breaking the existing v1.15 package.

</code_context>

<specifics>
## Specific Ideas

Add a v1.16 paper-strength module that can be called by CLI/package code and tested with fixtures.

</specifics>

<deferred>
## Deferred Ideas

Optimizer/search changes belong to Phase 89; this phase only defines the gate and campaign contract.

</deferred>
