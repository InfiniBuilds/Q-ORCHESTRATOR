import os
import time

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITERATIONS = 100

DATA = os.urandom(1024)

KEY = AESGCM.generate_key(bit_length=256)

AES = AESGCM(KEY)

NONCE = os.urandom(12)


encrypt_times = []
decrypt_times = []

ciphertext = None

for _ in range(ITERATIONS):

    start = time.perf_counter()

    ciphertext = AES.encrypt(
        NONCE,
        DATA,
        None,
    )

    encrypt_times.append(
        (time.perf_counter() - start) * 1000
    )

    start = time.perf_counter()

    plaintext = AES.decrypt(
        NONCE,
        ciphertext,
        None,
    )

    decrypt_times.append(
        (time.perf_counter() - start) * 1000
    )

    assert plaintext == DATA

print("=" * 50)
print("AES-256-GCM BENCHMARK")
print("=" * 50)

print(
    f"Average Encryption : "
    f"{sum(encrypt_times)/ITERATIONS:.3f} ms"
)

print(
    f"Average Decryption : "
    f"{sum(decrypt_times)/ITERATIONS:.3f} ms"
)

print(
    f"Ciphertext Size    : "
    f"{len(ciphertext)} bytes"
)
