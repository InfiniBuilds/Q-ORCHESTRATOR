import sys
import os
import binascii

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestration.context import (
    Domain,
    SecurityContext,
    ResourceContext,
    UnifiedContext,
)
from app.orchestration.orchestrator import QOrchestrator
from app.crypto.executor import CryptoExecutionResult

def hex_trunc(b: bytes) -> str:
    if not b:
        return "None"
    h = binascii.hexlify(b).decode()
    if len(h) > 64:
        return f"{h[:32]}...{h[-32:]} ({len(b)} bytes)"
    return f"{h} ({len(b)} bytes)"

def run_connection_simulation():
    print("============================================================")
    print(" Q-ORCHESTRATOR SECURE CONNECTION ESTABLISHMENT ")
    print("============================================================")
    print("\n[Bank Server] Initializing Orchestrator...")
    orchestrator = QOrchestrator()

    print("\n[Alice] Wants to send a secure transaction to [Bob].")
    print("[Alice] Requesting security policy from [Bank Server]...")

    # Critical transaction context to trigger hybrid KEM and signatures
    context = UnifiedContext(
        context_id="TXN-ALICE-BOB-999",
        domain=Domain.BANKING,
        security=SecurityContext(
            criticality=0.9,
            sensitivity=0.9,
            anomaly_score=0.1,
            trust_deficit=0.1,
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

    plaintext = b"TRANSFER $1,000,000 FROM ALICE TO BOB"

    print(f"\n[Bank Server] Evaluating context for transaction {context.context_id}...")
    result = orchestrator.run(context, plaintext)

    print(f"[Bank Server] Selected Security Profile: {result.selection.profile.profile_id}")
    print(f"   - KEM: {result.selection.profile.mlkem_algorithm} (Post-Quantum) + {result.selection.profile.classical_algorithm or 'None'} (Pre-Quantum)")
    print(f"   - Signature: {result.selection.profile.signature_algorithm}")
    print(f"   - AEAD: {result.selection.profile.aead_algorithm}")
    
    crypto: CryptoExecutionResult = result.crypto_result

    print("\n" + "-"*60)
    print(" KEY EXCHANGE & AUTHENTICATION")
    print("-" * 60)
    print("[Alice & Bob] Generating Pre-Quantum and Post-Quantum Key Pairs...")
    print(f"[Bob] Sending Public Keys to Alice...")
    print(f"[Alice] Encapsulating shared secret and combining (HKDF) into a single session key...")
    
    print(f"\n Derived Session Key (Alice): {hex_trunc(crypto.sender_session_key)}")
    print(f" Derived Session Key (Bob):   {hex_trunc(crypto.receiver_session_key)}")
    if crypto.sender_session_key == crypto.receiver_session_key:
        print(" [SUCCESS] Session Keys match! Secure channel established.")
    else:
        print(" [FAILED] Session Keys DO NOT match!")

    print("\n" + "-"*60)
    print(" SIGNATURE & ENCRYPTION")
    print("-" * 60)
    print(f"[Alice] Signing the transaction using {result.selection.profile.signature_algorithm}...")
    if crypto.signature:
        print(f"  Digital Signature:\n   {hex_trunc(crypto.signature)}")
    else:
        print("  Digital Signature: Not required by profile.")

    print(f"\n[Alice] Encrypting transaction with {result.selection.profile.aead_algorithm}...")
    print(f"  Ciphertext: {hex_trunc(crypto.ciphertext)}")
    print(f"  Nonce: {hex_trunc(crypto.nonce)}")

    print("\n" + "-"*60)
    print(" RECEPTION & VERIFICATION")
    print("-" * 60)
    print("[Bob] Receiving ciphertext and signature from Alice via Bank Server...")
    print(f"[Bob] Decrypting ciphertext...")
    print(f"  Decrypted Message: {crypto.decrypted_plaintext.decode()}")
    
    if crypto.signature_valid is not None:
        print(f"[Bob] Verifying signature...")
        if crypto.signature_valid:
            print(" [SUCCESS] Signature is VALID! Authentication successful.")
        else:
            print(" [FAILED] Signature is INVALID!")

    print("\n" + "="*60)
    print(" SECURE CONNECTION AND TRANSACTION COMPLETE ")
    print("="*60)

if __name__ == "__main__":
    run_connection_simulation()
