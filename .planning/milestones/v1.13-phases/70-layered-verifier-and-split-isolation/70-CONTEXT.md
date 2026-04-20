# Phase 70: Layered Verifier and Split Isolation - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase upgrades the verifier contract and split discipline without trying to solve all future formal methods. It should add reportable evidence layers, fresh non-selection probes, explicit certificate/unsupported statuses, and data-role labels while preserving existing benchmark and demo behavior.

</domain>

<decisions>
## Implementation Decisions

### Verifier Layers
- Keep the existing `verify_candidate` API backward compatible and add optional fields rather than replacing the report shape.
- Symbolic equivalence should be attempted when a target SymPy expression is provided; otherwise the report must say symbolic evidence is unsupported, not silently skip the layer.
- Dense randomized and adversarial probes should use fresh points from verifier-owned evaluators when available, and should report unsupported when the target evaluator/domain information is unavailable.
- Interval/certificate evidence can start as a conservative status field: symbolic equivalence can satisfy certificate-like evidence, while unsupported interval proof must be labeled explicitly.

### Split Roles
- Add split-role metadata while inferring roles from existing split names such as `train`, `heldout`, `extrap`, `selection`, and `final_confirmation`.
- Candidate ranking must ignore final-confirmation splits even when callers accidentally include them in `verification_splits`.
- Final confirmation checks can still appear in verifier reports after selection; they just cannot drive selection/ranking.
- Artifacts should expose metric role counts so later benchmark/report phases can separate training, selection, diagnostic, verifier, and final-confirmation metrics.

### Compatibility
- Existing demos, campaigns, warm starts, and paper package tests must continue to pass.
- New fields in `VerificationReport.as_dict()` should be additive and stable JSON-friendly.
- Use deterministic pseudo-random probes so tests are reproducible.
- Keep Phase 70 focused on verifier/reporting infrastructure; broader dataset expansion belongs to Phase 74.

### the agent's Discretion
The agent may choose helper names and exact dataclass shapes, provided they preserve existing callers, make unsupported evidence explicit, and add tests covering symbolic pass, placeholder unsupported/certificate statuses, fresh probe behavior, and final-confirmation exclusion from candidate ranking.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/verify.py` defines `DataSplit`, `SplitResult`, `VerificationReport`, and `verify_candidate`.
- `src/eml_symbolic_regression/optimize.py` ranks exact candidates in `_select_exact_candidate` using `VerificationReport` metrics.
- `src/eml_symbolic_regression/benchmark.py` serializes verifier reports into run artifacts and aggregate metrics.
- `tests/test_verify.py`, `tests/test_benchmark_reports.py`, and compiler/warm-start tests cover existing verifier and evidence taxonomy behavior.

### Established Patterns
- Reports are dataclasses with `as_dict()` methods and string statuses.
- Evidence upgrades are normally additive and claim-safe rather than broad rewrites.
- Tests prefer deterministic small datasets and direct report assertions.

### Integration Points
- Add role/evidence fields in `verify.py`.
- Use split filtering in `optimize.py` before candidate ranking.
- Add focused verifier-layer tests before broad benchmark integration.

</code_context>

<specifics>
## Specific Ideas

- Add `target_sympy` and `target_mpmath`-based probe support to `verify_candidate`.
- Add `role` to `DataSplit` with fallback role inference by split name.
- Add helper functions such as `split_role`, `selection_candidate_splits`, and `metric_role_counts`.

</specifics>

<deferred>
## Deferred Ideas

- Full interval arithmetic over all supported elementary operators is deferred; Phase 70 should label unsupported certificate status explicitly.
- Expanded adversarial datasets belong to Phase 74.
- Claim-audit enforcement over final publication artifacts belongs to Phase 76.

</deferred>
