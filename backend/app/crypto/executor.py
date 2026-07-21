import os
from dataclasses import dataclass
from typing import Optional

from app.crypto.hybrid_kem import HybridKeyEstablishment
from app.crypto.profiles import CryptoProfile
from app.crypto.providers.aesgcm_provider import AESGCMProvider
from app.crypto.providers.hkdf_provider import HKDFProvider
from app.crypto.providers.mldsa_provider import MLDSAProvider
from app.crypto.providers.mlkem_provider import MLKEMProvider


@dataclass(frozen=True)
class CryptoExecutionResult:
    profile_id: str

    # Profile Information
    mlkem_algorithm: str
    mldsa_algorithm: Optional[str]
    hybrid_enabled: bool

    ciphertext: bytes
    nonce: bytes
    associated_data: bytes

    signature: Optional[bytes]
    signing_public_key: Optional[bytes]

    sender_session_key: bytes
    receiver_session_key: bytes

    mlkem_ciphertext_size: int

    decrypted_plaintext: bytes
    signature_valid: Optional[bool]


class CryptoExecutor:
    """
    Executes an approved Q-ORCHESTRATOR cryptographic profile.
    """

    def __init__(self):
        self.aesgcm_provider = AESGCMProvider()

    def execute(
        self,
        profile: CryptoProfile,
        plaintext: bytes,
        domain: str,
        session_id: str,
    ) -> CryptoExecutionResult:

        salt = os.urandom(32)
        nonce = os.urandom(12)

        associated_data = (
            f"QORCH-V1|"
            f"PROFILE={profile.profile_id}|"
            f"DOMAIN={domain}|"
            f"SESSION={session_id}"
        ).encode("utf-8")

        if profile.hybrid_key_establishment:
            (
                sender_session_key,
                receiver_session_key,
                mlkem_ciphertext_size,
            ) = self._establish_hybrid_session(
                profile=profile,
                domain=domain,
                session_id=session_id,
                salt=salt,
            )
        else:
            (
                sender_session_key,
                receiver_session_key,
                mlkem_ciphertext_size,
            ) = self._establish_pqc_session(
                profile=profile,
                domain=domain,
                session_id=session_id,
                salt=salt,
            )

        signature = None
        signing_public_key = None
        signature_valid = None

        if profile.per_message_signature:
            if profile.signature_algorithm is None:
                raise RuntimeError(
                    "Profile requires signatures but has no signature algorithm"
                )

            signature_provider = MLDSAProvider(
                profile.signature_algorithm
            )

            signing_keys = signature_provider.generate_keypair()

            signature_result = signature_provider.sign(
                secret_key=signing_keys.secret_key,
                message=plaintext,
            )

            signature = signature_result.signature
            signing_public_key = signing_keys.public_key

        encryption_result = self.aesgcm_provider.encrypt(
            key=sender_session_key,
            plaintext=plaintext,
            associated_data=associated_data,
            nonce=nonce,
        )

        decrypted_plaintext = self.aesgcm_provider.decrypt(
            key=receiver_session_key,
            nonce=encryption_result.nonce,
            ciphertext=encryption_result.ciphertext,
            associated_data=associated_data,
        )

        if profile.per_message_signature:
            signature_provider = MLDSAProvider(
                profile.signature_algorithm
            )

            signature_valid = signature_provider.verify(
                public_key=signing_public_key,
                message=decrypted_plaintext,
                signature=signature,
            )

        return CryptoExecutionResult(
            profile_id=profile.profile_id,
            mlkem_algorithm=profile.mlkem_algorithm,
            mldsa_algorithm=profile.signature_algorithm,
            hybrid_enabled=profile.hybrid_key_establishment,
            ciphertext=encryption_result.ciphertext,
            nonce=encryption_result.nonce,
            associated_data=associated_data,
            signature=signature,
            signing_public_key=signing_public_key,
            sender_session_key=sender_session_key,
            receiver_session_key=receiver_session_key,
            mlkem_ciphertext_size=mlkem_ciphertext_size,
            decrypted_plaintext=decrypted_plaintext,
            signature_valid=signature_valid,
        )

    def _establish_hybrid_session(
        self,
        profile: CryptoProfile,
        domain: str,
        session_id: str,
        salt: bytes,
    ) -> tuple[bytes, bytes, int]:

        hybrid = HybridKeyEstablishment(
            mlkem_algorithm=profile.mlkem_algorithm,
            hkdf_hash=profile.hkdf_hash,
        )

        result = hybrid.establish_session(
            profile_id=profile.profile_id,
            domain=domain,
            session_id=session_id,
            salt=salt,
        )

        return (
            result.sender_session_key,
            result.receiver_session_key,
            result.mlkem_ciphertext_size,
        )

    def _establish_pqc_session(
        self,
        profile: CryptoProfile,
        domain: str,
        session_id: str,
        salt: bytes,
    ) -> tuple[bytes, bytes, int]:

        mlkem_provider = MLKEMProvider(
            profile.mlkem_algorithm
        )

        receiver_keys = mlkem_provider.generate_keypair()

        sender_result = mlkem_provider.encapsulate(
            receiver_keys.public_key
        )

        receiver_secret = mlkem_provider.decapsulate(
            secret_key=receiver_keys.secret_key,
            ciphertext=sender_result.ciphertext,
        )

        context = (
            f"QORCH-V1|"
            f"PROFILE={profile.profile_id}|"
            f"DOMAIN={domain}|"
            f"SESSION={session_id}|"
            f"PQC={profile.mlkem_algorithm}|"
            f"KDF=HKDF-{profile.hkdf_hash}"
        ).encode("utf-8")

        hkdf_provider = HKDFProvider(
            profile.hkdf_hash
        )

        sender_session_key = hkdf_provider.derive(
            input_key_material=sender_result.shared_secret,
            salt=salt,
            info=context,
            output_length=32,
        )

        receiver_session_key = hkdf_provider.derive(
            input_key_material=receiver_secret,
            salt=salt,
            info=context,
            output_length=32,
        )

        return (
            sender_session_key,
            receiver_session_key,
            len(sender_result.ciphertext),
        )
