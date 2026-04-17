"""Hybrid symbolic regression over complete EML trees."""

from .compiler import CompilerConfig, CompileResult, UnsupportedExpression, compile_and_validate, compile_sympy_expression
from .expression import CenteredEml, Const, Eml, Expr, SympyCandidate, Var, ceml_expr, ceml_s_expr, exp_expr, log_expr, zeml_s_expr
from .master_tree import EmbeddingConfig, SoftEMLTree, embed_expr_into_tree
from .semantics import (
    EmlOperator,
    ceml_operator,
    ceml_s_operator,
    centered_eml_numpy,
    centered_eml_torch,
    eml_numpy,
    eml_operator_from_spec,
    eml_torch,
    raw_eml_operator,
    zeml_s_operator,
)
from .verify import VerificationReport, verify_candidate
from .witnesses import (
    CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING,
    ScaffoldPlan,
    ScaffoldWitness,
    known_scaffold_kinds,
    list_scaffold_witnesses,
    resolve_scaffold_plan,
    scaffold_witness_for,
)

__all__ = [
    "CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING",
    "Const",
    "CenteredEml",
    "CompilerConfig",
    "CompileResult",
    "Eml",
    "EmlOperator",
    "EmbeddingConfig",
    "Expr",
    "ScaffoldPlan",
    "ScaffoldWitness",
    "SoftEMLTree",
    "SympyCandidate",
    "UnsupportedExpression",
    "Var",
    "VerificationReport",
    "ceml_expr",
    "ceml_operator",
    "ceml_s_expr",
    "ceml_s_operator",
    "centered_eml_numpy",
    "centered_eml_torch",
    "compile_and_validate",
    "compile_sympy_expression",
    "eml_numpy",
    "eml_operator_from_spec",
    "eml_torch",
    "embed_expr_into_tree",
    "exp_expr",
    "known_scaffold_kinds",
    "list_scaffold_witnesses",
    "log_expr",
    "raw_eml_operator",
    "resolve_scaffold_plan",
    "scaffold_witness_for",
    "verify_candidate",
    "zeml_s_expr",
    "zeml_s_operator",
]
