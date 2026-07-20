from app.api.schemas.request import OrchestrationRequest, PolicyRequest
from app.api.schemas.response import OrchestrationResponse, PolicyResponse

from app.orchestration.context import (
    Domain,
    SecurityContext,
    ResourceContext,
    UnifiedContext,
)

from app.orchestration.orchestrator import QOrchestrator

from fastapi import APIRouter

router = APIRouter()

orchestrator = QOrchestrator()


@router.post(
    "/orchestrate",
    response_model=OrchestrationResponse,
)
def orchestrate(request: OrchestrationRequest):

    context = UnifiedContext(
        context_id="API_SESSION",

        domain=Domain(request.domain),

        security=SecurityContext(
            criticality=request.criticality,
            sensitivity=request.sensitivity,
            anomaly_score=request.anomaly_score,
            trust_deficit=request.trust_deficit,
            exposure=request.exposure,
        ),

        resources=ResourceContext(
            cpu_constraint=request.cpu_constraint,
            memory_constraint=request.memory_constraint,
            energy_constraint=request.energy_constraint,
            bandwidth_constraint=request.bandwidth_constraint,
            latency_constraint=request.latency_constraint,
        ),
    )

    result = orchestrator.run(
        context=context,
        plaintext=request.plaintext.encode(),
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


@router.post(
    "/policy",
    response_model=PolicyResponse,
)
def policy(request: PolicyRequest):
    context = UnifiedContext(
        context_id="API_POLICY_SESSION",
        domain=Domain(request.domain),
        security=SecurityContext(
            criticality=request.criticality,
            sensitivity=request.sensitivity,
            anomaly_score=request.anomaly_score,
            trust_deficit=request.trust_deficit,
            exposure=request.exposure,
        ),
        resources=ResourceContext(
            cpu_constraint=request.cpu_constraint,
            memory_constraint=request.memory_constraint,
            energy_constraint=request.energy_constraint,
            bandwidth_constraint=request.bandwidth_constraint,
            latency_constraint=request.latency_constraint,
        ),
    )

    result = orchestrator.prescribe(context)
    profile = result.selection.profile

    return PolicyResponse(
        selected_profile=profile.profile_id,
        security_rank=result.security.required_rank.name,
        resource_capability=result.resources.capability.name,
        mlkem_algorithm=profile.mlkem_algorithm,
        classical_algorithm=profile.classical_algorithm,
        hkdf_hash=profile.hkdf_hash,
        signature_algorithm=profile.signature_algorithm,
        aead_algorithm=profile.aead_algorithm,
    )
