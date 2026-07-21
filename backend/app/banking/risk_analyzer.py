from app.orchestration.context import (
    Domain,
    ResourceContext,
    SecurityContext,
    UnifiedContext,
)

from app.api.schemas.banking import (
    BankingRequest,
    TransactionType,
)


class BankingRiskAnalyzer:

    @staticmethod
    def build_context(request: BankingRequest) -> UnifiedContext:

        if request.transaction_type == TransactionType.BALANCE_CHECK:

            security = SecurityContext(
                criticality=0.20,
                sensitivity=0.20,
                anomaly_score=0.05,
                trust_deficit=0.10 if request.trusted_device else 0.40,
                exposure=0.20,
            )

        elif request.transaction_type == TransactionType.LOCAL_TRANSFER:

            security = SecurityContext(
                criticality=0.50,
                sensitivity=0.50,
                anomaly_score=0.10,
                trust_deficit=0.10 if request.trusted_device else 0.50,
                exposure=0.40,
            )

        elif request.transaction_type == TransactionType.HIGH_VALUE_TRANSFER:

            security = SecurityContext(
                criticality=0.95,
                sensitivity=0.95,
                anomaly_score=0.20,
                trust_deficit=0.10 if request.trusted_device else 0.60,
                exposure=0.60,
            )

        elif request.transaction_type == TransactionType.INTERNATIONAL_TRANSFER:

            security = SecurityContext(
                criticality=1.0,
                sensitivity=1.0,
                anomaly_score=0.30,
                trust_deficit=0.20 if request.trusted_device else 0.70,
                exposure=0.80,
            )

        else:

            security = SecurityContext(
                criticality=0.60,
                sensitivity=0.60,
                anomaly_score=0.10,
                trust_deficit=0.20,
                exposure=0.40,
            )

        resources = ResourceContext(
            cpu_constraint=0.20,
            memory_constraint=0.20,
            energy_constraint=0.00,
            bandwidth_constraint=0.20,
            latency_constraint=0.20,
        )

        return UnifiedContext(
            context_id="BANKING_API",
            domain=Domain.BANKING,
            security=security,
            resources=resources,
        )
