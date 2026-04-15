"""Hybrid symbolic regression over complete EML trees."""

from .compiler import CompilerConfig, CompileResult, UnsupportedExpression, compile_and_validate, compile_sympy_expression
from .expression import Const, Eml, Expr, SympyCandidate, Var, exp_expr, log_expr
from .master_tree import EmbeddingConfig, SoftEMLTree, embed_expr_into_tree
from .semantics import eml_numpy, eml_torch
from .verify import VerificationReport, verify_candidate

__all__ = [
    "Const",
    "CompilerConfig",
    "CompileResult",
    "Eml",
    "EmbeddingConfig",
    "Expr",
    "SoftEMLTree",
    "SympyCandidate",
    "UnsupportedExpression",
    "Var",
    "VerificationReport",
    "compile_and_validate",
    "compile_sympy_expression",
    "eml_numpy",
    "eml_torch",
    "embed_expr_into_tree",
    "exp_expr",
    "log_expr",
    "verify_candidate",
]
