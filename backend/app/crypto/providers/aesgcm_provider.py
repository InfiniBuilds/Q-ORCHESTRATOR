from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


@dataclass(frozen=True)
class AESGCMEncryptionResult:
    nonce: bytes
    ciphertext: bytes


class AESGCMProvider:
    """
    AES-GCM authenticated encryption provider.

    AES-GCM provides:
    - confidentiality
    - integrity
    - ciphertext authentication
    """

    KEY_SIZE = 32
    NONCE_SIZE = 12

    def encrypt(
        self,
        key: bytes,
        plaintext: bytes,
        associated_data: bytes,
        nonce: bytes,
    ) -> AESGCMEncryptionResult:
        self._validate_key(key)
        self._validate_nonce(nonce)

        aesgcm = AESGCM(key)

        ciphertext = aesgcm.encrypt(
            nonce,
            plaintext,
            associated_data,
        )

        return AESGCMEncryptionResult(
            nonce=nonce,
            ciphertext=ciphertext,
        )

    def decrypt(
        self,
        key: bytes,
        nonce: bytes,
        ciphertext: bytes,
        associated_data: bytes,
    ) -> bytes:
        self._validate_key(key)
        self._validate_nonce(nonce)

        aesgcm = AESGCM(key)

        return aesgcm.decrypt(
            nonce,
            ciphertext,
            associated_data,
        )

    @classmethod
    def _validate_key(cls, key: bytes) -> None:
        if len(key) != cls.KEY_SIZE:
            raise ValueError(
                "AES-256-GCM requires a 32-byte key"
            )

    @classmethod
    def _validate_nonce(cls, nonce: bytes) -> None:
        if len(nonce) != cls.NONCE_SIZE:
            raise ValueError(
                "AES-GCM nonce must be 12 bytes"
            )
