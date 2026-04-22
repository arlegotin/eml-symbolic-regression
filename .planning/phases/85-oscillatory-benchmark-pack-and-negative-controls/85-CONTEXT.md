# Phase 85: Oscillatory Benchmark Pack and Negative Controls - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning
**Mode:** Smart discuss auto-defaults

<domain>
## Phase Boundary

The comparison suite should test i*pi EML on targets where its phase-biased structure plausibly helps, and on controls where it should not be expected to help.

In scope:

- Register normalized safe-domain periodic, harmonic, damped oscillation, standing-wave, and log-periodic targets.
- Register negative controls for exp, log, polynomial, and rational targets.
- Add benchmark suite manifests that pair raw EML and i*pi EML with matched depths, optimizer settings, initialization budgets, snapping rules, verifier gates, and split policies.
- Add suite validation that fails closed for i*pi rows without an explicit safe branch-domain declaration.

Out of scope:

- Executing the full matched campaign and aggregating results. That is Phase 86.
- Claiming i*pi superiority from manifest registration alone. That is Phase 87 after evidence exists.
</domain>

<decisions>
## Implementation Decisions

- Use existing `DemoSpec` and `BenchmarkSuite` registries rather than adding a separate manifest format.
- Use `blind` benchmark rows with scaffold initializers disabled for both operators so the raw and i*pi rows have the same initialization budget.
- Keep tree depths and step counts modest. The suite is a protocol declaration first; broad execution belongs to Phase 86.
- Represent branch safety as explicit tags plus validation against the demo domain. Missing declaration should raise `BenchmarkValidationError`.
- Use existing `EmlOperator` serialization for raw and i*pi budgets.
</decisions>

<code_context>
## Existing Code Insights

- `datasets.py` owns `DemoSpec`, `demo_specs()`, formula provenance, deterministic splits, and target mpmath callbacks.
- `benchmark.py` owns `BenchmarkCase`, `OptimizerBudget`, suite validation, built-in suite names, and suite construction helpers.
- Phase 84 already made `OptimizerBudget.operator_family` and optimizer manifests family-aware.
- Existing family suites clone raw/centered variants with helper functions; Phase 85 can add a smaller v1.15-specific paired suite.
</code_context>

<specifics>
## Specific Ideas

- New natural-bias targets:
  - `sin_pi`
  - `cos_pi`
  - `harmonic_sum`
  - `standing_wave_snapshot`
  - `log_periodic_oscillation`
  - existing `damped_oscillator`
- Negative controls:
  - existing `exp`
  - existing `log`
  - new `quadratic_polynomial`
  - new `rational_decay`
- Suite names:
  - `v1.15-geml-oscillatory`
  - optional `v1.15-geml-oscillatory-smoke` for a cheap validation/run subset.
</specifics>

<deferred>
## Deferred Ideas

- Multivariable standing-wave surfaces can be added later through `ExpandedDatasetSpec` if Phase 86 evidence suggests the univariate snapshot is too weak.
- Learned or searched `a` values remain out of scope for v1.15.
</deferred>
