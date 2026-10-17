HybridBankFramework

A Hybrid Post-Quantum Secure Banking Framework — a TLS-style protocol between a banking client and server that combines classical cryptography (RSA) with NIST-standardised post-quantum cryptography (Kyber / ML-KEM and Dilithium / ML-DSA), so a session stays secure against both classical and quantum attackers.

Internship project: Implement quantum-resistant cryptographic algorithms that can run efficiently in real-time applications like banking and IoT.

Team: Shiva Swaroop DS (PES2UG24CS679) · Palla Tejeswar (PES2UG24CS644) · Adarsha V (PES2UG24CS621)

Why this project

RSA and elliptic-curve cryptography, which secure today's banking traffic, can be broken by Shor's algorithm on a large quantum computer. Attackers can also record encrypted traffic now and decrypt it later ("harvest now, decrypt later"). This framework shows how a banking system can migrate to post-quantum algorithms without dropping classical security, using a hybrid design.

Core modules
Module	Purpose
DAN — Dynamic Algorithm Negotiation	Coordinates the handshake so client and server agree on algorithms
NPE — Negotiation Policy Engine	Finds mutually supported algorithms, drops deprecated ones, picks the strongest, and outputs a Security Profile
HKFE — Hybrid Key Fusion Engine	Fuses the RSA secret and the Kyber secret with HKDF (RFC 5869) into a master secret, then derives separate client-write and server-write keys and nonce bases. An attacker must break both RSA and Kyber to recover the session key
HSFE — Hybrid Signature Fusion Engine	Signs the SHA3-512 digest of each request with RSA-PSS and ML-DSA. A request is accepted only if both signatures verify

HKFE and HSFE are original software modules that apply standard, proven primitives (HKDF, dual-signature verification) inside a new protocol architecture. They are not new cryptographic algorithms.

Algorithms used
Function	Classical	Post-quantum
Key exchange	RSA-2048 (OAEP)	Kyber / ML-KEM (512, 768, 1024)
Digital signature	RSA-PSS	Dilithium / ML-DSA (44, 65, 87)
Session encryption	AES-256-GCM	—
Hashing	SHA3-512	—
Key derivation	HKDF-SHA256	—
Features
Dynamic, policy-driven algorithm negotiation with a deprecation list
Hybrid key establishment (RSA + Kyber) fused via HKDF
Directional session keys, so client and server never reuse an AES-GCM nonce
Hybrid authentication tokens with AND-logic verification (tampering is rejected)
Banking operations: signup, login, check balance, transfer, transaction history, logout
Persistent accounts in accounts.json; passwords hashed with PBKDF2-HMAC-SHA256 and a per-user salt (never stored in plaintext)
Qiskit demos: quantum random bits and Shor's algorithm factoring N = 15
Benchmark suite comparing PQC with RSA / ECDH / ECDSA
