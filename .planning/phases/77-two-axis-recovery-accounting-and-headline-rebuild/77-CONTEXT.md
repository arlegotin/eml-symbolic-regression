# Phase 77: Two-Axis Recovery Accounting and Headline Rebuild - Context

**Gathered:** 2026-04-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Separate verifier outcome from discovery/training evidence in run, aggregate, campaign, and publication claim-audit surfaces. Compile-only rows may remain verified support, but they must not contribute to trained recovery headlines.

</domain>

<decisions>
## Implementation Decisions

### Accounting Contract
- Preserve backward-compatible verifier-owned status fields where useful, but add explicit `verification_outcome`, `evidence_regime`, and `discovery_class` fields.
- Treat `start_mode=compile` plus verifier pass as `compile_only_verified_support`, not trained exact recovery.
- Count trained exact recovery from non-compile verified rows only.
- Keep unsupported and failed denominators visible.

### Public Headline
- Campaign report headline should show trained exact recoveries, compile-only verified support, unsupported rows, and failed rows.
- Avoid public wording that turns compile-only verifier support into a recovered headline.

### Claim Audit
- Audit should fail if compile-only verified rows appear in the trained recovery numerator.
- Audit should report corrected v1.14 headline counts for the paper-track package.
- Verifier evidence checks still apply to all verification-passed rows.

### the agent's Discretion
Implementation details may follow the current `benchmark.py`, `campaign.py`, and `publication.py` patterns.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `benchmark.aggregate_evidence()` centralizes aggregate JSON and Markdown.
- `campaign.write_campaign_report()` and `write_campaign_tables()` own public campaign headline surfaces.
- `publication.build_publication_claim_audit()` owns package-level release checks.

### Established Patterns
- Recovery taxonomy already uses `evidence_class` values such as `compile_only_verified`, `same_ast`, and `unsupported`.
- Reports keep mixed regimes visible through start-mode and evidence-class grouping.
- Tests use synthetic aggregate rows for schema and headline regression checks.

### Integration Points
- Add derived fields during `execute_benchmark_run()` and preserve them through `_run_summary()`.
- Add aggregate-level counts and use them in campaign tables, report Markdown, and claim audit checks.

</code_context>

<specifics>
## Specific Ideas

- Expected corrected paper-track headline: 8 trained exact recoveries, 1 compile-only verified support row, 15 unsupported rows, 0 failed rows.
- The existing v1.13 aggregate has 24 rows with `compile_only_verified=1`, `same_ast=8`, and `unsupported=15`.

</specifics>

<deferred>
## Deferred Ideas

Robust warm-start relabeling, baseline quarantine, verifier multivariate target lookup, and regenerated publication artifacts are covered by later v1.14 phases.

</deferred>
