from dataclasses import dataclass

import oqs


SUPPORTED_MLKEM_ALGORITHMS = {
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024",
}


@dataclass(frozen=True)
class MLKEMKeyPair:
    public_key: bytes
    secret_key: bytes


@dataclass(frozen=True)
class MLKEMEncapsulationResult:
    ciphertext: bytes
    shared_secret: bytes


class MLKEMProvider:
    """
    Reusable ML-KEM provider backed by liboqs.

    ML-KEM is a Key Encapsulation Mechanism.
    It is used to establish a shared secret.

    It is NOT used to directly encrypt application data.
    """

    def __init__(self, algorithm: str):
        if algorithm not in SUPPORTED_MLKEM_ALGORITHMS:
            raise ValueError(
                f"Unsupported ML-KEM algorithm: {algorithm}"
            )

        enabled_algorithms = set(
            oqs.get_enabled_kem_mechanisms()
        )

        if algorithm not in enabled_algorithms:
            raise RuntimeError(
                f"{algorithm} is not enabled in liboqs"
            )

        self.algorithm = algorithm

    def generate_keypair(self) -> MLKEMKeyPair:
        """
        Generate an ML-KEM public and secret key pair.
        """

        with oqs.KeyEncapsulation(self.algorithm) as kem:
            public_key = kem.generate_keypair()
            secret_key = kem.export_secret_key()

        return MLKEMKeyPair(
            public_key=public_key,
            secret_key=secret_key,
        )

    def encapsulate(
        self,
        public_key: bytes,
    ) -> MLKEMEncapsulationResult:
        """
        Encapsulate a shared secret using the receiver's
        ML-KEM public key.
        """

        with oqs.KeyEncapsulation(self.algorithm) as kem:
            ciphertext, shared_secret = kem.encap_secret(
                public_key
            )

        return MLKEMEncapsulationResult(
            ciphertext=ciphertext,
            shared_secret=shared_secret,
        )

    def decapsulate(
        self,
        secret_key: bytes,
        ciphertext: bytes,
    ) -> bytes:
        """
        Recover the shared secret using the receiver's
        ML-KEM secret key.
        """

        with oqs.KeyEncapsulation(
            self.algorithm,
            secret_key,
        ) as kem:
            shared_secret = kem.decap_secret(ciphertext)

        return shared_secret
