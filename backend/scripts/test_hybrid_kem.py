import os

from app.crypto.hybrid_kem import HybridKeyEstablishment


CONFIGURATIONS = [
    (
        "P2_STANDARD",
        "ML-KEM-768",
        "SHA384",
    ),
    (
        "P3_CRITICAL",
        "ML-KEM-1024",
        "SHA384",
    ),
]


def test_hybrid(
    profile_id: str,
    mlkem_algorithm: str,
    hkdf_hash: str,
):
    print(f"\n=== Testing {profile_id} ===")

    hybrid = HybridKeyEstablishment(
        mlkem_algorithm=mlkem_algorithm,
        hkdf_hash=hkdf_hash,
    )

    result = hybrid.establish_session(
        profile_id=profile_id,
        domain="BANKING",
        session_id="TEST-SESSION-001",
        salt=os.urandom(32),
    )

    if result.sender_session_key != result.receiver_session_key:
        raise RuntimeError(
            f"{profile_id}: session key mismatch"
        )

    if len(result.sender_session_key) != 32:
        raise RuntimeError(
            f"{profile_id}: invalid session key size"
        )

    print("Hybrid key match       : PASS")
    print("Session key size       :", len(result.sender_session_key), "bytes")
    print("X25519 public key size :", result.x25519_public_key_size, "bytes")
    print("ML-KEM public key size :", result.mlkem_public_key_size, "bytes")
    print("ML-KEM ciphertext size :", result.mlkem_ciphertext_size, "bytes")


if __name__ == "__main__":
    for configuration in CONFIGURATIONS:
        test_hybrid(*configuration)

    print("\nALL HYBRID KEY ESTABLISHMENT TESTS PASSED")
