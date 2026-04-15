# Roadmap: EML Symbolic Regression

**Created:** 2026-04-15
**Updated:** 2026-04-15
**Granularity:** Coarse
**Mode:** YOLO
**Current milestone:** None - v1.4 shipped
**Coverage:** No active milestone requirements

## Overview

The project has shipped five milestone cycles. v1.0 established the core EML symbolic-regression engine. v1.1 added compiler-driven warm starts. v1.2 added benchmark contracts and recovery evidence. v1.3 added campaign reports. v1.4 improved measured recovery against the committed v1.3 standard/showcase baselines.

Detailed completed milestone roadmaps are archived under `.planning/milestones/`.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)

## Latest Shipped Milestone

### v1.4 Recovery Performance Improvements

**Goal shipped:** Improve real end-to-end recovery performance against committed v1.3 standard/showcase baselines, then rerun the same campaigns to produce before/after evidence.

**Completed phases:**

- Phase 24: Baseline Failure Triage and Diagnostic Harness
- Phase 25: Blind Optimizer Recovery Improvements
- Phase 26: Warm-Start Perturbation Robustness
- Phase 27: Compiler Coverage and Depth Reduction
- Phase 28: Before/After Campaign Evaluation

**Outcome:** v1.4 improved overall recovery from 18/45 to 27/45 across the combined standard/showcase before-after comparison. Blind recovery improved from 3/15 to 10/15, compiler coverage improved from 0/9 to 2/9, and Beer-Lambert perturbation recovery remained unchanged with a clearer failure mechanism.

## Next Step

No active milestone is currently defined. Start the next cycle with `/gsd-new-milestone`.

---
*Roadmap updated: 2026-04-15 after archiving milestone v1.4*
