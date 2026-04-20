---
quick_id: 260420-bia
slug: fix-readme-plot-gallery-to-one-conservat
status: complete
created: 2026-04-20
completed: 2026-04-20
workflow: gsd-quick
files_modified:
  - README.md
  - readme-assets/fit-gallery.svg
summary_artifact: .planning/quick/260420-bia-fix-readme-plot-gallery-to-one-conservat/260420-bia-SUMMARY.md
---

# Quick Task 260420-bia Summary: Fixed 2x2 README Plot Gallery

## Status

Replaced the stacked README plot list with a single conservative 2x2 SVG gallery.

The gallery now contains exactly four panels: two good fits and two bad/stretch diagnostics. Planck uses the same plain style as the other panels. The legend is below the panels, outside the plotting areas. Candidate and target curves use solid colors only, so there is no dashed/solid overlap clutter.

## Verification Completed

```bash
rg --files readme-assets
```

Result: passed; only `readme-assets/fit-gallery.svg` remains.

```bash
rg -n "fit-gallery|approximation-|\.planning|sources|artifacts" README.md
```

Result: passed; README references `fit-gallery.svg` and has no old plot refs or forbidden internal refs.

```bash
python - <<'PY'
from pathlib import Path
paths = sorted(Path('readme-assets').glob('*.svg'))
print(f'count={len(paths)}')
for path in paths:
    text = path.read_text(encoding='utf-8')
    checks = {
        'svg': text.startswith('<?xml') and text.rstrip().endswith('</svg>'),
        'four_titles': text.count('Good:') == 2 and text.count('Bad/stretch:') == 2,
        'no_dash': 'stroke-dasharray' not in text,
        'no_rx': 'rx=' not in text,
        'legend_outside': 'Legend is outside the plotting panels' in text,
    }
    print(path, checks)
PY
```

Result: passed.

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

README gallery commit: `79059e0`.
