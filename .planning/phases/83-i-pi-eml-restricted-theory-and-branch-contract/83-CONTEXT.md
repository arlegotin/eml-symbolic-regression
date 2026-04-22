# Phase 83: i*pi EML Restricted Theory and Branch Contract - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning
**Mode:** Autonomous smart discuss defaults

<domain>
## Phase Boundary

Phase 83 turns the new i*pi EML specialization into a claim-safe, branch-aware operator contract. It must provide executable restricted-domain theory checks for the requested identities and expose branch convention, proximity, crossing, invalid-domain, and branch-failure fields in evaluator/verifier artifacts before benchmark work begins.

</domain>

<decisions>
## Implementation Decisions

### Theory Scope
- Use executable high-precision checks and a generated theory note rather than formal theorem-prover certificates.
- Restrict the reciprocal, nested recovery, derivative, and one-step magnitude claims to positive-real second-slot domains and real-axis assumptions exactly as listed in v1.15 requirements.
- State that these identities do not imply full i*pi EML universality or global closure.

### Branch Contract
- Centralize principal-log branch diagnostics in a reusable module so semantics, verifier, and reports can share field names.
- Track branch convention, branch-cut proximity, branch-cut crossings/hits, invalid-domain skips, and branch-related candidate failure flags as structured dictionaries.
- Keep branch safety guards optional and training-only; faithful verification remains canonical principal-log evaluation.

### Integration Points
- Extend `AnomalyStats` without removing or renaming existing fields.
- Extend `VerificationReport.as_dict()` with branch diagnostics while preserving existing verifier keys.
- Add focused tests in semantic/verifier areas and a theory-artifact test rather than running broad campaigns.

### the agent's Discretion
Helper names, exact output filenames, and markdown formatting are at the agent's discretion, provided artifact schemas and tests make the branch contract machine-readable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `semantics.py` already counts log branch-cut hits and log-domain anomalies.
- `verify.py` owns verifier report serialization and failure reasons.
- `docs/IMPLEMENTATION.md` is the right place for concise branch/theory contract documentation.

### Established Patterns
- Tests prefer executable contract checks over informal prose.
- Artifact dictionaries carry explicit `schema` and status fields when they feed reports.
- Existing verification keeps branch-sensitive SymPy simplification failures non-fatal.

### Integration Points
- Branch diagnostics should be available from candidate exact AST evaluation where possible.
- Later phases will consume these fields in optimizer manifests, benchmark rows, and evidence packages.

</code_context>

<specifics>
## Specific Ideas

- Add a `branch.py` or similarly small module for principal-log diagnostics.
- Add an executable theory module for i*pi EML identities and write markdown/json artifacts under `artifacts/theory/v1.15/`.

</specifics>

<deferred>
## Deferred Ideas

- Benchmark target branch-domain validation belongs to Phase 85.
- Campaign-level aggregation of branch metrics belongs to Phase 86.
- Claim-audit language checks belong to Phase 87.

</deferred>
