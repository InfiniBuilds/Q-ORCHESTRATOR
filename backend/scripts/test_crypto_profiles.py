from app.crypto.profiles import (
    CRYPTO_PROFILES,
    SecurityRank,
    get_crypto_profile,
    get_profiles_at_or_above_rank,
)


def test_profile_definitions():
    print("\n=== Testing profile definitions ===")

    p1 = get_crypto_profile("P1_CONSTRAINED")
    p2 = get_crypto_profile("P2_STANDARD")
    p3 = get_crypto_profile("P3_CRITICAL")

    assert p1.mlkem_algorithm == "ML-KEM-512"
    assert p1.hybrid_key_establishment is False
    assert p1.signature_algorithm is None

    assert p2.mlkem_algorithm == "ML-KEM-768"
    assert p2.classical_algorithm == "X25519"
    assert p2.signature_algorithm == "ML-DSA-44"
    assert p2.hybrid_key_establishment is True

    assert p3.mlkem_algorithm == "ML-KEM-1024"
    assert p3.classical_algorithm == "X25519"
    assert p3.signature_algorithm == "ML-DSA-65"
    assert p3.hybrid_key_establishment is True

    print("Profile definitions : PASS")


def test_security_floor():
    print("\n=== Testing security floor eligibility ===")

    constrained_profiles = get_profiles_at_or_above_rank(
        SecurityRank.CONSTRAINED
    )

    standard_profiles = get_profiles_at_or_above_rank(
        SecurityRank.STANDARD
    )

    critical_profiles = get_profiles_at_or_above_rank(
        SecurityRank.CRITICAL
    )

    constrained_ids = {
        profile.profile_id
        for profile in constrained_profiles
    }

    standard_ids = {
        profile.profile_id
        for profile in standard_profiles
    }

    critical_ids = {
        profile.profile_id
        for profile in critical_profiles
    }

    assert constrained_ids == {
        "P1_CONSTRAINED",
        "P2_STANDARD",
        "P3_CRITICAL",
    }

    assert standard_ids == {
        "P2_STANDARD",
        "P3_CRITICAL",
    }

    assert critical_ids == {
        "P3_CRITICAL",
    }

    print("CONSTRAINED eligibility :", constrained_ids)
    print("STANDARD eligibility    :", standard_ids)
    print("CRITICAL eligibility    :", critical_ids)
    print("Security floor          : PASS")


def test_unknown_profile():
    print("\n=== Testing unknown profile rejection ===")

    try:
        get_crypto_profile("P0_WEAK")

    except ValueError:
        print("Unknown profile rejection : PASS")
        return

    raise RuntimeError(
        "Unknown profile was incorrectly accepted"
    )


if __name__ == "__main__":
    print("Profiles registered:", len(CRYPTO_PROFILES))

    test_profile_definitions()
    test_security_floor()
    test_unknown_profile()

    print("\nALL CRYPTO PROFILE TESTS PASSED")
