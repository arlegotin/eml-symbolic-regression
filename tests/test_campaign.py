import json

import pytest

from eml_symbolic_regression.benchmark import RunFilter, load_suite
from eml_symbolic_regression.campaign import (
    CampaignOutputExistsError,
    campaign_preset,
    list_campaign_presets,
    run_campaign,
)


def test_campaign_presets_map_to_budgeted_suites():
    assert list_campaign_presets() == ("smoke", "standard", "showcase")

    standard = campaign_preset("standard")
    suite = load_suite(standard.suite)
    runs = suite.expanded_runs()

    assert standard.tier == "showcase-default"
    assert {run.start_mode for run in runs} >= {"blind", "warm_start", "compile"}
    assert any(run.case_id == "beer-perturbation-sweep" for run in runs)
    assert any(run.formula == "michaelis_menten" for run in runs)
    assert any(run.formula == "planck" for run in runs)
    assert {"radioactive_decay", "logistic", "shockley"} <= {run.formula for run in runs}


def test_campaign_writes_manifest_suite_result_and_aggregate(tmp_path):
    result = run_campaign(
        "smoke",
        output_root=tmp_path,
        label="ci-smoke",
        run_filter=RunFilter(case_ids=("planck-diagnostic",)),
    )

    assert result.campaign_dir == tmp_path / "ci-smoke"
    assert result.manifest_path.exists()
    assert result.suite_result_path.exists()
    assert result.aggregate_paths["json"].exists()
    assert result.aggregate_paths["markdown"].exists()

    manifest = json.loads(result.manifest_path.read_text())
    assert manifest["schema"] == "eml.campaign_manifest.v1"
    assert manifest["preset"]["name"] == "smoke"
    assert manifest["suite"]["id"] == "smoke"
    assert manifest["counts"]["total"] == 1
    assert manifest["run_filter"]["case_ids"] == ["planck-diagnostic"]
    assert "campaign smoke" in manifest["reproducibility"]["command"]


def test_campaign_refuses_silent_overwrite(tmp_path):
    run_campaign(
        "smoke",
        output_root=tmp_path,
        label="existing",
        run_filter=RunFilter(case_ids=("planck-diagnostic",)),
    )

    with pytest.raises(CampaignOutputExistsError):
        run_campaign(
            "smoke",
            output_root=tmp_path,
            label="existing",
            run_filter=RunFilter(case_ids=("planck-diagnostic",)),
        )

    replacement = run_campaign(
        "smoke",
        output_root=tmp_path,
        label="existing",
        overwrite=True,
        run_filter=RunFilter(case_ids=("planck-diagnostic",)),
    )

    assert replacement.manifest_path.exists()
