---
status: clean
reviewed_at: "2026-04-20"
implementation_commit: 994dbaf
---

# Phase 73: Basis-Only and Literal-Constants Benchmark Tracks - Review

## Findings

No blocking findings.

## Review Notes

- The strict basis-only behavior is opt-in through the new track suite, which avoids silently changing historical v1.11/v1.12 evidence semantics.
- Basis-only rows validate that no non-1 literal constants are present and use `CompilerConfig.constant_policy="basis_only"`, so literal-coefficient targets fail closed instead of being accidentally compiled through the convenience policy.
- Literal-constant rows expose constants policy, literal catalog, start mode, warm-start status, and scaffold status in `benchmark_track`.
- Mixed-track aggregates now include a top-level `tracks` denominator table and group summaries for `benchmark_track` and `constants_policy`.
- The `paper-tracks` campaign preset is a routing layer over existing benchmark infrastructure rather than a separate reporting path.

## Residual Risk

- The publication target inventory is now centralized in `PUBLICATION_BENCHMARK_TARGETS`; Phase 74 or Phase 76 may need to extend it if new datasets or final publication targets are added.
- Existing legacy suites still default to the historical literal-capable policy. Publication claims should use the new v1.13 track suites when denominator purity matters.
