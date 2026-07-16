import time

from app.crypto.hybrid_kem import HybridKeyEstablishment

ITERATIONS = 100

CONFIGS = [
    ("P2_STANDARD", "ML-KEM-768"),
    ("P3_CRITICAL", "ML-KEM-1024"),
]


def benchmark(profile_id, mlkem_algorithm):

    handshake = []

    hk = HybridKeyEstablishment(
        mlkem_algorithm=mlkem_algorithm,
        hkdf_hash="SHA256",
    )

    for i in range(ITERATIONS):

        start = time.perf_counter()

        result = hk.establish_session(
            profile_id=profile_id,
            domain="BANKING",
            session_id=f"SESSION-{i}",
            salt=b"QORCH-BENCHMARK",
        )

        handshake.append(
            (time.perf_counter() - start) * 1000
        )

        assert (
            result.sender_session_key
            == result.receiver_session_key
        )

    print(f"\n{profile_id}")
    print("-" * 40)

    print(
        f"Average Handshake : "
        f"{sum(handshake)/ITERATIONS:.3f} ms"
    )

    print(
        f"Session Key Size : "
        f"{len(result.sender_session_key)} bytes"
    )

    print(
        f"ML-KEM Ciphertext : "
        f"{result.mlkem_ciphertext_size} bytes"
    )


if __name__ == "__main__":

    print("=" * 50)
    print("HYBRID HANDSHAKE BENCHMARK")
    print("=" * 50)

    for profile_id, algorithm in CONFIGS:
        benchmark(profile_id, algorithm)
