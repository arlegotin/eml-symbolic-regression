# Perturbed Basin Bound Report

- Formula: `beer_lambert`
- Declared noise grid: 5, 15, 35
- Declared bounded proof max: 5
- Raw supported max: 5
- Repaired supported max: 35
- Claim recommendation: `probe_supports_35`

High-noise probe rows remain separate from bounded proof thresholds. Probe evidence can support a follow-up bound only when it forms a continuous declared-grid prefix.

## Rows

| Source | Suite | Case | Run | Seed | Noise | Status | Claim | Evidence | Return Kind | Raw Status | Repair Status | Changed Slots | Accepted Repair Moves | Reason | Artifact |
|--------|-------|------|-----|------|-------|--------|-------|----------|-------------|------------|---------------|---------------|-----------------------|--------|----------|
| bounded | proof-perturbed-basin | basin-beer-lambert-bound | proof-perturbed-basin-basin-beer-lambert-bound-f716bb6f9e3e | 0 | 5 | recovered | recovered | perturbed_true_tree_recovered | same_ast_return | recovered | not_attempted | 0 | 0 | verified | /tmp/eml-phase31-basin-bound/bounded/proof-perturbed-basin/proof-perturbed-basin-basin-beer-lambert-bound-f716bb6f9e3e.json |
| bounded | proof-perturbed-basin | basin-beer-lambert-bound | proof-perturbed-basin-basin-beer-lambert-bound-88212187883e | 1 | 5 | recovered | recovered | perturbed_true_tree_recovered | same_ast_return | recovered | not_attempted | 0 | 0 | verified | /tmp/eml-phase31-basin-bound/bounded/proof-perturbed-basin/proof-perturbed-basin-basin-beer-lambert-bound-88212187883e.json |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-18d83e2efbce | 0 | 15 | recovered | recovered | perturbed_true_tree_recovered | same_ast_return | recovered | not_attempted | 0 | 0 | verified | /tmp/eml-phase31-basin-bound/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-18d83e2efbce.json |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-015438da428c | 1 | 15 | repaired_candidate | recovered | repaired_candidate | snapped_but_failed | snapped_but_failed | repaired | 1 | 1 | mpmath_failed | /tmp/eml-phase31-basin-bound/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-015438da428c.json |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-8d0fd251f11f | 0 | 35 | repaired_candidate | recovered | repaired_candidate | snapped_but_failed | snapped_but_failed | repaired | 5 | 6 | mpmath_failed | /tmp/eml-phase31-basin-bound/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-8d0fd251f11f.json |
| probe | proof-perturbed-basin-beer-probes | basin-beer-lambert-bound-probes | proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-2535ff9f4d39 | 1 | 35 | repaired_candidate | recovered | repaired_candidate | snapped_but_failed | snapped_but_failed | repaired | 3 | 1 | mpmath_failed | /tmp/eml-phase31-basin-bound/probe/proof-perturbed-basin-beer-probes/proof-perturbed-basin-beer-probes-basin-beer-lambert-bound-probes-2535ff9f4d39.json |
