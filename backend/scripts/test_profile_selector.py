from app.crypto.profiles import SecurityRank
from app.orchestration.conflict_resolver import ConflictResolution
from app.orchestration.profile_selector import (
    AdaptiveProfileSelector,
)

selector = AdaptiveProfileSelector()


def create_resolution(rank):
    return ConflictResolution(
        minimum_required_rank=rank,
        recommended_rank=rank,
        downgraded=False,
        explanation="Test",
    )


def test_constrained():
    print("\n=== CONSTRAINED ===")

    selection = selector.select(
        create_resolution(SecurityRank.CONSTRAINED)
    )

    assert (
        selection.profile.profile_id
        == "P1_CONSTRAINED"
    )

    print(selection)


def test_standard():
    print("\n=== STANDARD ===")

    selection = selector.select(
        create_resolution(SecurityRank.STANDARD)
    )

    assert (
        selection.profile.profile_id
        == "P2_STANDARD"
    )

    print(selection)


def test_critical():
    print("\n=== CRITICAL ===")

    selection = selector.select(
        create_resolution(SecurityRank.CRITICAL)
    )

    assert (
        selection.profile.profile_id
        == "P3_CRITICAL"
    )

    print(selection)


if __name__ == "__main__":

    test_constrained()

    test_standard()

    test_critical()

    print("\nALL PROFILE SELECTOR TESTS PASSED")
