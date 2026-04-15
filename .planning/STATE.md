# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** Not started (defining requirements)
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-15)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** Milestone v1.1 - EML Compiler and Warm Starts

## Current Position

Phase: Not started (defining requirements)
Plan: -
Status: Defining requirements
Last activity: 2026-04-15 - Milestone v1.1 started

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Research summary | `.planning/research/SUMMARY.md` | Complete |
| Requirements | `.planning/REQUIREMENTS.md` | Complete |
| Roadmap | `.planning/ROADMAP.md` | Complete |

## Current Milestone

**v1.1: EML Compiler and Warm Starts**

Goal: Turn verified reference demos into actual EML-tree recovery workflows by compiling ordinary formulas into exact EML ASTs and using those trees as warm starts for training.

Target features:
- Ordinary-expression-to-EML compiler subset.
- Warm-start embedding into soft master trees.
- Perturbed warm-start recovery tests.
- Trained EML recovery demos for Beer-Lambert and Michaelis-Menten.
- Normalized Planck stretch reporting.

## Phase Status

| Phase | Name | Status | Requirements |
|-------|------|--------|--------------|
| 1 | Semantics, AST, and Deterministic Artifacts | Complete | SEM-01, SEM-02, SEM-03, SEM-04 |
| 2 | Complete Master Trees and Soft Evaluation | Complete | TREE-01, TREE-02, TREE-03, TREE-04 |
| 3 | Optimizer, Restarts, Hardening, and Recovery Statuses | Complete | OPT-01, OPT-02, OPT-03, OPT-04 |
| 4 | Verifier and Acceptance Contract | Complete | VER-01, VER-02, VER-03 |
| 5 | Local Cleanup, SymPy Export, and Reports | Complete | CLEAN-01, CLEAN-02, CLEAN-03 |
| 6 | Demo Harness and Public Showcase | Complete | DEMO-01, DEMO-02, DEMO-03, DEMO-04 |
| 7 | Tests and Documentation | Complete | TEST-01, TEST-02 |

## Notes

- The roadmapper subagent failed before writing files, so roadmap and state were written directly from the research synthesis.
- The initial implementation should stay Python/PyTorch-first and dependency-light.
- Recovery claims must be verifier-owned and post-snap.
- Demos should follow `sources/FOR_DEMO.md` and report feasibility honestly.
- Verification completed with `python -m pytest` passing 15 tests.
- Demo reports generated under `artifacts/` for exact EML `exp`, Michaelis-Menten, and normalized Planck.

---
*Last updated: 2026-04-15 after starting milestone v1.1*
