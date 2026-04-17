# Phase 46: Family Matrix Calibration - Context

**Gathered:** 2026-04-17
**Status:** Ready for planning
**Mode:** Auto-selected defaults from `$gsd-autonomous`

<domain>
## Phase Boundary

Expand v1.8 family suites and calibration artifacts so raw EML, fixed centered scales, and continuation schedules are represented before full evidence runs.

</domain>

<decisions>
## Implementation Decisions

### Matrix Shape
- Preserve v1.7 suite IDs as historical anchors.
- Add v1.8 suite IDs for expanded `s in {1,2,4,8}` fixed `CEML_s` and `ZEML_s` variants.
- Include continuation schedules `ZEML_8 -> ZEML_4` and `ZEML_8 -> ZEML_4 -> ZEML_2 -> ZEML_1`.
- Add a focused calibration preset separate from full shallow, basin, depth-curve, standard, and showcase evidence.

### Artifact Policy
- Campaign run IDs and tables must expose formula, start mode, training mode, depth, seed, operator family, and schedule.
- Calibration artifacts must record exclusions and recommended full-run scope.
- Keep expensive showcase optional until earlier evidence shows a centered-family signal.

### the agent's Discretion
Exact case IDs and descriptions can follow existing naming patterns as long as filters remain stable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `_family_suite` clones existing suites over operator variants.
- `CampaignPreset` maps named CLI presets to benchmark suite IDs.
- Operator-family tables already include fixed operator and schedule columns.

### Established Patterns
- New evidence suites get new IDs instead of overwriting proof or historical campaign contracts.
- Tests assert suite counts, variant labels, and campaign preset mappings.

### Integration Points
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/campaign.py`
- `tests/test_benchmark_contract.py`
- `tests/test_campaign.py`

</code_context>

<specifics>
## Specific Ideas

Use `family-calibration` for focused `exp` and `log` probes, then use the resulting aggregate in the go/no-go artifact.

</specifics>

<deferred>
## Deferred Ideas

Additional CEML continuation schedules can wait until fixed-scale evidence suggests they are worth the larger matrix.

</deferred>
