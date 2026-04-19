# Phase 65: Shallow Seed and Depth-Curve Refresh - Plan

**Created:** 2026-04-19  
**Status:** Ready for execution

## Goal

Add small current-code evidence refreshes that strengthen the bounded shallow recovery and depth-limit story.

## Tasks

1. Add v1.12 shallow refresh suite construction for five new pure-blind and five new scaffolded `exp` seeds.
2. Add v1.12 depth refresh suite construction for current-code `proof-depth-curve` depth 2-5 blind rows with two seeds each.
3. Add a refresh runner that writes suite definitions, suite results, aggregates, compact tables, and a manifest.
4. Add CLI wiring for the refresh runner.
5. Add unit tests for suite construction and table/manifest behavior without running the full training refresh.
6. Run the actual refresh command and verify artifacts.

## Verification

- `v1.12-shallow-refresh` has 10 expanded runs: 5 pure-blind and 5 scaffolded.
- Current-code depth refresh has 8 expanded runs: depths 2, 3, 4, and 5 with seeds 0 and 1.
- Generated aggregates include seed, depth, start mode, evidence class, verifier outcome, failure/unsupported reason, and artifact path.
- Focused tests pass and the refresh CLI completes.

## Risks

- Training can fail in honest ways; those rows should remain visible.
- Runtime should stay bounded by using the requested shallow/depth subset only.
