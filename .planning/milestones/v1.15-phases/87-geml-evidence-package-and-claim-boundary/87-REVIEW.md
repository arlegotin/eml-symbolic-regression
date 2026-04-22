status: clean

# Phase 87 Code Review

## Scope

Reviewed:

- `src/eml_symbolic_regression/geml_package.py`
- `src/eml_symbolic_regression/campaign.py`
- `src/eml_symbolic_regression/cli.py`
- `tests/test_geml_package.py`
- `tests/test_campaign.py`
- `artifacts/campaigns/v1.15-geml-oscillatory-smoke/`
- `artifacts/paper/v1.15-geml/`

## Findings

No open findings.

## Fixed During Review

- Added formula-based target-family fallback for paired campaign rows whose aggregate payloads do not carry benchmark tags.
- Counted loss-only paired outcomes as `neither_recovered` in the paired summary while also exposing explicit loss-only counters.
- Removed the manifest self-lock from the manifest output list so refreshes do not record a stale pre-refresh hash.

## Residual Risk

The checked-in campaign is the cheap two-pair smoke protocol. The final package therefore makes an `inconclusive_smoke_only` decision and does not claim a paper-worthy i*pi section until the full matched campaign is run.
