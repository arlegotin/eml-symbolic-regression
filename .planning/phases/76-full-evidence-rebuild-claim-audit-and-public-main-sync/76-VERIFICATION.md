---
status: passed
verified_at: "2026-04-20"
implementation_commit: 2dbe429
evidence_commit: 31006ac
---

# Phase 76: Full Evidence Rebuild, Claim Audit, and Public Main Sync - Verification

## Result

Passed.

## Commands

```bash
PYTHONPATH=src python -m compileall -q src/eml_symbolic_regression/publication.py src/eml_symbolic_regression/cli.py
```

Result: passed.

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py -q
```

Result: 8 passed.

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py tests/test_baseline_harness.py tests/test_expanded_datasets.py -q
```

Result: 23 passed in 2.38s.

```bash
python scripts/validate-ci-contract.py --mode dev --root .
```

Result: `dev: ok`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir /tmp/eml-phase76-publication-smoke --smoke --overwrite --allow-dirty
```

Result: smoke rebuild passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir artifacts/paper/v1.13 --overwrite --allow-dirty
```

Result: full rebuild passed and wrote `artifacts/paper/v1.13/manifest.json`.

```bash
node -e 'const fs=require("fs"); const m=JSON.parse(fs.readFileSync("artifacts/paper/v1.13/manifest.json","utf8")); const bad=(m.outputs||[]).filter(r=>r.path.includes("suite-result")||r.path.includes("/runs/")); if(m.validation.status!=="passed"||m.claim_audit.status!=="passed"||m.release_gate.status!=="passed"||bad.length){ process.exit(1); } console.log(`manifest ok: ${m.outputs.length} linked outputs, no raw runs`);'
```

Result: `manifest ok: 22 linked outputs, no raw runs`.

```bash
git diff --check
```

Result: passed.

## Acceptance Checks

- Full rebuild generated the campaign, baseline, dataset, publication, claim-audit, release-gate, source-lock, and validation artifacts.
- Claim audit passed with verifier evidence, track labels, source artifact links, final-confirmation or substitute verifier evidence, and baseline context present.
- Public snapshot contract validated locally through the release gate.
- Generated v1.13 artifacts were committed on `dev`.
- Direct remote `main` force-push was not attempted locally; the release gate records readiness for `.github/workflows/publish-main.yml`.
