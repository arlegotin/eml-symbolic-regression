---
phase: 98
status: passed
verified: 2026-04-22
implementation_commit: 3079007
---

# Phase 98 Verification

## Goal

Assemble a source-locked v1.17 evidence package and final next-campaign gate without mutating the v1.16 package.

## Must-Have Checks

- Package includes `eml.v117_evidence_package.v1`: verified by `test_write_v117_evidence_package_preserves_v116_and_blocks_without_exact_signal`.
- v1.16 remains an intact additive before-state reference: verified by the required `v116_package_manifest` source lock assertion.
- Final decisions are constrained and gate-controlled: verified by blocked no-signal and allowed exact-signal fixture tests.
- CLI command is registered with output, upstream artifact, v1.16 package, and overwrite options: verified by `test_cli_registers_geml_v117_package`.
- Existing v1.17 campaign table diagnostics remain compatible: verified by the targeted campaign test.
- Committed package artifacts exist under `artifacts/paper/v1.17-geml/` with decision `still_inconclusive`, source locks OK, and claim audit `passed`.

## Automated Checks

```bash
python -m pytest tests/test_paper_v117.py tests/test_campaign.py::test_campaign_tables_emit_geml_paired_comparison -q
```

Result: `14 passed`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v117-snap-diagnostics --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v117-neighborhoods --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v117-rank-candidates --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v117-sandbox --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v117-package --overwrite
```

Result: final package decision `still_inconclusive`; broader campaign gate `block_broader_campaigns`; claim audit `passed`.

## Human Verification

None required.
