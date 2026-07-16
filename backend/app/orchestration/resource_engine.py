from dataclasses import dataclass
from enum import Enum

from app.orchestration.context import UnifiedContext
from app.orchestration.resource_policy import (
    DEFAULT_RESOURCE_THRESHOLDS,
    DEFAULT_RESOURCE_WEIGHTS,
)


class ResourceCapability(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class ResourceDecision:
    constraint_score: float
    capability: ResourceCapability
    explanation: str


class ResourceConstraintEngine:

    def __init__(
        self,
        weights=DEFAULT_RESOURCE_WEIGHTS,
        thresholds=DEFAULT_RESOURCE_THRESHOLDS,
    ):
        self.weights = weights
        self.thresholds = thresholds

    def evaluate(
        self,
        context: UnifiedContext,
    ) -> ResourceDecision:

        resources = context.resources

        score = (
            resources.cpu_constraint * self.weights.cpu
            + resources.memory_constraint * self.weights.memory
            + resources.energy_constraint * self.weights.energy
            + resources.bandwidth_constraint * self.weights.bandwidth
            + resources.latency_constraint * self.weights.latency
        )

        score = round(score, 3)

        if score < self.thresholds.high_capability_max:
            capability = ResourceCapability.HIGH

        elif score < self.thresholds.medium_capability_max:
            capability = ResourceCapability.MEDIUM

        else:
            capability = ResourceCapability.LOW

        return ResourceDecision(
            constraint_score=score,
            capability=capability,
            explanation="Weighted resource constraint evaluation.",
        )
