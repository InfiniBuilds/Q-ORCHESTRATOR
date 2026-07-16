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
