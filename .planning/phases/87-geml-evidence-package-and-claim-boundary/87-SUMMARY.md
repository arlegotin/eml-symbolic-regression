# Phase 87 Summary: GEML Evidence Package and Claim Boundary

## Status

Complete.

## Commits

- `5497c98` - `docs(87): smart discuss context and plan`
- `7735b54` - `feat(87): add GEML evidence package`

## Delivered

- Added `geml_package.py` to build a deterministic v1.15 evidence package.
- Added `eml-sr geml-package` CLI support for reproducible package refreshes.
- Generated the cheap v1.15 GEML smoke campaign under `artifacts/campaigns/v1.15-geml-oscillatory-smoke/`.
- Generated the final package under `artifacts/paper/v1.15-geml/` with:
  - benchmark manifests,
  - target-family classification JSON/CSV/Markdown,
  - claim audit JSON/Markdown,
  - claim-boundary summary,
  - source locks,
  - reproduction commands.
- Classified paired evidence by target family, including negative-control rows.
- Added claim-audit checks that reject overbroad comparative, blind-recovery, and universality language.

## Tests

- `PYTHONPATH=src python -m pytest tests/test_geml_package.py tests/test_campaign.py tests/test_benchmark_reports.py -q`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_optimizer_cleanup.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m compileall -q src tests`
- `git diff --check`

## Outcome

The package decision is `inconclusive_smoke_only`: the smoke protocol provides useful paired diagnostics, but no verifier-gated exact recovery and not enough coverage to justify a stronger i*pi EML paper-section claim. The artifact explicitly keeps the full matched campaign as the next reproduction command.
