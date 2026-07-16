from dataclasses import dataclass

from app.crypto.profiles import SecurityRank
from app.orchestration.resource_engine import (
    ResourceCapability,
    ResourceDecision,
)
from app.orchestration.security_engine import (
    SecurityDecision,
)


@dataclass(frozen=True)
class ConflictResolution:
    minimum_required_rank: SecurityRank
    recommended_rank: SecurityRank
    downgraded: bool
    explanation: str


class ConflictResolver:

    def resolve(
        self,
        security: SecurityDecision,
        resources: ResourceDecision,
    ) -> ConflictResolution:

        minimum_rank = security.required_rank

        # Never downgrade below the required security rank

        if minimum_rank == SecurityRank.CRITICAL:

            return ConflictResolution(
                minimum_required_rank=minimum_rank,
                recommended_rank=SecurityRank.CRITICAL,
                downgraded=False,
                explanation=(
                    "Critical security requirement. "
                    "Downgrade not permitted."
                ),
            )

        if minimum_rank == SecurityRank.STANDARD:

            return ConflictResolution(
                minimum_required_rank=minimum_rank,
                recommended_rank=SecurityRank.STANDARD,
                downgraded=False,
                explanation=(
                    "Standard security requirement maintained."
                ),
            )

        # Only constrained workloads can follow resource capability

        if resources.capability == ResourceCapability.HIGH:

            rank = SecurityRank.STANDARD

            explanation = (
                "Additional resources available. "
                "Upgrading protection."
            )

        else:

            rank = SecurityRank.CONSTRAINED

            explanation = (
                "Constrained workload remains constrained."
            )

        return ConflictResolution(
            minimum_required_rank=minimum_rank,
            recommended_rank=rank,
            downgraded=False,
            explanation=explanation,
        )
