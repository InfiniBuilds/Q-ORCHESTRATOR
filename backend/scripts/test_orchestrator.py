from app.orchestration.context import (
    Domain,
    ResourceContext,
    SecurityContext,
    UnifiedContext,
)

from app.orchestration.orchestrator import QOrchestrator


def create_context():

    return UnifiedContext(
        context_id="BANK-001",
        domain=Domain.BANKING,
        security=SecurityContext(
            criticality=0.95,
            sensitivity=0.90,
            anomaly_score=0.20,
            trust_deficit=0.10,
            exposure=0.30,
        ),
        resources=ResourceContext(
            cpu_constraint=0.20,
            memory_constraint=0.20,
            energy_constraint=0.00,
            bandwidth_constraint=0.20,
            latency_constraint=0.20,
        ),
    )


if __name__ == "__main__":

    orchestrator = QOrchestrator()

    result = orchestrator.run(
        context=create_context(),
        plaintext=b"Q-ORCHESTRATOR TEST MESSAGE",
    )

    print("\n========== ORCHESTRATION RESULT ==========\n")

    print("Security Decision")
    print(result.security)

    print("\nResource Decision")
    print(result.resources)

    print("\nConflict Resolution")
    print(result.resolution)

    print("\nSelected Profile")
    print(result.selection)

    crypto = result.crypto_result

    print("\n========== CRYPTO EXECUTION ==========\n")

    print(f"Profile             : {crypto.profile_id}")
    print(f"Ciphertext Size     : {len(crypto.ciphertext)} bytes")
    print(f"Nonce Size          : {len(crypto.nonce)} bytes")
    print(f"Session Key Size    : {len(crypto.sender_session_key)} bytes")
    print(f"ML-KEM CT Size      : {crypto.mlkem_ciphertext_size} bytes")
    print(f"Signature Enabled   : {crypto.signature is not None}")
    print(f"Signature Valid     : {crypto.signature_valid}")
    print(f"Recovered Plaintext : {crypto.decrypted_plaintext.decode()}")

    print("\n==========================================")
