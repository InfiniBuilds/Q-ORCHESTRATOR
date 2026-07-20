import sys
import os

# Ensure backend is in PYTHONPATH if running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestration.context import (
    Domain,
    SecurityContext,
    ResourceContext,
    UnifiedContext,
)
from app.orchestration.orchestrator import QOrchestrator


def print_simulation_result(name: str, context: UnifiedContext, orchestrator: QOrchestrator):
    print(f"\n{'='*50}")
    print(f"Simulation: {name}")
    print(f"Domain: {context.domain.value}")
    
    # Run the orchestrator
    plaintext = b"SIMULATED_TRAFFIC_DATA"
    result = orchestrator.run(context, plaintext)
    
    print("\n--- Scores ---")
    print(f"Security Score: {result.security.score} (Required Rank: {result.security.required_rank.name})")
    print(f"Resource Score: {result.resources.constraint_score} (Capability: {result.resources.capability.name})")
    print(f"Conflict Resolution: {result.resolution.recommended_rank.name} ({result.resolution.explanation})")
    
    print("\n--- Allocation ---")
    profile = result.selection.profile
    print(f"Profile Selected: {profile.profile_id}")
    print(f"Description: {profile.description}")
    print(f"KEM Algorithm: {profile.mlkem_algorithm}")
    if profile.signature_algorithm:
        print(f"Signature Algorithm: {profile.signature_algorithm}")
    else:
        print("Signature Algorithm: NONE")
    print(f"AEAD Algorithm: {profile.aead_algorithm}")


def main():
    orchestrator = QOrchestrator()

    # 1. Standard Banking Simulator
    banking_standard_ctx = UnifiedContext(
        context_id="BANK-STD-001",
        domain=Domain.BANKING,
        security=SecurityContext(
            criticality=0.6,
            sensitivity=0.6,
            anomaly_score=0.1,
            trust_deficit=0.1,
            exposure=0.2,
        ),
        resources=ResourceContext(
            cpu_constraint=0.2,
            memory_constraint=0.2,
            energy_constraint=0.1,
            bandwidth_constraint=0.2,
            latency_constraint=0.2,
        ),
    )

    # 2. Critical Banking Simulator (e.g., Anomaly detected or very high value)
    banking_critical_ctx = UnifiedContext(
        context_id="BANK-CRIT-002",
        domain=Domain.BANKING,
        security=SecurityContext(
            criticality=0.9,
            sensitivity=0.9,
            anomaly_score=0.8,
            trust_deficit=0.5,
            exposure=0.5,
        ),
        resources=ResourceContext(
            cpu_constraint=0.2,
            memory_constraint=0.2,
            energy_constraint=0.1,
            bandwidth_constraint=0.2,
            latency_constraint=0.2,
        ),
    )

    # 3. Standard IoT Simulator
    iot_standard_ctx = UnifiedContext(
        context_id="IOT-STD-001",
        domain=Domain.IOT,
        security=SecurityContext(
            criticality=0.3,
            sensitivity=0.3,
            anomaly_score=0.1,
            trust_deficit=0.4,
            exposure=0.6,
        ),
        resources=ResourceContext(
            cpu_constraint=0.6,
            memory_constraint=0.6,
            energy_constraint=0.5,
            bandwidth_constraint=0.6,
            latency_constraint=0.5,
        ),
    )

    # 4. Highly Constrained IoT Simulator (Battery low, high network congestion)
    iot_constrained_ctx = UnifiedContext(
        context_id="IOT-CON-002",
        domain=Domain.IOT,
        security=SecurityContext(
            criticality=0.2,
            sensitivity=0.2,
            anomaly_score=0.1,
            trust_deficit=0.2,
            exposure=0.4,
        ),
        resources=ResourceContext(
            cpu_constraint=0.9,
            memory_constraint=0.9,
            energy_constraint=0.9,
            bandwidth_constraint=0.9,
            latency_constraint=0.8,
        ),
    )

    scenarios = [
        ("Standard Banking Transaction", banking_standard_ctx),
        ("Critical Banking Transaction (Anomalous)", banking_critical_ctx),
        ("Standard IoT Telemetry", iot_standard_ctx),
        ("Highly Constrained IoT Telemetry (Low Battery)", iot_constrained_ctx),
    ]

    print("Starting Q-ORCHESTRATOR Traffic Simulator...")
    for name, ctx in scenarios:
        print_simulation_result(name, ctx, orchestrator)


if __name__ == "__main__":
    main()
