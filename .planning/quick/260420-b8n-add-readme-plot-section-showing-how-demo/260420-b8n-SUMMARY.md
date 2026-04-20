---
quick_id: 260420-b8n
slug: add-readme-plot-section-showing-how-demo
status: complete
created: 2026-04-20
completed: 2026-04-20
workflow: gsd-quick
files_modified:
  - README.md
  - readme-assets/approximation-arrhenius.svg
  - readme-assets/approximation-beer-lambert.svg
  - readme-assets/approximation-michaelis-menten.svg
  - readme-assets/approximation-planck.svg
summary_artifact: .planning/quick/260420-b8n-add-readme-plot-section-showing-how-demo/260420-b8n-SUMMARY.md
---

# Quick Task 260420-b8n Summary: README Approximation Plots

## Status

Added a README section showing representative approximation/verification plots.

The new plots show sampled training points, target curves, and candidate curves for Beer-Lambert, Arrhenius, Michaelis-Menten, and Planck. The README text keeps the evidence boundary clear: exact and same-AST cases overlay the target, while Planck remains a stretch diagnostic rather than a recovered EML claim.

## Verification Completed

```bash
rg --files readme-assets
```

Result: passed; four SVG plot assets are present.

```bash
rg -n "\.planning|sources|artifacts" README.md
```

Result: passed with no matches.

```bash
python - <<'PY'
from pathlib import Path
for path in sorted(Path('readme-assets').glob('*.svg')):
    text = path.read_text(encoding='utf-8')
    ok = text.startswith('<?xml') and text.rstrip().endswith('</svg>') and '<polyline' in text and '<circle' in text
    print(f'{path}: {"ok" if ok else "bad"}')
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

Full pytest was not run because this was a docs/asset-only change and the focused checks cover the README claims without regenerating broader benchmark outputs.

## Commit

README and plot assets commit: `842797d`.
