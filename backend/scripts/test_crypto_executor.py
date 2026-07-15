from cryptography.exceptions import InvalidTag

from app.crypto.executor import CryptoExecutor
from app.crypto.profiles import CRYPTO_PROFILES


def test_profile_execution(profile_id: str):
    print(f"\n=== Executing {profile_id} ===")

    profile = CRYPTO_PROFILES[profile_id]

    executor = CryptoExecutor()

    plaintext = (
        b"TRANSFER|AMOUNT=50000|"
        b"CURRENCY=INR|"
        b"FROM=USER001|"
        b"TO=USER002"
    )

    result = executor.execute(
        profile=profile,
        plaintext=plaintext,
        domain="BANKING",
        session_id=f"{profile_id}-TEST-001",
    )

    if (
        result.sender_session_key
        != result.receiver_session_key
    ):
        raise RuntimeError(
            f"{profile_id}: session key mismatch"
        )

    if result.decrypted_plaintext != plaintext:
        raise RuntimeError(
            f"{profile_id}: plaintext mismatch"
        )

    if profile.per_message_signature:
        if result.signature_valid is not True:
            raise RuntimeError(
                f"{profile_id}: signature verification failed"
            )

    print("Session key match       : PASS")
    print("Encryption/decryption   : PASS")

    if profile.per_message_signature:
        print("ML-DSA verification     : PASS")
        print(
            "Signature size          :",
            len(result.signature),
            "bytes",
        )

    else:
        print("Per-message signature   : DISABLED")

    print(
        "Ciphertext size         :",
        len(result.ciphertext),
        "bytes",
    )

    print(
        "ML-KEM ciphertext size  :",
        result.mlkem_ciphertext_size,
        "bytes",
    )


def test_ciphertext_tampering():
    print("\n=== Testing AES-GCM tamper rejection ===")

    profile = CRYPTO_PROFILES["P2_STANDARD"]

    executor = CryptoExecutor()

    plaintext = b"CRITICAL BANKING MESSAGE"

    result = executor.execute(
        profile=profile,
        plaintext=plaintext,
        domain="BANKING",
        session_id="TAMPER-TEST-001",
    )

    tampered_ciphertext = bytearray(
        result.ciphertext
    )

    tampered_ciphertext[0] ^= 1

    try:
        executor.aesgcm_provider.decrypt(
            key=result.receiver_session_key,
            nonce=result.nonce,
            ciphertext=bytes(tampered_ciphertext),
            associated_data=result.associated_data,
        )

    except InvalidTag:
        print("Ciphertext tamper rejection : PASS")
        return

    raise RuntimeError(
        "Tampered ciphertext was incorrectly accepted"
    )


if __name__ == "__main__":
    for profile_id in CRYPTO_PROFILES:
        test_profile_execution(profile_id)

    test_ciphertext_tampering()

    print("\nALL CRYPTO EXECUTOR TESTS PASSED")
