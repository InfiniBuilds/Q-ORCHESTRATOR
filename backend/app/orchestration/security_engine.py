from dataclasses import dataclass
from enum import Enum

from app.crypto.profiles import SecurityRank
from app.orchestration.context import UnifiedContext
from app.orchestration.security_policy import (
    DEFAULT_SECURITY_THRESHOLDS,
    DEFAULT_SECURITY_WEIGHTS,
)


class TriggeredRule(str, Enum):
    NONE = "NONE"
    HIGH_CRITICALITY = "HIGH_CRITICALITY"
    HIGH_ANOMALY = "HIGH_ANOMALY"
    LOW_TRUST_HIGH_EXPOSURE = "LOW_TRUST_HIGH_EXPOSURE"
    HIGH_SENSITIVITY_ATTACK = "HIGH_SENSITIVITY_ATTACK"


@dataclass(frozen=True)
class SecurityDecision:
    score: float
    required_rank: SecurityRank
    triggered_rule: TriggeredRule
    explanation: str


class SecurityRequirementEngine:
    """
    Evaluates the required security level for a request.

    Evaluation strategy:
    1. Hard security policy overrides
    2. Weighted security scoring
    """

    def __init__(
        self,
        weights=DEFAULT_SECURITY_WEIGHTS,
        thresholds=DEFAULT_SECURITY_THRESHOLDS,
    ):
        self.weights = weights
        self.thresholds = thresholds

    def evaluate(
        self,
        context: UnifiedContext,
    ) -> SecurityDecision:

        security = context.security

        # ------------------------------------------------
        # HARD POLICY RULES
        # ------------------------------------------------

        if (
            security.criticality
            >= self.thresholds.criticality_override
        ):
            return SecurityDecision(
                score=1.0,
                required_rank=SecurityRank.CRITICAL,
                triggered_rule=TriggeredRule.HIGH_CRITICALITY,
                explanation="Critical operation requires highest security.",
            )

        if (
            security.anomaly_score
            >= self.thresholds.anomaly_override
        ):
            return SecurityDecision(
                score=1.0,
                required_rank=SecurityRank.CRITICAL,
                triggered_rule=TriggeredRule.HIGH_ANOMALY,
                explanation="Severe anomaly detected.",
            )

        if (
            security.trust_deficit
            >= self.thresholds.trust_override
            and security.exposure
            >= self.thresholds.exposure_override
        ):
            return SecurityDecision(
                score=1.0,
                required_rank=SecurityRank.CRITICAL,
                triggered_rule=TriggeredRule.LOW_TRUST_HIGH_EXPOSURE,
                explanation="Untrusted entity on highly exposed network.",
            )

        if (
            security.sensitivity
            >= self.thresholds.sensitivity_override
            and security.anomaly_score
            >= self.thresholds.anomaly_attack_override
        ):
            return SecurityDecision(
                score=1.0,
                required_rank=SecurityRank.CRITICAL,
                triggered_rule=TriggeredRule.HIGH_SENSITIVITY_ATTACK,
                explanation="Sensitive asset under suspicious activity.",
            )

        # ------------------------------------------------
        # WEIGHTED SECURITY SCORE
        # ------------------------------------------------

        score = (
            security.criticality
            * self.weights.criticality
            + security.sensitivity
            * self.weights.sensitivity
            + security.anomaly_score
            * self.weights.anomaly
            + security.trust_deficit
            * self.weights.trust_deficit
            + security.exposure
            * self.weights.exposure
        )

        if score < self.thresholds.constrained_max:
            rank = SecurityRank.CONSTRAINED

        elif score < self.thresholds.standard_max:
            rank = SecurityRank.STANDARD

        else:
            rank = SecurityRank.CRITICAL

        return SecurityDecision(
            score=round(score, 3),
            required_rank=rank,
            triggered_rule=TriggeredRule.NONE,
            explanation="Weighted policy evaluation.",
        )
