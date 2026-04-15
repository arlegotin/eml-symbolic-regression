"""Paper claim and proof-threshold contracts for v1.5 evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


CLAIM_CLASSES = {
    "contract_context": "contract_context",
    "bounded_training_proof": "bounded_training_proof",
    "measured_depth_curve": "measured_depth_curve",
    "catalog_verification": "catalog_verification",
    "compile_only_verification": "compile_only_verification",
}

TRAINING_MODES = {
    "catalog_verification": "catalog_verification",
    "compile_only_verification": "compile_only_verification",
    "blind_training": "blind_training",
    "compiler_warm_start_training": "compiler_warm_start_training",
    "perturbed_true_tree_training": "perturbed_true_tree_training",
}

EVIDENCE_CLASSES = {
    "catalog_verified": "catalog_verified",
    "compile_only_verified": "compile_only_verified",
    "blind_training_recovered": "blind_training_recovered",
    "compiler_warm_start_recovered": "compiler_warm_start_recovered",
    "perturbed_true_tree_recovered": "perturbed_true_tree_recovered",
    "repaired_candidate": "repaired_candidate",
    "unsupported": "unsupported",
    "failed": "failed",
    "snapped_but_failed": "snapped_but_failed",
    "soft_fit_only": "soft_fit_only",
    "same_ast": "same_ast",
    "verified_equivalent": "verified_equivalent",
    "execution_failure": "execution_failure",
}

_POLICY_TYPES = ("bounded_rate", "measured_rate", "context_only")


class ProofContractError(ValueError):
    """Raised when proof metadata cannot be trusted."""

    def __init__(self, reason: str, detail: str, *, path: str | None = None) -> None:
        self.reason = reason
        self.detail = detail
        self.path = path
        location = f" at {path}" if path else ""
        super().__init__(f"{reason}{location}: {detail}")

    def as_dict(self) -> dict[str, str]:
        payload = {"reason": self.reason, "detail": self.detail}
        if self.path is not None:
            payload["path"] = self.path
        return payload


@dataclass(frozen=True)
class ThresholdPolicy:
    id: str
    description: str
    policy_type: str
    required_rate: float | None
    allowed_evidence_classes: tuple[str, ...]
    fail_on_unsupported: bool
    fail_on_execution_error: bool

    def validate(self, path: str = "threshold_policy") -> None:
        if not self.id:
            raise ProofContractError("malformed_threshold_policy", "policy id must not be empty", path=f"{path}.id")
        if self.policy_type not in _POLICY_TYPES:
            raise ProofContractError(
                "malformed_threshold_policy",
                f"policy_type must be one of: {', '.join(_POLICY_TYPES)}",
                path=f"{path}.policy_type",
            )
        if self.required_rate is not None and not 0.0 <= self.required_rate <= 1.0:
            raise ProofContractError("malformed_threshold_policy", "required_rate must be between 0.0 and 1.0", path=f"{path}.required_rate")
        if self.policy_type == "bounded_rate" and self.required_rate is None:
            raise ProofContractError("malformed_threshold_policy", "bounded_rate policies require required_rate", path=f"{path}.required_rate")
        if self.policy_type != "bounded_rate" and self.required_rate is not None:
            raise ProofContractError(
                "malformed_threshold_policy",
                "non-bounded policies must not define required_rate",
                path=f"{path}.required_rate",
            )
        unknown = sorted(set(self.allowed_evidence_classes) - set(EVIDENCE_CLASSES.values()))
        if unknown:
            raise ProofContractError(
                "malformed_threshold_policy",
                f"unknown evidence classes: {', '.join(unknown)}",
                path=f"{path}.allowed_evidence_classes",
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "policy_type": self.policy_type,
            "required_rate": self.required_rate,
            "allowed_evidence_classes": list(self.allowed_evidence_classes),
            "fail_on_unsupported": self.fail_on_unsupported,
            "fail_on_execution_error": self.fail_on_execution_error,
        }


@dataclass(frozen=True)
class PaperClaim:
    id: str
    statement: str
    source_refs: tuple[str, ...]
    claim_class: str
    suite_ids: tuple[str, ...]
    case_ids: tuple[str, ...]
    threshold_policy_id: str
    notes: tuple[str, ...] = ()

    def validate(self, path: str = "claim") -> None:
        if not self.id:
            raise ProofContractError("malformed_claim", "claim id must not be empty", path=f"{path}.id")
        if not self.statement:
            raise ProofContractError("malformed_claim", "claim statement must not be empty", path=f"{path}.statement")
        if not self.source_refs:
            raise ProofContractError("malformed_claim", "source_refs must not be empty", path=f"{path}.source_refs")
        if self.claim_class not in CLAIM_CLASSES.values():
            raise ProofContractError("malformed_claim", f"unknown claim_class {self.claim_class!r}", path=f"{path}.claim_class")
        try:
            threshold_policy(self.threshold_policy_id)
        except ProofContractError as exc:
            raise ProofContractError(exc.reason, exc.detail, path=f"{path}.threshold_policy_id") from exc

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "source_refs": list(self.source_refs),
            "claim_class": self.claim_class,
            "suite_ids": list(self.suite_ids),
            "case_ids": list(self.case_ids),
            "threshold_policy_id": self.threshold_policy_id,
            "notes": list(self.notes),
        }


def threshold_policies() -> dict[str, ThresholdPolicy]:
    policies = {
        "bounded_100_percent": ThresholdPolicy(
            id="bounded_100_percent",
            description="Declared bounded proof suites pass only at 100% verifier-owned training recovery.",
            policy_type="bounded_rate",
            required_rate=1.0,
            allowed_evidence_classes=(
                EVIDENCE_CLASSES["blind_training_recovered"],
                EVIDENCE_CLASSES["compiler_warm_start_recovered"],
                EVIDENCE_CLASSES["perturbed_true_tree_recovered"],
                EVIDENCE_CLASSES["repaired_candidate"],
                EVIDENCE_CLASSES["verified_equivalent"],
            ),
            fail_on_unsupported=True,
            fail_on_execution_error=True,
        ),
        "measured_depth_curve": ThresholdPolicy(
            id="measured_depth_curve",
            description="Depth-curve suites report measured recovery by depth without requiring universal blind recovery.",
            policy_type="measured_rate",
            required_rate=None,
            allowed_evidence_classes=(
                EVIDENCE_CLASSES["blind_training_recovered"],
                EVIDENCE_CLASSES["compiler_warm_start_recovered"],
                EVIDENCE_CLASSES["perturbed_true_tree_recovered"],
                EVIDENCE_CLASSES["repaired_candidate"],
                EVIDENCE_CLASSES["verified_equivalent"],
                EVIDENCE_CLASSES["same_ast"],
                EVIDENCE_CLASSES["soft_fit_only"],
                EVIDENCE_CLASSES["snapped_but_failed"],
                EVIDENCE_CLASSES["failed"],
                EVIDENCE_CLASSES["unsupported"],
                EVIDENCE_CLASSES["execution_failure"],
            ),
            fail_on_unsupported=False,
            fail_on_execution_error=False,
        ),
        "contract_context": ThresholdPolicy(
            id="contract_context",
            description="Representation-context claim used to label proof suites; it is not a recovery threshold.",
            policy_type="context_only",
            required_rate=None,
            allowed_evidence_classes=(),
            fail_on_unsupported=False,
            fail_on_execution_error=False,
        ),
    }
    for policy_id, policy in policies.items():
        policy.validate(f"threshold_policies.{policy_id}")
    return policies


def threshold_policy(policy_id: str) -> ThresholdPolicy:
    policies = threshold_policies()
    try:
        return policies[policy_id]
    except KeyError as exc:
        available = ", ".join(policies)
        raise ProofContractError(
            "unknown_threshold_policy",
            f"{policy_id!r} is not one of: {available}",
            path="threshold_policy_id",
        ) from exc


def claim_matrix() -> dict[str, PaperClaim]:
    claims = {
        "paper-complete-depth-bounded-search": PaperClaim(
            id="paper-complete-depth-bounded-search",
            statement=(
                "EML trees form a complete depth-bounded representation family for the paper's elementary-function basis; "
                "this is context for proof suites, not a training-recovery pass condition."
            ),
            source_refs=("sources/paper.pdf", "sources/NORTH_STAR.md", ".planning/REQUIREMENTS.md", ".planning/ROADMAP.md"),
            claim_class=CLAIM_CLASSES["contract_context"],
            suite_ids=("proof-shallow-blind", "proof-perturbed-basin", "proof-depth-curve"),
            case_ids=(),
            threshold_policy_id="contract_context",
            notes=(
                "Complete depth-bounded search is represented separately from empirical optimizer success.",
                "Catalog or compile-only validation cannot satisfy bounded training-proof claims.",
            ),
        ),
        "paper-shallow-blind-recovery": PaperClaim(
            id="paper-shallow-blind-recovery",
            statement=(
                "For a declared shallow suite, blind training must recover all formulas through verifier-owned held-out, "
                "extrapolation, and high-precision checks."
            ),
            source_refs=("sources/paper.pdf", "sources/NORTH_STAR.md", ".planning/REQUIREMENTS.md", ".planning/ROADMAP.md"),
            claim_class=CLAIM_CLASSES["bounded_training_proof"],
            suite_ids=("proof-shallow-blind",),
            case_ids=("exp", "log", "radioactive_decay", "scaled_exponential_family"),
            threshold_policy_id="bounded_100_percent",
            notes=(
                "The bounded suite target is 100% recovery over declared cases only.",
                "The current radioactive_decay blind failure remains visible for Phase 30 repair.",
            ),
        ),
        "paper-perturbed-true-tree-basin": PaperClaim(
            id="paper-perturbed-true-tree-basin",
            statement=(
                "For declared true-tree perturbation bounds, training from perturbed correct EML trees must return "
                "verifier-owned recovered or verified-equivalent candidates at 100% rate."
            ),
            source_refs=("sources/paper.pdf", "sources/NORTH_STAR.md", ".planning/REQUIREMENTS.md", ".planning/ROADMAP.md"),
            claim_class=CLAIM_CLASSES["bounded_training_proof"],
            suite_ids=("proof-perturbed-basin",),
            case_ids=("synthetic_true_tree_depths", "beer_lambert_perturbation"),
            threshold_policy_id="bounded_100_percent",
            notes=(
                "Same-AST return is tracked separately and is not by itself bounded training proof.",
                "Phase 31 owns the exact perturbation inventory and noise bounds.",
            ),
        ),
        "paper-blind-depth-degradation": PaperClaim(
            id="paper-blind-depth-degradation",
            statement=(
                "Blind recovery is expected to degrade with increasing EML depth; deeper blind failures are measured "
                "evidence rather than regressions against a universal 100% target."
            ),
            source_refs=("sources/paper.pdf", "sources/NORTH_STAR.md", ".planning/REQUIREMENTS.md", ".planning/ROADMAP.md"),
            claim_class=CLAIM_CLASSES["measured_depth_curve"],
            suite_ids=("proof-depth-curve",),
            case_ids=("depth_2", "depth_3", "depth_4", "depth_5", "depth_6"),
            threshold_policy_id="measured_depth_curve",
            notes=(
                "The paper reports rapid blind-depth degradation, including no depth-6 blind recovery in its reported attempts.",
                "Depth-curve reports must not present expected deep blind failures as product regressions.",
            ),
        ),
    }
    for claim_id, claim in claims.items():
        claim.validate(f"claim_matrix.{claim_id}")
    return claims


def paper_claim(claim_id: str) -> PaperClaim:
    claims = claim_matrix()
    try:
        return claims[claim_id]
    except KeyError as exc:
        available = ", ".join(claims)
        raise ProofContractError("unknown_claim", f"{claim_id!r} is not one of: {available}", path="claim_id") from exc


def list_claims() -> list[PaperClaim]:
    return list(claim_matrix().values())


def validate_claim_reference(claim_id: str, threshold_policy_id: str, path: str = "claim") -> PaperClaim:
    claim = paper_claim(claim_id)
    policy = threshold_policy(threshold_policy_id)
    if claim.threshold_policy_id != policy.id:
        raise ProofContractError(
            "threshold_mismatch",
            f"claim {claim.id!r} requires threshold policy {claim.threshold_policy_id!r}, got {policy.id!r}",
            path=f"{path}.threshold_policy_id",
        )
    return claim
