import oqs


ALGORITHMS = [
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024",
]


def test_mlkem(algorithm: str):
    print(f"\n=== Testing {algorithm} ===")

    # Receiver creates ML-KEM key pair
    with oqs.KeyEncapsulation(algorithm) as receiver:
        public_key = receiver.generate_keypair()

        # Sender encapsulates using receiver's public key
        with oqs.KeyEncapsulation(algorithm) as sender:
            ciphertext, sender_secret = sender.encap_secret(
                public_key
            )

        # Receiver decapsulates the ciphertext
        receiver_secret = receiver.decap_secret(ciphertext)

    # Both parties must derive the same shared secret
    if sender_secret != receiver_secret:
        raise RuntimeError(
            f"{algorithm}: shared secrets do not match"
        )

    print("Shared secret match : PASS")
    print("Public key size     :", len(public_key), "bytes")
    print("Ciphertext size     :", len(ciphertext), "bytes")
    print("Shared secret size  :", len(sender_secret), "bytes")


if __name__ == "__main__":
    for algorithm in ALGORITHMS:
        test_mlkem(algorithm)

    print("\nALL ML-KEM ROUND-TRIP TESTS PASSED")
