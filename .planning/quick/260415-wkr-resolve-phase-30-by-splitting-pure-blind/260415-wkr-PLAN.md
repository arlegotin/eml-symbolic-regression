# Quick Plan: Resolve Phase 30 by Splitting Pure Blind and Scaffolded Claims

**Date:** 2026-04-15
**Workflow:** gsd-quick

## Goal

Resolve the Phase 30 review blocker with an honest long-term claim model:

- Pure random-initialized blind training is measured as its own boundary and cannot use scaffold initializers.
- Scaffolded/initialized shallow recovery is a separate bounded 100% proof claim.
- Reports, campaign presets, and regression tests keep the two claims separate.

## Tasks

- [x] Add separate proof claims and threshold policies for measured pure-blind recovery and bounded scaffolded recovery.
- [x] Add optimizer-suite metadata that can disable scaffold initializers for pure-blind runs.
- [x] Add a `v1.5-shallow-pure-blind` measured suite and reclassify `v1.5-shallow-proof` as scaffolded.
- [x] Update campaigns, aggregate thresholds, CLI claim listing, and regression tests around the split.
- [x] Run focused proof/benchmark/campaign tests.
- [x] Update roadmap, requirements, and state once verification passes.
