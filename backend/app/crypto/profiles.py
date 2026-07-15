from dataclasses import dataclass
from enum import IntEnum
from typing import Optional


class SecurityRank(IntEnum):
    CONSTRAINED = 1
    STANDARD = 2
    CRITICAL = 3


@dataclass(frozen=True)
class CryptoProfile:
    profile_id: str
    security_rank: SecurityRank

    mlkem_algorithm: str
    classical_algorithm: Optional[str]

    hkdf_hash: str
    signature_algorithm: Optional[str]
    aead_algorithm: str

    hybrid_key_establishment: bool
    per_message_signature: bool

    description: str


CRYPTO_PROFILES = {
    "P1_CONSTRAINED": CryptoProfile(
        profile_id="P1_CONSTRAINED",
        security_rank=SecurityRank.CONSTRAINED,
        mlkem_algorithm="ML-KEM-512",
        classical_algorithm=None,
        hkdf_hash="SHA256",
        signature_algorithm=None,
        aead_algorithm="AES-256-GCM",
        hybrid_key_establishment=False,
        per_message_signature=False,
        description=(
            "Low-overhead PQC profile for constrained "
            "IoT workloads."
        ),
    ),

    "P2_STANDARD": CryptoProfile(
        profile_id="P2_STANDARD",
        security_rank=SecurityRank.STANDARD,
        mlkem_algorithm="ML-KEM-768",
        classical_algorithm="X25519",
        hkdf_hash="SHA384",
        signature_algorithm="ML-DSA-44",
        aead_algorithm="AES-256-GCM",
        hybrid_key_establishment=True,
        per_message_signature=True,
        description=(
            "Standard hybrid PQC profile for normal "
            "banking and capable IoT workloads."
        ),
    ),

    "P3_CRITICAL": CryptoProfile(
        profile_id="P3_CRITICAL",
        security_rank=SecurityRank.CRITICAL,
        mlkem_algorithm="ML-KEM-1024",
        classical_algorithm="X25519",
        hkdf_hash="SHA384",
        signature_algorithm="ML-DSA-65",
        aead_algorithm="AES-256-GCM",
        hybrid_key_establishment=True,
        per_message_signature=True,
        description=(
            "High-assurance hybrid PQC profile for "
            "critical banking operations."
        ),
    ),
}


def get_crypto_profile(profile_id: str) -> CryptoProfile:
    try:
        return CRYPTO_PROFILES[profile_id]
    except KeyError as exc:
        raise ValueError(
            f"Unknown crypto profile: {profile_id}"
        ) from exc


def get_profiles_at_or_above_rank(
    required_rank: SecurityRank,
) -> list[CryptoProfile]:
    return [
        profile
        for profile in CRYPTO_PROFILES.values()
        if profile.security_rank >= required_rank
    ]
