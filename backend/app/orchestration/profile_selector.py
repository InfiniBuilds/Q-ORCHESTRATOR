from dataclasses import dataclass

from app.crypto.profiles import (
    CRYPTO_PROFILES,
    CryptoProfile,
    SecurityRank,
)
from app.orchestration.conflict_resolver import (
    ConflictResolution,
)


@dataclass(frozen=True)
class ProfileSelection:
    profile: CryptoProfile
    explanation: str


class AdaptiveProfileSelector:

    def select(
        self,
        resolution: ConflictResolution,
    ) -> ProfileSelection:

        if (
            resolution.recommended_rank
            == SecurityRank.CRITICAL
        ):
            profile = CRYPTO_PROFILES["P3_CRITICAL"]

        elif (
            resolution.recommended_rank
            == SecurityRank.STANDARD
        ):
            profile = CRYPTO_PROFILES["P2_STANDARD"]

        else:
            profile = CRYPTO_PROFILES["P1_CONSTRAINED"]

        return ProfileSelection(
            profile=profile,
            explanation=(
                f"Selected profile "
                f"{profile.profile_id}"
            ),
        )
