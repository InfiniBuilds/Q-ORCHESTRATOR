from dataclasses import dataclass
from enum import Enum


class Domain(str, Enum):
    BANKING = "BANKING"
    IOT = "IOT"


@dataclass(frozen=True)
class SecurityContext:
    criticality: float
    sensitivity: float
    anomaly_score: float
    trust_deficit: float
    exposure: float


@dataclass(frozen=True)
class ResourceContext:
    cpu_constraint: float
    memory_constraint: float
    energy_constraint: float
    bandwidth_constraint: float
    latency_constraint: float


@dataclass(frozen=True)
class UnifiedContext:
    context_id: str
    domain: Domain

    security: SecurityContext
    resources: ResourceContext

    def __post_init__(self):
        if not self.context_id:
            raise ValueError(
                "context_id is required"
            )

        self._validate_normalized_values()

    def _validate_normalized_values(self) -> None:
        values = {
            "criticality": self.security.criticality,
            "sensitivity": self.security.sensitivity,
            "anomaly_score": self.security.anomaly_score,
            "trust_deficit": self.security.trust_deficit,
            "exposure": self.security.exposure,
            "cpu_constraint": self.resources.cpu_constraint,
            "memory_constraint": self.resources.memory_constraint,
            "energy_constraint": self.resources.energy_constraint,
            "bandwidth_constraint": (
                self.resources.bandwidth_constraint
            ),
            "latency_constraint": (
                self.resources.latency_constraint
            ),
        }

        for name, value in values.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{name} must be between 0.0 and 1.0"
                )
