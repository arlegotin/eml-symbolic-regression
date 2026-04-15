# Perturbed Basin Bound Report

- Formula: `beer_lambert`
- Declared noise grid: 5, 15, 35
- Declared bounded proof max: 5
- Raw supported max: 5
- Repaired supported max: 35
- Claim recommendation: `probe_supports_35`
- Expected seed/noise rows: 6
- Missing seed/noise rows: 0

High-noise probe rows remain separate from bounded proof thresholds. Probe evidence can support a follow-up bound only when it forms a continuous declared-grid prefix.

## Rows

| Source | Suite | Case | Run | Seed | Noise | Status | Claim | Evidence | Return Kind | Raw Status | Repair Status | Changed Slots | Accepted Repair Moves | Reason | Artifact | Artifact SHA256 |
|--------|-------|------|-----|------|-------|--------|-------|----------|-------------|------------|---------------|---------------|-----------------------|--------|----------|----------|
| bounded | proof-perturbed-basin | basin-beer-lambert-bound | proof-perturbed-basin-basin-beer-lambert-bound-f716bb6f9e3e | 0 | 5 | recovered | recovered | perturbed_true_tree_recovered | same_ast_return | recovered | not_attempted | 0 | 0 | verified | artifacts/diagnostics/phase31-basin-bound/raw-runs/bounded/proof-perturbed-basin/proof-perturbed-basin-basin-beer-lambert-bound-f716bb6f9e3e.json | 5189e632e6a147f743c40d709574a512285ce1bfa69792e2d5d6ab11f84bd1fe |
| bounded | proof-perturbed-basin | basin-beer-lambert-bound | proof-perturbed-basin-basin-beer-lambert-bound-88212187883e | 1 | 5 | recovered | recovered | perturbed_true_tree_recovered | same_ast_return | recovered | not_attempted | 0 | 0 | verified | artifacts/diagnostics/phase31-basin-bound/raw-runs/bounded/proof-perturbed-basin/proof-perturbed-basin-basin-beer-lambert-bound-88212187883e.json | d9d2523d0a034586c9d9e4cd1ea33043e019818957dbd766c815ae5bbe969ba7 |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-18d83e2efbce | 0 | 15 | recovered | recovered | perturbed_true_tree_recovered | same_ast_return | recovered | not_attempted | 0 | 0 | verified | artifacts/diagnostics/phase31-basin-bound/raw-runs/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-18d83e2efbce.json | da2cb74808f97e32f101f927626b3637784c12d9b0a94d081b22af9be83ef54d |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-015438da428c | 1 | 15 | repaired_candidate | recovered | repaired_candidate | snapped_but_failed | snapped_but_failed | repaired | 1 | 1 | mpmath_failed | artifacts/diagnostics/phase31-basin-bound/raw-runs/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-015438da428c.json | 51c417bf97b474eaf382fbcb3eeadd02eb3fdf8adbeb7c5b0255e82421e27c8c |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-8d0fd251f11f | 0 | 35 | repaired_candidate | recovered | repaired_candidate | snapped_but_failed | snapped_but_failed | repaired | 5 | 6 | mpmath_failed | artifacts/diagnostics/phase31-basin-bound/raw-runs/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-8d0fd251f11f.json | 678176db50237c647c7156a39cb96eff5dc24f4a4eef64ce175c77f9ff3d8bf0 |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-2535ff9f4d39 | 1 | 35 | repaired_candidate | recovered | repaired_candidate | snapped_but_failed | snapped_but_failed | repaired | 3 | 1 | mpmath_failed | artifacts/diagnostics/phase31-basin-bound/raw-runs/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-2535ff9f4d39.json | 59c665008c0fcf6f2f5ced0c0134829714cc83bed40158b1e38090736b0dda47 |
