from pydantic import BaseModel, Field


class OrchestrationRequest(BaseModel):

    domain: str

    criticality: float = Field(..., ge=0.0, le=1.0)
    sensitivity: float = Field(..., ge=0.0, le=1.0)
    anomaly_score: float = Field(..., ge=0.0, le=1.0)
    trust_deficit: float = Field(..., ge=0.0, le=1.0)
    exposure: float = Field(..., ge=0.0, le=1.0)

    cpu_constraint: float = Field(..., ge=0.0, le=1.0)
    memory_constraint: float = Field(..., ge=0.0, le=1.0)
    energy_constraint: float = Field(..., ge=0.0, le=1.0)
    bandwidth_constraint: float = Field(..., ge=0.0, le=1.0)
    latency_constraint: float = Field(..., ge=0.0, le=1.0)

    plaintext: str

class PolicyRequest(BaseModel):
    domain: str

    criticality: float = Field(..., ge=0.0, le=1.0)
    sensitivity: float = Field(..., ge=0.0, le=1.0)
    anomaly_score: float = Field(..., ge=0.0, le=1.0)
    trust_deficit: float = Field(..., ge=0.0, le=1.0)
    exposure: float = Field(..., ge=0.0, le=1.0)

    cpu_constraint: float = Field(..., ge=0.0, le=1.0)
    memory_constraint: float = Field(..., ge=0.0, le=1.0)
    energy_constraint: float = Field(..., ge=0.0, le=1.0)
    bandwidth_constraint: float = Field(..., ge=0.0, le=1.0)
    latency_constraint: float = Field(..., ge=0.0, le=1.0)
