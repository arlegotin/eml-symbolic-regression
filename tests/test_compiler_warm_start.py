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
)
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.master_tree import EmbeddingConfig, EmbeddingError, SoftEMLTree
from eml_symbolic_regression.optimize import TrainingConfig
from eml_symbolic_regression.warm_start import PerturbationConfig, fit_warm_started_eml_tree


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
