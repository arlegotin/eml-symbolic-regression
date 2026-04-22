# Phase 78 Plan: Warm-Start Evidence Relabeling

## Tasks

1. Add warm-start evidence labeling helpers in benchmark aggregation.
   - Derive zero-noise same-AST warm starts as `exact_seed_round_trip`.
   - Derive nonzero same-AST or verified-equivalent returns as perturbed warm-start evidence only when the run shape supports it.
   - Preserve unsupported/failed rows as non-evidence labels.

2. Surface required warm-start accounting fields.
   - Include `warm_start_evidence`, `ast_return_status`, and `total_restarts` in aggregate run summaries.
   - Export those fields in campaign `runs.csv`.
   - Keep existing fields such as `perturbation_noise`, `warm_steps`, `warm_restarts`, `return_kind`, and `changed_slot_count`.

3. Update narrative text.
   - Rewrite same-AST warm-start report/README wording to exact seed round-trip language.
   - Avoid robustness/basin wording for zero-noise single-seed single-step warm-start evidence.
   - Keep perturbed true-tree basin wording unchanged for proof-basin reports.

4. Add regression tests.
   - Assert zero-noise same-AST warm starts get exact seed round-trip labels.
   - Assert campaign CSV includes the new fields and total restart count.
   - Assert report prose for warm-only zero-noise rows avoids robustness/basin language.

## Verification

- Run focused benchmark/campaign report tests.
- Run compile checks for touched modules.
- Run `git diff --check`.

