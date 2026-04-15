# Phase 22: Evidence Report Assembly - Plan

status: planned

## Goal

Users receive a self-contained benchmark evidence report suitable for explaining how the paper's EML idea performs in this implementation.

## Tasks

- Add `write_campaign_report`.
- Include headline metrics, figure/table links, raw artifact links, and reproduction command.
- Add narrative sections for strengths, limitations, failed/unsupported cases, and next experiments.
- Add focused tests for report generation and manifest linkage.

## Verification

- `python -m pytest tests/test_campaign.py -q`

## Out of Scope

- README/docs updates.
- Committed showcase artifact generation.
