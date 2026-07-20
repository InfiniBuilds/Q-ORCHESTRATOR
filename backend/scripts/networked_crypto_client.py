import time
import os
import sys
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.crypto.providers.x25519_provider import X25519Provider
from app.crypto.providers.mlkem_provider import MLKEMProvider
from app.crypto.providers.hkdf_provider import HKDFProvider
from app.crypto.providers.mldsa_provider import MLDSAProvider
from app.crypto.providers.aesgcm_provider import AESGCMProvider

def main():
    print("============================================================")
    print(" NETWORKED CLIENT CRYPTO SIMULATION ")
    print("============================================================")
    
    # 1. Ask the server for the prescription of algorithms over the network
    print("\n[1] Requesting Policy from Bank Server (over network)...")
    t0 = time.perf_counter()
    
    # Payload for the /policy endpoint
    payload = {
        "domain": "BANKING",
        "criticality": 0.8,
        "sensitivity": 0.8,
        "anomaly_score": 0.1,
        "trust_deficit": 0.1,
        "exposure": 0.5,
        "cpu_constraint": 0.2,
        "memory_constraint": 0.2,
        "energy_constraint": 0.1,
        "bandwidth_constraint": 0.2,
        "latency_constraint": 0.2
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/policy", json=payload, timeout=5)
        response.raise_for_status()
        policy = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to the Orchestrator Server. Is Uvicorn running?")
        print(f"Error: {e}")
        return

    t1 = time.perf_counter()
    
    print(f"    Network Request & Policy Selection Time: {(t1 - t0)*1000:.3f} ms")
    print(f"    Algorithms prescribed by Server:")
    print(f"      - Profile ID: {policy['selected_profile']}")
    print(f"      - Standard: {policy['classical_algorithm']}")
    print(f"      - PQC:      {policy['mlkem_algorithm']}")
    print(f"      - Sign:     {policy['signature_algorithm']}")
    print(f"      - Encrypt:  {policy['aead_algorithm']}")
    
    # 2. Use those algorithms in real time and generate the keys locally
    print("\n[2] Generating Keys Locally on the Client...")
    
    # Pre-Quantum Generation
    t_pq_start = time.perf_counter()
    x25519_provider = X25519Provider()
    alice_x25519 = x25519_provider.generate_keypair()
    bob_x25519 = x25519_provider.generate_keypair()
    t_pq_end = time.perf_counter()
    print(f"    {policy['classical_algorithm']} Key Generation (Alice & Bob): {(t_pq_end - t_pq_start)*1000:.3f} ms")
    
    # Post-Quantum Generation
    t_pqc_start = time.perf_counter()
    mlkem_provider = MLKEMProvider(policy['mlkem_algorithm'])
    bob_mlkem = mlkem_provider.generate_keypair()
    t_pqc_end = time.perf_counter()
    print(f"    {policy['mlkem_algorithm']} Keypair Generation (Bob): {(t_pqc_end - t_pqc_start)*1000:.3f} ms")

    print("\n[3] Establishing Connection and Session Key...")
    t_session_start = time.perf_counter()
    
    # Alice encapsulates shared secret for Bob
    alice_encap = mlkem_provider.encapsulate(bob_mlkem.public_key)
    
    # Bob decapsulates Alice's ciphertext
    bob_decap_secret = mlkem_provider.decapsulate(bob_mlkem.secret_key, alice_encap.ciphertext)
    
    # X25519 Exchange
    alice_x25519_secret = x25519_provider.exchange(alice_x25519.private_key, bob_x25519.public_key)
    bob_x25519_secret = x25519_provider.exchange(bob_x25519.private_key, alice_x25519.public_key)
    
    # Generate the session key using both secrets
    hkdf_provider = HKDFProvider(policy['hkdf_hash'])
    salt = os.urandom(32)
    
    def combine(s1, s2):
        return len(s1).to_bytes(4, "big") + s1 + len(s2).to_bytes(4, "big") + s2

    alice_ikm = combine(alice_x25519_secret, alice_encap.shared_secret)
    bob_ikm = combine(bob_x25519_secret, bob_decap_secret)
    
    info = b"networked-simulation"
    alice_session_key = hkdf_provider.derive(alice_ikm, salt, info, 32)
    bob_session_key = hkdf_provider.derive(bob_ikm, salt, info, 32)
    t_session_end = time.perf_counter()
    
    print(f"    KEM Encapsulation, Decapsulation & HKDF Session Key Derivation: {(t_session_end - t_session_start)*1000:.3f} ms")
    assert alice_session_key == bob_session_key, "Session keys mismatch!"
    
    # 4. Signatures
    print("\n[4] Digital Signatures & Encryption...")
    t_sign_start = time.perf_counter()
    mldsa_provider = MLDSAProvider(policy['signature_algorithm'])
    alice_sign_keys = mldsa_provider.generate_keypair()
    
    plaintext = b"Highly confidential networked transaction data."
    
    signature_result = mldsa_provider.sign(alice_sign_keys.secret_key, plaintext)
    t_sign_end = time.perf_counter()
    print(f"    {policy['signature_algorithm']} Signature Generation Time (incl. Keypair): {(t_sign_end - t_sign_start)*1000:.3f} ms")
    
    t_enc_start = time.perf_counter()
    aes_provider = AESGCMProvider()
    nonce = os.urandom(12)
    encryption_result = aes_provider.encrypt(alice_session_key, plaintext, associated_data=b"test", nonce=nonce)
    t_enc_end = time.perf_counter()
    print(f"    {policy['aead_algorithm']} Encryption Overhead: {(t_enc_end - t_enc_start)*1000:.3f} ms")

    # 5. Verification
    print("\n[5] Decryption & Verification at Receiver...")
    t_dec_start = time.perf_counter()
    decrypted = aes_provider.decrypt(bob_session_key, encryption_result.nonce, encryption_result.ciphertext, associated_data=b"test")
    t_dec_end = time.perf_counter()
    print(f"    {policy['aead_algorithm']} Decryption Overhead: {(t_dec_end - t_dec_start)*1000:.3f} ms")
    
    t_ver_start = time.perf_counter()
    is_valid = mldsa_provider.verify(alice_sign_keys.public_key, decrypted, signature_result.signature)
    t_ver_end = time.perf_counter()
    print(f"    {policy['signature_algorithm']} Signature Verification Time: {(t_ver_end - t_ver_start)*1000:.3f} ms")
    
    print(f"\n    Verification Status: {'SUCCESS' if is_valid else 'FAILED'}")
    
    print("\n============================================================")
    total_time = (t_ver_end - t0) * 1000
    print(f" Total End-to-End Latency (including network roundtrip): {total_time:.3f} ms")
    print("============================================================")

if __name__ == "__main__":
    main()
