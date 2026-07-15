from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)


@dataclass(frozen=True)
class X25519KeyPair:
    public_key: bytes
    private_key: bytes


class X25519Provider:
    """
    X25519 classical elliptic-curve key agreement provider.

    X25519 performs key agreement.
    It does NOT directly encrypt application data.
    """

    def generate_keypair(self) -> X25519KeyPair:
        private_key = X25519PrivateKey.generate()
        public_key = private_key.public_key()

        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        return X25519KeyPair(
            public_key=public_key_bytes,
            private_key=private_key_bytes,
        )

    def exchange(
        self,
        private_key: bytes,
        peer_public_key: bytes,
    ) -> bytes:
        local_private_key = X25519PrivateKey.from_private_bytes(
            private_key
        )

        remote_public_key = X25519PublicKey.from_public_bytes(
            peer_public_key
        )

        return local_private_key.exchange(remote_public_key)
