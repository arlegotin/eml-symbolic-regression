# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-20
**Current milestone:** None - v1.13 shipped and archived
**Next phase number:** 77

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

## Current Status

v1.13 is shipped and archived. It added the clean-room publication rebuild path, stronger verifier and split discipline, semantics-alignment evidence, CI/public snapshot validation, separated benchmark tracks, expanded dataset manifests, matched baseline harness, final v1.13 evidence package, claim audit, and release gate.

No active milestone is open. Start the next milestone with `$gsd-new-milestone`; phase numbering should continue at Phase 77.

## Archive Index

| Milestone | Roadmap | Requirements | Audit | Phase Artifacts |
|-----------|---------|--------------|-------|-----------------|
| v1.13 | `.planning/milestones/v1.13-ROADMAP.md` | `.planning/milestones/v1.13-REQUIREMENTS.md` | `.planning/milestones/v1.13-MILESTONE-AUDIT.md` | `.planning/milestones/v1.13-phases/` |
| v1.12 | `.planning/milestones/v1.12-ROADMAP.md` | `.planning/milestones/v1.12-REQUIREMENTS.md` | `.planning/v1.12-MILESTONE-AUDIT.md` | `.planning/milestones/v1.12-phases/` |
| v1.11 | `.planning/milestones/v1.11-ROADMAP.md` | `.planning/milestones/v1.11-REQUIREMENTS.md` | `.planning/milestones/v1.11-MILESTONE-AUDIT.md` | `.planning/milestones/v1.11-phases/` |

Older milestone archives remain under `.planning/milestones/`.

## Candidate Next Directions

- Manuscript packaging: venue-specific prose, bibliography, appendices, and submission assets.
- Formal assurance: theorem-prover or broader interval/certificate coverage for selected expressions.
- Baseline expansion: install and run optional external SR systems under the Phase 75 harness.
- Acceleration: profile the full rebuild and evaluate Rust or CUDA acceleration without changing semantics.
