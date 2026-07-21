from typing import TYPE_CHECKING

from app.database.models import OrchestrationLog
from app.orchestration.context import UnifiedContext

if TYPE_CHECKING:
    from app.orchestration.orchestrator import OrchestrationResult


class OrchestrationMapper:
    @staticmethod
    def to_database_model(
        context: UnifiedContext,
        result: "OrchestrationResult",
        execution_time_ms: float,
    ):
        crypto = result.crypto_result

        return OrchestrationLog(
            # Request Context
            domain=context.domain.value,

            # Security Decision
            security_score=result.security.score,
 	    security_rank=result.security.required_rank.name,
            triggered_rule=result.security.triggered_rule.value,

            # Resource Decision
            resource_score=result.resources.constraint_score,
            resource_capability=result.resources.capability.value,

            # Selected Profile
            selected_profile=result.selection.profile.profile_id,

            # Crypto Information
            mlkem_algorithm=crypto.mlkem_algorithm,
            mldsa_algorithm=(
                crypto.mldsa_algorithm
                if crypto.mldsa_algorithm is not None
                else "NONE"
            ),
            hybrid_enabled=crypto.hybrid_enabled,
            signature_verified=(
                crypto.signature_valid
                if crypto.signature_valid is not None
                else False
            ),
            ciphertext_size=len(crypto.ciphertext),
            session_key_size=len(crypto.sender_session_key),
            execution_time_ms=execution_time_ms,
        )
