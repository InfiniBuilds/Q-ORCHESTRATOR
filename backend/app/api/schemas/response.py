from pydantic import BaseModel


class OrchestrationResponse(BaseModel):

    selected_profile: str

    security_rank: str

    resource_capability: str

    signature_verified: bool | None

    ciphertext_size: int

    session_key_size: int

    mlkem_ciphertext_size: int

    recovered_plaintext: str

class PolicyResponse(BaseModel):
    selected_profile: str
    security_rank: str
    resource_capability: str
    mlkem_algorithm: str
    classical_algorithm: str | None
    hkdf_hash: str
    signature_algorithm: str | None
    aead_algorithm: str
