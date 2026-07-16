from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceWeights:
    cpu: float = 0.30
    memory: float = 0.25
    energy: float = 0.20
    bandwidth: float = 0.15
    latency: float = 0.10


@dataclass(frozen=True)
class ResourceThresholds:
    high_capability_max: float = 0.35
    medium_capability_max: float = 0.70


DEFAULT_RESOURCE_WEIGHTS = ResourceWeights()

DEFAULT_RESOURCE_THRESHOLDS = ResourceThresholds()
