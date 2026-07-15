from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


SUPPORTED_HASHES = {
    "SHA256": hashes.SHA256,
    "SHA384": hashes.SHA384,
}


class HKDFProvider:
    """
    HKDF-based key derivation provider.
    """

    def __init__(self, hash_algorithm: str):
        if hash_algorithm not in SUPPORTED_HASHES:
            raise ValueError(
                f"Unsupported HKDF hash: {hash_algorithm}"
            )

        self.hash_algorithm = hash_algorithm

    def derive(
        self,
        input_key_material: bytes,
        salt: bytes,
        info: bytes,
        output_length: int = 32,
    ) -> bytes:
        hash_class = SUPPORTED_HASHES[self.hash_algorithm]

        hkdf = HKDF(
            algorithm=hash_class(),
            length=output_length,
            salt=salt,
            info=info,
        )

        return hkdf.derive(input_key_material)
