from app.orchestration.context import (
    Domain,
    ResourceContext,
    SecurityContext,
    UnifiedContext,
)
from app.orchestration.resource_engine import (
    ResourceConstraintEngine,
    ResourceCapability,
)

engine = ResourceConstraintEngine()


def create_context(cpu, memory, energy, bandwidth, latency):
    return UnifiedContext(
        context_id="RESOURCE-TEST",
        domain=Domain.IOT,
        security=SecurityContext(
            criticality=0.5,
            sensitivity=0.5,
            anomaly_score=0.2,
            trust_deficit=0.2,
            exposure=0.2,
        ),
        resources=ResourceContext(
            cpu_constraint=cpu,
            memory_constraint=memory,
            energy_constraint=energy,
            bandwidth_constraint=bandwidth,
            latency_constraint=latency,
        ),
    )


def test_high_capability():
    print("\n=== High Capability ===")

    decision = engine.evaluate(
        create_context(
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
        )
    )

    assert decision.capability == ResourceCapability.HIGH

    print(decision)


def test_medium_capability():
    print("\n=== Medium Capability ===")

    decision = engine.evaluate(
        create_context(
            0.50,
            0.50,
            0.40,
            0.40,
            0.30,
        )
    )

    assert decision.capability == ResourceCapability.MEDIUM

    print(decision)


def test_low_capability():
    print("\n=== Low Capability ===")

    decision = engine.evaluate(
        create_context(
            0.90,
            0.90,
            0.95,
            0.85,
            0.80,
        )
    )

    assert decision.capability == ResourceCapability.LOW

    print(decision)


if __name__ == "__main__":
    test_high_capability()
    test_medium_capability()
    test_low_capability()

    print("\nALL RESOURCE ENGINE TESTS PASSED")
