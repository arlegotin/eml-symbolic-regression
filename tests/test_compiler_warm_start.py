import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import sympy as sp

from eml_symbolic_regression.compiler import (
    CompilerConfig,
    CompileReason,
    UnsupportedExpression,
    compile_and_validate,
    compile_sympy_expression,
    diagnose_compile_expression,
)
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.master_tree import EmbeddingConfig, EmbeddingError, SoftEMLTree
from eml_symbolic_regression.optimize import TrainingConfig
from eml_symbolic_regression.warm_start import PerturbationConfig, fit_warm_started_eml_tree
from eml_symbolic_regression.warm_start import perturb_tree_logits


ROOT = Path(__file__).resolve().parents[1]
CLI_ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


def test_compile_exp_log_and_beer_lambert_validate_against_sympy():
    x = sp.Symbol("x")
    inputs = {"x": np.linspace(0.25, 2.5, 12).astype(np.complex128)}
    config = CompilerConfig(variables=("x",), max_depth=12, max_nodes=128)

    for expr in (sp.exp(x), sp.log(x), sp.exp(sp.Float("-0.8") * x)):
        result = compile_and_validate(expr, config, inputs)
        assert result.validation is not None
        assert result.validation.passed
        assert result.metadata.unsupported_reason is None


def test_compile_shockley_uses_lower_depth_template():
    spec = get_demo("shockley")
    splits = spec.make_splits(points=24, seed=0)
    result = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=128),
        {spec.variable: splits[0].inputs[spec.variable]},
    )

    assert result.validation is not None
    assert result.validation.passed
    assert result.metadata.depth <= 13
    assert any(entry.rule == "scaled_exp_minus_one_template" for entry in result.metadata.trace)
    assert result.metadata.macro_diagnostics is not None
    assert result.metadata.macro_diagnostics["hits"] == ["scaled_exp_minus_one_template"]
    assert result.metadata.macro_diagnostics["depth_delta"] > 0
    assert result.metadata.macro_diagnostics["node_delta"] > 0


def test_michaelis_relaxed_diagnostic_reports_direct_division_macro():
    spec = get_demo("michaelis_menten")
    splits = spec.make_splits(points=24, seed=0)
    diagnostic = diagnose_compile_expression(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
        {spec.variable: splits[0].inputs[spec.variable]},
    )

    assert diagnostic["status"] == "unsupported"
    assert diagnostic["strict"]["reason"] == CompileReason.DEPTH_EXCEEDED
    relaxed_metadata = diagnostic["relaxed"]["metadata"]
    macro = relaxed_metadata["macro_diagnostics"]
    assert relaxed_metadata["depth"] <= 14
    assert macro["hits"] == ["direct_division_template"]
    assert macro["depth_delta"] > 0
    assert macro["node_delta"] > 0


def test_compile_arrhenius_uses_direct_division_template():
    spec = get_demo("arrhenius")
    splits = spec.make_splits(points=24, seed=0)
    result = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
        {spec.variable: splits[0].inputs[spec.variable]},
    )

    assert result.validation is not None
    assert result.validation.passed
    assert result.metadata.unsupported_reason is None
    assert result.metadata.depth == 7
    assert result.metadata.node_count <= 256
    assert result.metadata.macro_diagnostics is not None
    assert result.metadata.macro_diagnostics["hits"] == ["direct_division_template"]
    assert [entry.rule for entry in result.metadata.trace].count("direct_division_template") == 1


def test_compiler_fail_closed_negative_cases():
    x = sp.Symbol("x")

    with pytest.raises(UnsupportedExpression) as sin_error:
        compile_sympy_expression(sp.sin(x), CompilerConfig(variables=("x",)))
    assert sin_error.value.reason == CompileReason.UNSUPPORTED_OPERATOR

    with pytest.raises(UnsupportedExpression) as variable_error:
        compile_sympy_expression(x + sp.Symbol("y"), CompilerConfig(variables=("x",)))
    assert variable_error.value.reason == CompileReason.UNKNOWN_VARIABLE

    with pytest.raises(UnsupportedExpression) as constant_error:
        compile_sympy_expression(sp.Float("0.5"), CompilerConfig(constant_policy="basis_only"))
    assert constant_error.value.reason == CompileReason.CONSTANT_POLICY

    with pytest.raises(UnsupportedExpression) as depth_error:
        compile_sympy_expression(sp.exp(sp.Float("-0.8") * x), CompilerConfig(variables=("x",), max_depth=3))
    assert depth_error.value.reason == CompileReason.DEPTH_EXCEEDED


def test_compiler_diagnostics_include_relaxed_depth_metadata():
    spec = get_demo("planck")
    splits = spec.make_splits(points=12, seed=0)
    diagnostic = diagnose_compile_expression(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
        {spec.variable: splits[0].inputs[spec.variable]},
    )

    assert diagnostic["status"] == "unsupported"
    assert diagnostic["strict"]["reason"] == CompileReason.DEPTH_EXCEEDED
    assert diagnostic["relaxed"]["metadata"]["depth"] > 13
    assert diagnostic["relaxed"]["metadata"]["trace"]
    macro = diagnostic["relaxed"]["metadata"]["macro_diagnostics"]
    assert set(macro["hits"]) == {"scaled_exp_minus_one_template", "direct_division_template"}
    assert macro["depth_delta"] > 0
    assert macro["node_delta"] > 0


def test_damped_oscillator_diagnostic_defers_unsupported_cos():
    spec = get_demo("damped_oscillator")
    diagnostic = diagnose_compile_expression(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
    )

    assert diagnostic["status"] == "unsupported"
    assert diagnostic["strict"]["reason"] == CompileReason.UNSUPPORTED_OPERATOR
    assert diagnostic["relaxed_error"]["reason"] == CompileReason.UNSUPPORTED_OPERATOR


def test_constant_catalog_and_embedding_round_trip_for_beer_lambert():
    x = sp.Symbol("x")
    compiled = compile_and_validate(
        sp.exp(sp.Float("-0.8") * x),
        CompilerConfig(variables=("x",), max_depth=12, max_nodes=128),
    )
    tree = SoftEMLTree(compiled.metadata.depth, ("x",), compiled.metadata.constants)
    assert "const:-0.8" in tree.slot_catalog()["root.left"]

    embedding = tree.embed_expr(compiled.expression, EmbeddingConfig(strength=40.0))
    assert embedding.success
    assert embedding.round_trip_equal
    assert embedding.snap.min_margin > 0.99


def test_embedding_reports_missing_terminals():
    x = sp.Symbol("x")
    compiled = compile_and_validate(
        sp.exp(sp.Float("-0.8") * x),
        CompilerConfig(variables=("x",), max_depth=12, max_nodes=128),
    )
    tree = SoftEMLTree(compiled.metadata.depth, ("x",), (1.0,))

    with pytest.raises(EmbeddingError) as error:
        tree.embed_expr(compiled.expression)
    assert error.value.reason == "missing_constant"


def test_warm_start_manifest_returns_same_ast_and_verifies():
    spec = get_demo("beer_lambert")
    splits = spec.make_splits(points=24, seed=0)
    compiled = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=12, max_nodes=128),
        {spec.variable: splits[0].inputs[spec.variable]},
    )
    result = fit_warm_started_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(depth=compiled.metadata.depth, variables=(spec.variable,), steps=1, restarts=1, seed=0),
        compiled.expression,
        perturbation_config=PerturbationConfig(seed=0, noise_scale=0.0),
        verification_splits=splits,
        compiler_metadata=compiled.metadata.as_dict(),
    )

    assert result.status == "same_ast_return"
    assert result.verification is not None
    assert result.verification.status == "recovered"
    assert result.manifest["optimizer"]["status"] == "snapped_candidate"
    assert result.manifest["status"] == "same_ast_return"
    assert result.manifest["diagnosis"]["mechanism"] == "same_ast_return"
    assert result.manifest["diagnosis"]["changed_slot_count"] == 0


def test_arrhenius_warm_start_returns_same_ast_and_verifies():
    # v1.9-arrhenius-evidence / arrhenius-warm is same_ast evidence, not blind discovery.
    spec = get_demo("arrhenius")
    splits = spec.make_splits(points=24, seed=0)
    compiled = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
        {spec.variable: splits[0].inputs[spec.variable]},
    )
    result = fit_warm_started_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(depth=compiled.metadata.depth, variables=(spec.variable,), steps=1, restarts=1, seed=0),
        compiled.expression,
        perturbation_config=PerturbationConfig(seed=0, noise_scale=0.0),
        verification_splits=splits,
        compiler_metadata=compiled.metadata.as_dict(),
    )

    assert result.status == "same_ast_return"
    assert result.verification is not None
    assert result.verification.status == "recovered"
    assert result.manifest["status"] == "same_ast_return"
    assert result.manifest["diagnosis"]["mechanism"] == "same_ast_return"
    assert result.manifest["diagnosis"]["changed_slot_count"] == 0
    assert result.manifest["compiler_metadata"]["macro_diagnostics"]["hits"] == ["direct_division_template"]


def test_perturbation_is_seeded_and_reports_active_slots():
    spec = get_demo("beer_lambert")
    compiled = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=12, max_nodes=128),
    )
    reports = []
    for _ in range(2):
        tree = SoftEMLTree(compiled.metadata.depth, (spec.variable,), compiled.metadata.constants)
        embedding = tree.embed_expr(compiled.expression, EmbeddingConfig(strength=30.0))
        reports.append(perturb_tree_logits(tree, PerturbationConfig(seed=123, noise_scale=0.01), embedding))

    assert reports[0].as_dict() == reports[1].as_dict()
    assert reports[0].active_slot_changes
    assert {"slot", "embedded_choice", "pre_choice", "post_choice", "changed"} <= set(
        reports[0].active_slot_changes[0]
    )


def test_high_noise_warm_start_records_failure_mechanism():
    spec = get_demo("beer_lambert")
    splits = spec.make_splits(points=24, seed=0)
    compiled = compile_and_validate(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=12, max_nodes=128),
        {spec.variable: splits[0].inputs[spec.variable]},
    )
    result = fit_warm_started_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(depth=compiled.metadata.depth, variables=(spec.variable,), steps=1, restarts=1, seed=0),
        compiled.expression,
        perturbation_config=PerturbationConfig(seed=0, noise_scale=35.0),
        verification_splits=splits,
        compiler_metadata=compiled.metadata.as_dict(),
    )
    diagnosis = result.manifest["diagnosis"]

    assert diagnosis["active_slot_count"] > 0
    assert diagnosis["changed_slot_count"] > 0
    assert diagnosis["mechanism"] == "active_slot_perturbation"
    assert diagnosis["verifier_status"] in {"failed", "recovered"}


def test_cli_warm_start_promotes_beer_lambert_only_after_verification(tmp_path):
    output = tmp_path / "beer-warm.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "beer_lambert",
            "--warm-start-eml",
            "--points",
            "24",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )
    assert "trained_exact_recovery=recovered" in result.stdout
    payload = json.loads(output.read_text())
    assert payload["claim_status"] == "recovered"
    assert payload["stage_statuses"]["catalog_showcase"] == "verified_showcase"
    assert payload["stage_statuses"]["trained_exact_recovery"] == "recovered"


def test_cli_warm_start_promotes_shockley_after_macro_shortening(tmp_path):
    output = tmp_path / "shockley-warm.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "shockley",
            "--warm-start-eml",
            "--points",
            "24",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert "compiled_seed=recovered" in result.stdout
    payload = json.loads(output.read_text())
    assert payload["claim_status"] == "recovered"
    assert payload["stage_statuses"]["compiled_seed"] == "recovered"
    assert payload["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
    assert payload["stage_statuses"]["trained_exact_recovery"] == "recovered"
    assert payload["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["scaled_exp_minus_one_template"]


def test_cli_warm_start_promotes_arrhenius_same_ast_evidence(tmp_path):
    # Benchmark suite v1.9-arrhenius-evidence case arrhenius-warm must classify this as same_ast.
    spec = get_demo("arrhenius")
    assert spec.train_domain == (0.5, 3.0)
    assert spec.heldout_domain == (0.6, 2.7)
    assert spec.extrap_domain == (3.1, 4.2)

    output = tmp_path / "arrhenius-warm.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "arrhenius",
            "--warm-start-eml",
            "--points",
            "24",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert "compiled_seed=recovered" in result.stdout
    assert "trained_exact_recovery=recovered" in result.stdout
    payload = json.loads(output.read_text())
    assert payload["demo"] == "arrhenius"
    assert payload["candidate"]["sympy"] == "exp(-0.8/x)"
    assert payload["claim_status"] == "recovered"
    assert payload["stage_statuses"]["compiled_seed"] == "recovered"
    assert payload["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
    assert payload["stage_statuses"]["trained_exact_recovery"] == "recovered"
    assert payload["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["direct_division_template"]
    assert payload["compiled_eml"]["metadata"]["depth"] == 7
    assert payload["warm_start_eml"]["status"] == "same_ast_return"
    assert payload["warm_start_eml"]["verification"]["status"] == "recovered"
    assert payload["warm_start_eml"]["diagnosis"]["changed_slot_count"] == 0


def test_cli_reports_michaelis_menten_depth_gate_without_promotion(tmp_path):
    output = tmp_path / "mm-warm.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "michaelis_menten",
            "--warm-start-eml",
            "--points",
            "24",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )
    payload = json.loads(output.read_text())
    assert payload["claim_status"] == "verified_showcase"
    assert payload["stage_statuses"]["compiled_seed"] == "unsupported"
    assert payload["warm_start_eml"]["status"] == "unsupported"
    relaxed_macro = payload["compiled_eml"]["diagnostic"]["relaxed"]["metadata"]["macro_diagnostics"]
    assert relaxed_macro["hits"] == ["direct_division_template"]
    assert relaxed_macro["depth_delta"] > 0


def test_cli_reports_planck_as_stretch_without_promotion(tmp_path):
    output = tmp_path / "planck-warm.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "planck",
            "--warm-start-eml",
            "--points",
            "24",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )
    payload = json.loads(output.read_text())
    assert payload["claim_status"] == "verified_showcase"
    assert payload["stage_statuses"]["stretch"] == "reported"
    assert payload["stretch"]["guaranteed_trained_recovery"] is False
    assert payload["warm_start_eml"]["status"] == "unsupported"
    relaxed_macro = payload["compiled_eml"]["diagnostic"]["relaxed"]["metadata"]["macro_diagnostics"]
    assert set(relaxed_macro["hits"]) == {"scaled_exp_minus_one_template", "direct_division_template"}
    assert relaxed_macro["depth_delta"] > 0
