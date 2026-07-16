from dataclasses import dataclass

from app.crypto.executor import CryptoExecutor
from app.orchestration.context import UnifiedContext
from app.orchestration.security_engine import (
    SecurityDecision,
    SecurityRequirementEngine,
)
from app.orchestration.resource_engine import (
    ResourceConstraintEngine,
    ResourceDecision,
)
from app.orchestration.conflict_resolver import (
    ConflictResolver,
    ConflictResolution,
)
from app.orchestration.profile_selector import (
    AdaptiveProfileSelector,
    ProfileSelection,
)


@dataclass(frozen=True)
class OrchestrationResult:
    security: SecurityDecision
    resources: ResourceDecision
    resolution: ConflictResolution
    selection: ProfileSelection
    crypto_result: object


class QOrchestrator:

    def __init__(self):

        self.security_engine = SecurityRequirementEngine()

        self.resource_engine = ResourceConstraintEngine()

        self.conflict_resolver = ConflictResolver()

        self.selector = AdaptiveProfileSelector()

        self.executor = CryptoExecutor()

    def run(
        self,
        context: UnifiedContext,
        plaintext: bytes,
    ) -> OrchestrationResult:

        security = self.security_engine.evaluate(
            context
        )

        resources = self.resource_engine.evaluate(
            context
        )

        resolution = self.conflict_resolver.resolve(
            security,
            resources,
        )

        selection = self.selector.select(
            resolution,
        )

        crypto_result = self.executor.execute(
            profile=selection.profile,
            plaintext=plaintext,
            domain=context.domain.value,
            session_id=context.context_id,
        )

        return OrchestrationResult(
            security=security,
            resources=resources,
            resolution=resolution,
            selection=selection,
            crypto_result=crypto_result,
        )
