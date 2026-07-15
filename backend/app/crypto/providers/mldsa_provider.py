from dataclasses import dataclass

import oqs


SUPPORTED_MLDSA_ALGORITHMS = {
    "ML-DSA-44",
    "ML-DSA-65",
}


@dataclass(frozen=True)
class MLDSAKeyPair:
    public_key: bytes
    secret_key: bytes


@dataclass(frozen=True)
class MLDSASignatureResult:
    signature: bytes


class MLDSAProvider:
    """
    Reusable ML-DSA digital signature provider backed by liboqs.

    ML-DSA provides digital signatures for message authenticity
    and integrity.

    ML-DSA does NOT encrypt application data.
    """

    def __init__(self, algorithm: str):
        if algorithm not in SUPPORTED_MLDSA_ALGORITHMS:
            raise ValueError(
                f"Unsupported ML-DSA algorithm: {algorithm}"
            )

        enabled_algorithms = set(
            oqs.get_enabled_sig_mechanisms()
        )

        if algorithm not in enabled_algorithms:
            raise RuntimeError(
                f"{algorithm} is not enabled in liboqs"
            )

        self.algorithm = algorithm

    def generate_keypair(self) -> MLDSAKeyPair:
        """
        Generate an ML-DSA public and secret key pair.
        """

        with oqs.Signature(self.algorithm) as signature:
            public_key = signature.generate_keypair()
            secret_key = signature.export_secret_key()

        return MLDSAKeyPair(
            public_key=public_key,
            secret_key=secret_key,
        )

    def sign(
        self,
        secret_key: bytes,
        message: bytes,
    ) -> MLDSASignatureResult:
        """
        Sign a message using an ML-DSA secret key.
        """

        with oqs.Signature(
            self.algorithm,
            secret_key,
        ) as signer:
            signature = signer.sign(message)

        return MLDSASignatureResult(
            signature=signature,
        )

    def verify(
        self,
        public_key: bytes,
        message: bytes,
        signature: bytes,
    ) -> bool:
        """
        Verify an ML-DSA signature.
        """

        with oqs.Signature(self.algorithm) as verifier:
            return verifier.verify(
                message,
                signature,
                public_key,
            )
