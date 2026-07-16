from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityWeights:
    criticality: float = 0.30
    sensitivity: float = 0.25
    anomaly: float = 0.20
    trust_deficit: float = 0.15
    exposure: float = 0.10


@dataclass(frozen=True)
class SecurityThresholds:
    criticality_override: float = 0.95
    anomaly_override: float = 0.90

    trust_override: float = 0.85
    exposure_override: float = 0.80

    sensitivity_override: float = 0.90
    anomaly_attack_override: float = 0.60

    constrained_max: float = 0.35
    standard_max: float = 0.70


DEFAULT_SECURITY_WEIGHTS = SecurityWeights()

DEFAULT_SECURITY_THRESHOLDS = SecurityThresholds()
