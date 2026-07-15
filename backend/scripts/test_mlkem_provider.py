from app.crypto.providers.mlkem_provider import MLKEMProvider


ALGORITHMS = [
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024",
]


def test_provider(algorithm: str):
    print(f"\n=== Testing MLKEMProvider: {algorithm} ===")

    provider = MLKEMProvider(algorithm)

    receiver_keypair = provider.generate_keypair()

    sender_result = provider.encapsulate(
        receiver_keypair.public_key
    )

    receiver_secret = provider.decapsulate(
        secret_key=receiver_keypair.secret_key,
        ciphertext=sender_result.ciphertext,
    )

    if sender_result.shared_secret != receiver_secret:
        raise RuntimeError(
            f"{algorithm}: shared secret mismatch"
        )

    print("Provider round trip : PASS")
    print(
        "Public key size     :",
        len(receiver_keypair.public_key),
        "bytes",
    )
    print(
        "Secret key size     :",
        len(receiver_keypair.secret_key),
        "bytes",
    )
    print(
        "Ciphertext size     :",
        len(sender_result.ciphertext),
        "bytes",
    )


if __name__ == "__main__":
    for algorithm in ALGORITHMS:
        test_provider(algorithm)

    print("\nALL MLKEM PROVIDER TESTS PASSED")
