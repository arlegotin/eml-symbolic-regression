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

__all__ = [
    "Const",
    "CenteredEml",
    "CompilerConfig",
    "CompileResult",
    "Eml",
    "EmlOperator",
    "EmbeddingConfig",
    "Expr",
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
    "log_expr",
    "raw_eml_operator",
    "verify_candidate",
    "zeml_s_expr",
    "zeml_s_operator",
]
