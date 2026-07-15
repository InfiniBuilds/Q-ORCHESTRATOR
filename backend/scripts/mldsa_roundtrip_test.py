import oqs


ALGORITHMS = [
    "ML-DSA-44",
    "ML-DSA-65",
]


def test_mldsa(algorithm: str):
    print(f"\n=== Testing {algorithm} ===")

    message = b"Q-ORCHESTRATOR TEST MESSAGE"

    with oqs.Signature(algorithm) as signer:
        # Generate ML-DSA key pair
        public_key = signer.generate_keypair()

        # Sign original message
        signature = signer.sign(message)

        # Verify original message
        valid = signer.verify(
            message,
            signature,
            public_key,
        )

        # Simulate message tampering
        tampered_message = (
            b"Q-ORCHESTRATOR TAMPERED MESSAGE"
        )

        tampered_valid = signer.verify(
            tampered_message,
            signature,
            public_key,
        )

    if not valid:
        raise RuntimeError(
            f"{algorithm}: valid signature rejected"
        )

    if tampered_valid:
        raise RuntimeError(
            f"{algorithm}: tampered message accepted"
        )

    print("Original verification : PASS")
    print("Tamper detection      : PASS")
    print("Public key size       :", len(public_key), "bytes")
    print("Signature size        :", len(signature), "bytes")


if __name__ == "__main__":
    for algorithm in ALGORITHMS:
        test_mldsa(algorithm)

    print("\nALL ML-DSA ROUND-TRIP TESTS PASSED")
