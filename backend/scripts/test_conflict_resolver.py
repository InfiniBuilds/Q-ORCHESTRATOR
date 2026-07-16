from app.crypto.profiles import SecurityRank
from app.orchestration.conflict_resolver import ConflictResolver
from app.orchestration.resource_engine import (
    ResourceCapability,
    ResourceDecision,
)
from app.orchestration.security_engine import (
    SecurityDecision,
    TriggeredRule,
)

resolver = ConflictResolver()


def make_security(rank):
    return SecurityDecision(
        score=1.0,
        required_rank=rank,
        triggered_rule=TriggeredRule.NONE,
        explanation="Test",
    )


def make_resource(capability):
    return ResourceDecision(
        constraint_score=0.5,
        capability=capability,
        explanation="Test",
    )


def test_critical():
    print("\n=== Critical Security ===")

    result = resolver.resolve(
        make_security(SecurityRank.CRITICAL),
        make_resource(ResourceCapability.LOW),
    )

    assert result.recommended_rank == SecurityRank.CRITICAL
    assert result.downgraded is False

    print(result)


def test_standard():
    print("\n=== Standard Security ===")

    result = resolver.resolve(
        make_security(SecurityRank.STANDARD),
        make_resource(ResourceCapability.LOW),
    )

    assert result.recommended_rank == SecurityRank.STANDARD
    assert result.downgraded is False

    print(result)


def test_constrained_high_resources():
    print("\n=== Constrained + High Resources ===")

    result = resolver.resolve(
        make_security(SecurityRank.CONSTRAINED),
        make_resource(ResourceCapability.HIGH),
    )

    assert result.recommended_rank == SecurityRank.STANDARD

    print(result)


def test_constrained_low_resources():
    print("\n=== Constrained + Low Resources ===")

    result = resolver.resolve(
        make_security(SecurityRank.CONSTRAINED),
        make_resource(ResourceCapability.LOW),
    )

    assert result.recommended_rank == SecurityRank.CONSTRAINED

    print(result)


if __name__ == "__main__":

    test_critical()

    test_standard()

    test_constrained_high_resources()

    test_constrained_low_resources()

    print("\nALL CONFLICT RESOLVER TESTS PASSED")
