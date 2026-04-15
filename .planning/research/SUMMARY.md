# Research Summary: v1.2 Training Benchmark and Recovery Evidence

**Project:** EML Symbolic Regression
**Domain:** Repeatable training benchmarks and recovery evidence for the EML symbolic-regression engine
**Recorded:** 2026-04-15
**Research decision:** External research skipped; this is an internal evidence milestone grounded in current code, v1.1 artifacts, `sources/NORTH_STAR.md`, and `sources/FOR_DEMO.md`.

## Executive Summary

v1.2 should turn the current anecdotal training results into a reproducible benchmark harness. The important question is no longer whether the compiler and warm-start infrastructure can represent formulas; v1.1 proved that. The important question is how often training recovers exact verified formulas under blind starts, same-basin warm starts, perturbation sweeps, and current depth gates.

The milestone should preserve the existing verifier-owned recovery contract. A run is recovered only when the snapped exact candidate passes verification. Training loss, compiler success, catalog equality, and same-AST warm-start return are useful evidence stages, but none of them should become a recovery claim by themselves.

## Current Evidence Baseline

- Blind `exp` training recovered after snapping in the existing artifact: `best_loss ~= 3.6e-6`, `post_snap_loss = 0`, verifier passed.
- Beer-Lambert warm starts recover perfectly from no perturbation or mild perturbation: losses are near zero and high-precision verification passes.
- A stronger Beer-Lambert perturbation that changed active discrete slots failed in the tested run: `best_loss ~= 0.213`, verifier failed.
- Michaelis-Menten and normalized Planck remain unsupported/stretch under the current compiler and depth gates.

## Stack Additions

No new mandatory runtime dependencies are required. Prefer standard library JSON, CSV, Markdown, and existing PyTorch/SymPy/mpmath/pytest facilities. Add plotting or dataframe dependencies only if a later phase proves they materially improve reporting.

## Feature Table Stakes

- Deterministic benchmark suite files define formulas, datasets, start modes, seeds, perturbation levels, optimizer budgets, verifier settings, and artifact locations.
- CLI support runs a full suite or a filtered subset and writes per-run JSON artifacts plus aggregate summaries.
- Aggregation reports recovery rate, verifier pass/fail, best loss, post-snap loss, snap outcome, active slot changes, runtime, unsupported reasons, and failure classes.
- Formula coverage includes shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten diagnostics, normalized Planck stretch diagnostics, and selected `sources/FOR_DEMO.md` formulas where current gates allow honest runs.
- Documentation answers whether the system is promising from aggregate evidence rather than cherry-picked examples.

## Watch Out For

- Do not hide failed or unsupported runs.
- Do not call same-AST warm-start return "discovery".
- Do not promote formulas based on loss alone; `verify.py` remains the owner of `recovered`.
- Keep CI smoke suites small enough to run quickly, with larger benchmark suites available as explicit commands.
- Treat Planck as a stretch diagnostic unless depth and training evidence improve.

## Recommended Phase Shape

1. Benchmark contract and suite registry.
2. Benchmark runner and per-run artifacts.
3. Training matrix coverage for blind starts, warm starts, perturbation sweeps, and unsupported/stretch cases.
4. Aggregation and evidence reports.
5. Regression tests and documentation.

---
*Research decision recorded: 2026-04-15*
