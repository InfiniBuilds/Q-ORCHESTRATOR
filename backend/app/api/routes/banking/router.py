from fastapi import APIRouter

from app.api.schemas.banking import BankingRequest
from app.api.schemas.response import OrchestrationResponse

from app.banking.risk_analyzer import BankingRiskAnalyzer

from app.orchestration.orchestrator import QOrchestrator

router = APIRouter(prefix="/banking", tags=["Banking"])

orchestrator = QOrchestrator()


@router.post("/simulate", response_model=OrchestrationResponse)
def simulate_transaction(request: BankingRequest):

    context = BankingRiskAnalyzer.build_context(request)

    plaintext = (
        f"{request.transaction_type.value}|"
        f"{request.amount}|"
        f"{request.authenticated}"
    ).encode()

    result = orchestrator.run(
        context=context,
        plaintext=plaintext,
    )

    crypto = result.crypto_result

    return OrchestrationResponse(
        selected_profile=result.selection.profile.profile_id,
        security_rank=result.security.required_rank.name,
        resource_capability=result.resources.capability.name,
        signature_verified=crypto.signature_valid,
        ciphertext_size=len(crypto.ciphertext),
        session_key_size=len(crypto.sender_session_key),
        mlkem_ciphertext_size=crypto.mlkem_ciphertext_size,
        recovered_plaintext=crypto.decrypted_plaintext.decode(),
    )
