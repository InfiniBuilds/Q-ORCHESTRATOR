from dataclasses import dataclass

from app.crypto.providers.hkdf_provider import HKDFProvider
from app.crypto.providers.mlkem_provider import MLKEMProvider
from app.crypto.providers.x25519_provider import X25519Provider


@dataclass(frozen=True)
class HybridSessionResult:
    sender_session_key: bytes
    receiver_session_key: bytes
    mlkem_ciphertext: bytes
    x25519_public_key_size: int
    mlkem_public_key_size: int
    mlkem_ciphertext_size: int


class HybridKeyEstablishment:
    """
    Hybrid X25519 + ML-KEM key establishment.

    The two independently derived shared secrets are encoded
    unambiguously and passed to HKDF.

    Raw shared secrets are never used directly as application
    encryption keys.
    """

    def __init__(
        self,
        mlkem_algorithm: str,
        hkdf_hash: str,
    ):
        self.mlkem_provider = MLKEMProvider(mlkem_algorithm)
        self.x25519_provider = X25519Provider()
        self.hkdf_provider = HKDFProvider(hkdf_hash)

        self.mlkem_algorithm = mlkem_algorithm
        self.hkdf_hash = hkdf_hash

    @staticmethod
    def _length_prefix(value: bytes) -> bytes:
        return len(value).to_bytes(
            4,
            byteorder="big",
        ) + value

    def _combine_secrets(
        self,
        x25519_secret: bytes,
        mlkem_secret: bytes,
    ) -> bytes:
        return (
            self._length_prefix(x25519_secret)
            + self._length_prefix(mlkem_secret)
        )

    def establish_session(
        self,
        profile_id: str,
        domain: str,
        session_id: str,
        salt: bytes,
    ) -> HybridSessionResult:
        # Receiver ML-KEM key pair
        receiver_mlkem_keys = (
            self.mlkem_provider.generate_keypair()
        )

        # Sender encapsulates to receiver
        sender_mlkem_result = self.mlkem_provider.encapsulate(
            receiver_mlkem_keys.public_key
        )

        # Receiver decapsulates
        receiver_mlkem_secret = (
            self.mlkem_provider.decapsulate(
                secret_key=receiver_mlkem_keys.secret_key,
                ciphertext=sender_mlkem_result.ciphertext,
            )
        )

        # Sender and receiver X25519 key pairs
        sender_x25519_keys = (
            self.x25519_provider.generate_keypair()
        )

        receiver_x25519_keys = (
            self.x25519_provider.generate_keypair()
        )

        # Sender derives classical shared secret
        sender_x25519_secret = (
            self.x25519_provider.exchange(
                private_key=sender_x25519_keys.private_key,
                peer_public_key=receiver_x25519_keys.public_key,
            )
        )

        # Receiver independently derives same classical secret
        receiver_x25519_secret = (
            self.x25519_provider.exchange(
                private_key=receiver_x25519_keys.private_key,
                peer_public_key=sender_x25519_keys.public_key,
            )
        )

        sender_ikm = self._combine_secrets(
            x25519_secret=sender_x25519_secret,
            mlkem_secret=sender_mlkem_result.shared_secret,
        )

        receiver_ikm = self._combine_secrets(
            x25519_secret=receiver_x25519_secret,
            mlkem_secret=receiver_mlkem_secret,
        )

        protocol_context = (
            f"QORCH-V1|"
            f"PROFILE={profile_id}|"
            f"DOMAIN={domain}|"
            f"SESSION={session_id}|"
            f"CLASSICAL=X25519|"
            f"PQC={self.mlkem_algorithm}|"
            f"KDF=HKDF-{self.hkdf_hash}"
        ).encode("utf-8")

        sender_session_key = self.hkdf_provider.derive(
            input_key_material=sender_ikm,
            salt=salt,
            info=protocol_context,
            output_length=32,
        )

        receiver_session_key = self.hkdf_provider.derive(
            input_key_material=receiver_ikm,
            salt=salt,
            info=protocol_context,
            output_length=32,
        )

        return HybridSessionResult(
            sender_session_key=sender_session_key,
            receiver_session_key=receiver_session_key,
            mlkem_ciphertext=sender_mlkem_result.ciphertext,
            x25519_public_key_size=len(
                sender_x25519_keys.public_key
            ),
            mlkem_public_key_size=len(
                receiver_mlkem_keys.public_key
            ),
            mlkem_ciphertext_size=len(
                sender_mlkem_result.ciphertext
            ),
        )
