from app.orchestration.context import (
    Domain,
    ResourceContext,
    SecurityContext,
    UnifiedContext,
)
from app.orchestration.security_engine import (
    SecurityRequirementEngine,
    TriggeredRule,
)
from app.crypto.profiles import SecurityRank


engine = SecurityRequirementEngine()


def create_context(
    criticality,
    sensitivity,
    anomaly,
    trust,
    exposure,
):
    return UnifiedContext(
        context_id="TEST-001",
        domain=Domain.BANKING,
        security=SecurityContext(
            criticality=criticality,
            sensitivity=sensitivity,
            anomaly_score=anomaly,
            trust_deficit=trust,
            exposure=exposure,
        ),
        resources=ResourceContext(
            cpu_constraint=0.20,
            memory_constraint=0.20,
            energy_constraint=0.00,
            bandwidth_constraint=0.20,
            latency_constraint=0.20,
        ),
    )


def test_rule_criticality():
    print("\n=== Rule 1 : High Criticality ===")

    decision = engine.evaluate(
        create_context(
            0.98,
            0.50,
            0.20,
            0.20,
            0.20,
        )
    )

    assert decision.required_rank == SecurityRank.CRITICAL
    assert decision.triggered_rule == TriggeredRule.HIGH_CRITICALITY

    print(decision)


def test_rule_anomaly():
    print("\n=== Rule 2 : High Anomaly ===")

    decision = engine.evaluate(
        create_context(
            0.40,
            0.40,
            0.95,
            0.20,
            0.30,
        )
    )

    assert decision.required_rank == SecurityRank.CRITICAL
    assert decision.triggered_rule == TriggeredRule.HIGH_ANOMALY

    print(decision)


def test_rule_trust():
    print("\n=== Rule 3 : Low Trust + High Exposure ===")

    decision = engine.evaluate(
        create_context(
            0.30,
            0.40,
            0.30,
            0.90,
            0.90,
        )
    )

    assert decision.required_rank == SecurityRank.CRITICAL
    assert (
        decision.triggered_rule
        == TriggeredRule.LOW_TRUST_HIGH_EXPOSURE
    )

    print(decision)


def test_rule_sensitive():
    print("\n=== Rule 4 : Sensitive Asset Under Attack ===")

    decision = engine.evaluate(
        create_context(
            0.50,
            0.95,
            0.70,
            0.20,
            0.20,
        )
    )

    assert decision.required_rank == SecurityRank.CRITICAL
    assert (
        decision.triggered_rule
        == TriggeredRule.HIGH_SENSITIVITY_ATTACK
    )

    print(decision)


def test_weighted():
    print("\n=== Weighted Evaluation ===")

    decision = engine.evaluate(
        create_context(
            0.50,
            0.50,
            0.30,
            0.20,
            0.20,
        )
    )

    assert decision.triggered_rule == TriggeredRule.NONE
    assert decision.required_rank == SecurityRank.STANDARD

    print(decision)


if __name__ == "__main__":

    test_rule_criticality()

    test_rule_anomaly()

    test_rule_trust()

    test_rule_sensitive()

    test_weighted()

    print("\nALL SECURITY ENGINE TESTS PASSED")
