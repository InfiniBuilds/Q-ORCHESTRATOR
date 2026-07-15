from app.crypto.providers.mldsa_provider import MLDSAProvider


ALGORITHMS = [
    "ML-DSA-44",
    "ML-DSA-65",
]


def test_provider(algorithm: str):
    print(f"\n=== Testing MLDSAProvider: {algorithm} ===")

    provider = MLDSAProvider(algorithm)

    keypair = provider.generate_keypair()

    original_message = (
        b"TRANSFER:50000:INR:USER001:USER002"
    )

    signature_result = provider.sign(
        secret_key=keypair.secret_key,
        message=original_message,
    )

    valid = provider.verify(
        public_key=keypair.public_key,
        message=original_message,
        signature=signature_result.signature,
    )

    tampered_message = (
        b"TRANSFER:500000:INR:USER001:USER002"
    )

    tampered_valid = provider.verify(
        public_key=keypair.public_key,
        message=tampered_message,
        signature=signature_result.signature,
    )

    if not valid:
        raise RuntimeError(
            f"{algorithm}: valid signature rejected"
        )

    if tampered_valid:
        raise RuntimeError(
            f"{algorithm}: tampered message accepted"
        )

    print("Valid signature      : PASS")
    print("Tamper rejection     : PASS")
    print(
        "Public key size      :",
        len(keypair.public_key),
        "bytes",
    )
    print(
        "Secret key size      :",
        len(keypair.secret_key),
        "bytes",
    )
    print(
        "Signature size       :",
        len(signature_result.signature),
        "bytes",
    )


if __name__ == "__main__":
    for algorithm in ALGORITHMS:
        test_provider(algorithm)

    print("\nALL MLDSA PROVIDER TESTS PASSED")
