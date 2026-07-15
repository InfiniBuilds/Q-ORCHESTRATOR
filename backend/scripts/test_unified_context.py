from app.orchestration.context import (
    Domain,
    ResourceContext,
    SecurityContext,
    UnifiedContext,
)


def test_banking_context():
    print("\n=== Testing banking unified context ===")

    context = UnifiedContext(
        context_id="BANK-TXN-001",
        domain=Domain.BANKING,
        security=SecurityContext(
            criticality=0.90,
            sensitivity=0.95,
            anomaly_score=0.70,
            trust_deficit=0.20,
            exposure=0.80,
        ),
        resources=ResourceContext(
            cpu_constraint=0.10,
            memory_constraint=0.10,
            energy_constraint=0.00,
            bandwidth_constraint=0.10,
            latency_constraint=0.30,
        ),
    )

    assert context.domain == Domain.BANKING
    assert context.security.criticality == 0.90

    print("Banking context creation : PASS")


def test_iot_context():
    print("\n=== Testing IoT unified context ===")

    context = UnifiedContext(
        context_id="IOT-DEVICE-001",
        domain=Domain.IOT,
        security=SecurityContext(
            criticality=0.30,
            sensitivity=0.40,
            anomaly_score=0.10,
            trust_deficit=0.10,
            exposure=0.60,
        ),
        resources=ResourceContext(
            cpu_constraint=0.80,
            memory_constraint=0.90,
            energy_constraint=0.95,
            bandwidth_constraint=0.85,
            latency_constraint=0.50,
        ),
    )

    assert context.domain == Domain.IOT
    assert context.resources.energy_constraint == 0.95

    print("IoT context creation     : PASS")


def test_invalid_context():
    print("\n=== Testing invalid score rejection ===")

    try:
        UnifiedContext(
            context_id="INVALID-001",
            domain=Domain.IOT,
            security=SecurityContext(
                criticality=1.50,
                sensitivity=0.40,
                anomaly_score=0.10,
                trust_deficit=0.10,
                exposure=0.60,
            ),
            resources=ResourceContext(
                cpu_constraint=0.80,
                memory_constraint=0.90,
                energy_constraint=0.95,
                bandwidth_constraint=0.85,
                latency_constraint=0.50,
            ),
        )

    except ValueError as exc:
        print("Invalid score rejection :", exc)
        print("Validation              : PASS")
        return

    raise RuntimeError(
        "Invalid normalized value was accepted"
    )


if __name__ == "__main__":
    test_banking_context()
    test_iot_context()
    test_invalid_context()

    print("\nALL UNIFIED CONTEXT TESTS PASSED")
