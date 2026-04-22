---
phase: 94
status: passed
verified: 2026-04-22
---

# Phase 94 Verification

## Goal

Add the diagnostic layer needed to understand why v1.16 soft/loss-only candidates fail after snapping.

## Must-Have Checks

- Campaign rows expose selected/fallback candidate IDs, per-slot lowest-margin payloads, low-confidence alternatives, snap margins, active node counts, and soft-versus-hard deltas: verified in `campaign.py` paired/run columns and `test_campaign_tables_emit_geml_paired_comparison`.
- Snap mismatch diagnostics classify low-margin slots, hard-snap degradation, branch pathology, loss-only candidates, and verifier/optimization misses: verified in `paper_v117.py` and `tests/test_paper_v117.py`.
- Deterministic manifests identify v1.16-style failed/loss-only rows that should seed neighborhood search: verified by `snap-neighborhood-seeds.json` fixture assertions.
- Raw EML and i*pi EML diagnostics are emitted without changing verifier recovery definitions: verified by preserving existing `comparison_outcome` and adding raw/ipi-prefixed diagnostic fields.

## Automated Checks

```bash
python -m pytest tests/test_campaign.py::test_campaign_tables_emit_geml_paired_comparison tests/test_paper_v117.py -q
```

Result: `4 passed`.

## Human Verification

None required.
