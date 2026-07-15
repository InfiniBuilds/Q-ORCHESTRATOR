from dataclasses import dataclass

from app.crypto.providers.mldsa_provider import MLDSAProvider


@dataclass(frozen=True)
class BankingSignature:
    signer_id: str
    algorithm: str
    signature: bytes


class BankingSigningIdentity:
    """
    Experimental persistent ML-DSA signing identity.

    The key pair is generated once when the identity object
    is created and reused for transaction signing.
    """

    def __init__(
        self,
        signer_id: str,
        algorithm: str,
    ):
        if not signer_id:
            raise ValueError("signer_id is required")

        self.signer_id = signer_id
        self.algorithm = algorithm

        self.provider = MLDSAProvider(algorithm)
        self._keypair = self.provider.generate_keypair()

    @property
    def public_key(self) -> bytes:
        return self._keypair.public_key

    def sign(
        self,
        message: bytes,
    ) -> BankingSignature:
        result = self.provider.sign(
            secret_key=self._keypair.secret_key,
            message=message,
        )

        return BankingSignature(
            signer_id=self.signer_id,
            algorithm=self.algorithm,
            signature=result.signature,
        )

    def verify(
        self,
        message: bytes,
        signature: BankingSignature,
    ) -> bool:
        if signature.signer_id != self.signer_id:
            return False

        if signature.algorithm != self.algorithm:
            return False

        return self.provider.verify(
            public_key=self.public_key,
            message=message,
            signature=signature.signature,
        )
