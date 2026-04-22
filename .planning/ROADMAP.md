# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-22
**Current milestone:** None - v1.15 shipped
**Next phase number:** 88

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)
- **v1.5 Training Proof and Recovery Guarantees** - Phases 29-33 complete (completed 2026-04-16; archive: `.planning/milestones/v1.5-ROADMAP.md`)
- **v1.6 Hybrid Search Pipeline and Exact Candidate Recovery** - Phases 34-38 complete (completed 2026-04-16; archive: `.planning/milestones/v1.6-ROADMAP.md`)
- **v1.7 Centered-Family Baseline and Paper Decision** - Phases 39-43 complete (completed 2026-04-16; archive: `.planning/milestones/v1.7-ROADMAP.md`)
- **v1.8 Centered-Family Viability and Full Evidence Run** - Phases 44-48 complete (completed 2026-04-17; archive: `.planning/milestones/v1.8-ROADMAP.md`)
- **v1.9 Raw-EML Hybrid Recovery and Paper Suite** - Phases 49-53 complete (completed 2026-04-17; archive: `.planning/milestones/v1.9-ROADMAP.md`)
- **v1.10 Search-backed motif library and compiler shortening for logistic and Planck** - Phases 54-58 complete (completed 2026-04-18; archive: `.planning/milestones/v1.10-ROADMAP.md`)
- **v1.11 Paper-strength evidence and figure package** - Phases 59-63 complete (completed 2026-04-19; archive: `.planning/milestones/v1.11-ROADMAP.md`)
- **v1.12 Paper draft skeleton and refreshed shallow evidence** - Phases 64-68 complete (completed 2026-04-19; archive: `.planning/milestones/v1.12-ROADMAP.md`)
- **v1.13 Publication-grade reproduction and validation** - Phases 69-76 complete (completed 2026-04-20; archives: `.planning/milestones/v1.13-ROADMAP.md`, `.planning/milestones/v1.13-REQUIREMENTS.md`, `.planning/milestones/v1.13-MILESTONE-AUDIT.md`, `.planning/milestones/v1.13-phases/`)
- **v1.14 Evidence claim integrity and audit hardening** - Phases 77-81 complete (completed 2026-04-21; archives: `.planning/milestones/v1.14-ROADMAP.md`, `.planning/milestones/v1.14-REQUIREMENTS.md`, `.planning/milestones/v1.14-phases/`)
- **v1.15 GEML family and i*pi EML exploration** - Phases 82-87 complete (completed 2026-04-22; archives: `.planning/milestones/v1.15-ROADMAP.md`, `.planning/milestones/v1.15-REQUIREMENTS.md`, `.planning/milestones/v1.15-MILESTONE-AUDIT.md`)

## Current Status

v1.15 is shipped and archived. It added fixed-parameter `GEML_a` semantics, restricted i*pi theory and branch diagnostics, family-aware training/snap integration, matched raw EML versus i*pi EML benchmark protocols, paired campaign outputs, and a final claim-safe evidence package.

The final package is intentionally bounded: `artifacts/paper/v1.15-geml/` reports `inconclusive_smoke_only` because the checked-in smoke campaign has two paired rows, no verifier-gated exact recovery, one periodic i*pi loss-only signal, and one negative-control raw loss-only signal.

## Active Phases

No active phases. Start the next milestone with `$gsd-new-milestone`; the next phase number is 88.

## Notes

- Full v1.15 phase details are archived in `.planning/milestones/v1.15-ROADMAP.md`.
- v1.15 requirements and audit are archived in `.planning/milestones/v1.15-REQUIREMENTS.md` and `.planning/milestones/v1.15-MILESTONE-AUDIT.md`.
- The full 20-row `geml-oscillatory` campaign remains available as a reproduction command, not a checked-in claim.

---
*Roadmap archived for v1.15 on 2026-04-22*
