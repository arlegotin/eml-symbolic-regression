---
quick_id: 260420-bdg
slug: expand-readme-fit-plots-with-four-additi
status: complete
created: 2026-04-20
completed: 2026-04-20
workflow: gsd-quick
files_modified:
  - README.md
  - readme-assets/approximation-arrhenius.svg
  - readme-assets/approximation-beer-lambert.svg
  - readme-assets/approximation-damped-oscillator.svg
  - readme-assets/approximation-exp.svg
  - readme-assets/approximation-log.svg
  - readme-assets/approximation-logistic.svg
  - readme-assets/approximation-michaelis-menten.svg
  - readme-assets/approximation-planck.svg
summary_artifact: .planning/quick/260420-bdg-expand-readme-fit-plots-with-four-additi/260420-bdg-SUMMARY.md
---

# Quick Task 260420-bdg Summary: Expanded Conservative Plot Gallery

## Status

Updated the README plot gallery.

The gallery now has eight plots total. Four new plots were added: `exp` and `log` as good exact overlays, and `logistic` and `damped_oscillator` as failed/stretch diagnostics. Existing plot assets were regenerated in a more conservative style: plain white background, thin axes, muted lines, no rounded card frame, and simpler labels.

## README Changes

- Added `Good fits` and `Failed and stretch diagnostics` groups.
- Kept Planck, logistic, and damped oscillator framed as diagnostic mismatches rather than recovered formulas.
- Preserved the public-facing README constraint: no `.planning`, source-document, or generated-output directory references.

## Verification Completed

```bash
rg --files readme-assets
```

Result: passed; eight SVG plot assets are present.

```bash
rg -n "\.planning|sources|artifacts" README.md
```

Result: passed with no matches.

```bash
python - <<'PY'
from pathlib import Path
paths = sorted(Path('readme-assets').glob('*.svg'))
print(f'count={len(paths)}')
for path in paths:
    text = path.read_text(encoding='utf-8')
    ok = text.startswith('<?xml') and text.rstrip().endswith('</svg>') and '<polyline' in text and '<circle' in text and 'rx=' not in text
    print(f'{path}: {"ok" if ok else "bad"}')
PY
```

Result: passed; count is 8 and all SVGs passed the structural/style sanity check.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos
```

Result: passed.

```bash
python -m pytest tests/test_semantics_expression.py tests/test_verifier_demos_cli.py
```

Result: passed, 18 tests.

## Notes

Full pytest was not run because this was a README/asset-only update and focused checks cover the changed claims without regenerating broader benchmark outputs.

## Commit

README and plot gallery commit: `46baa82`.
