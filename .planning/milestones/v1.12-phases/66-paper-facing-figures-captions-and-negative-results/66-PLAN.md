# Phase 66: Paper-Facing Figures, Captions, and Negative Results - Plan

**Created:** 2026-04-19  
**Status:** Ready for execution

## Goal

Make the paper visually and tabularly legible with motif evolution, pipeline, captions, and explicit negative-result framing.

## Tasks

1. Add a paper-facing artifact generator for captions, motif evolution rows, negative-results rows, and the pipeline SVG.
2. Generate `figure-captions.md` and `table-captions.md` under `artifacts/paper/v1.11/draft/`.
3. Generate motif library evolution JSON/CSV/Markdown from locked v1.11 motif diagnostics.
4. Generate logistic/Planck negative-results JSON/CSV/Markdown from locked v1.11 scientific-law and probe artifacts.
5. Generate deterministic `pipeline.svg` plus metadata.
6. Add CLI wiring and regression tests.
7. Run focused tests and generate the artifacts.

## Verification

- Caption files exist and reference relevant v1.11/v1.12 artifacts.
- Motif table includes logistic, Planck, Shockley, Arrhenius, and Michaelis-Menten.
- Negative-results table includes logistic and Planck with `promotion: no`.
- Pipeline SVG and metadata exist.
- Focused tests pass.

## Risks

- Motif table must explain Planck depth conventions instead of selecting only the favorable number.
- Captions must remain claim-safe and not promote unsupported diagnostics.
