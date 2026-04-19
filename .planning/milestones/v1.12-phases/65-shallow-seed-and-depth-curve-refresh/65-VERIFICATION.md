---
status: passed
phase: 65
phase_name: Shallow Seed and Depth-Curve Refresh
verified_at: 2026-04-19
---

# Phase 65 Verification

## Must-Haves

- [x] Shallow refresh artifacts include at least five new pure-blind seeds.
- [x] Shallow refresh artifacts include at least five new scaffolded seeds.
- [x] Depth refresh artifacts cover depths 2, 3, 4, and 5 with at least two seeds each.
- [x] Aggregates keep regimes and denominators separate.
- [x] Source tables include seed, depth, start mode, evidence class, verifier outcome, failure reason, and artifact path.

## Evidence

- Focused tests passed: `7 passed in 1.35s`.
- Refresh command completed with `shallow runs -> 10` and `depth runs -> 8`.
- `artifacts/campaigns/v1.12-evidence-refresh/manifest.json` records 10 shallow runs, 8 depth runs, 4 depth summary rows, 10 shallow verifier recoveries, and 4 depth verifier recoveries.
- `artifacts/campaigns/v1.12-evidence-refresh/tables/depth-refresh-summary.md` records depths 2-5 with two rows per depth group.

## Result

Phase 65 passes verification.
