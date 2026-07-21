from fastapi import APIRouter

from app.api.schemas.iot import IoTRequest
from app.api.schemas.response import OrchestrationResponse

from app.iot.risk_analyzer import IoTRiskAnalyzer

from app.orchestration.orchestrator import QOrchestrator

router = APIRouter(prefix="/iot", tags=["IoT"])

orchestrator = QOrchestrator()


@router.post("/simulate", response_model=OrchestrationResponse)
def simulate_device(request: IoTRequest):

    context = IoTRiskAnalyzer.build_context(request)

    plaintext = (
        f"{request.device_type.value}|"
        f"{request.battery_level}|"
        f"{request.trusted_device}|"
        f"{request.anomaly_detected}"
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
