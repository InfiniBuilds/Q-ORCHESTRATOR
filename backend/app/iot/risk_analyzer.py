from app.api.schemas.iot import DeviceType, IoTRequest

from app.orchestration.context import (
    Domain,
    ResourceContext,
    SecurityContext,
    UnifiedContext,
)


class IoTRiskAnalyzer:

    @staticmethod
    def build_context(request: IoTRequest) -> UnifiedContext:

        if request.device_type == DeviceType.MEDICAL_SENSOR:

            security = SecurityContext(
                criticality=1.0,
                sensitivity=1.0,
                anomaly_score=0.8 if request.anomaly_detected else 0.2,
                trust_deficit=0.1 if request.trusted_device else 0.7,
                exposure=0.5,
            )

            resources = ResourceContext(
                cpu_constraint=0.5,
                memory_constraint=0.4,
                energy_constraint=0.8,
                bandwidth_constraint=0.2,
                latency_constraint=0.3,
            )

        elif request.device_type == DeviceType.SMART_LOCK:

            security = SecurityContext(
                criticality=0.95,
                sensitivity=0.9,
                anomaly_score=0.7 if request.anomaly_detected else 0.2,
                trust_deficit=0.2 if request.trusted_device else 0.7,
                exposure=0.5,
            )

            resources = ResourceContext(
                cpu_constraint=0.3,
                memory_constraint=0.3,
                energy_constraint=0.5,
                bandwidth_constraint=0.2,
                latency_constraint=0.2,
            )

        elif request.device_type == DeviceType.CAMERA:

            security = SecurityContext(
                criticality=0.5,
                sensitivity=0.5,
                anomaly_score=0.5 if request.anomaly_detected else 0.1,
                trust_deficit=0.2 if request.trusted_device else 0.6,
                exposure=0.8,
            )

            resources = ResourceContext(
                cpu_constraint=0.7,
                memory_constraint=0.6,
                energy_constraint=0.4,
                bandwidth_constraint=0.9,
                latency_constraint=0.4,
            )

        else:

            security = SecurityContext(
                criticality=0.6,
                sensitivity=0.6,
                anomaly_score=0.4 if request.anomaly_detected else 0.1,
                trust_deficit=0.2,
                exposure=0.5,
            )

            resources = ResourceContext(
                cpu_constraint=0.4,
                memory_constraint=0.4,
                energy_constraint=1.0 - request.battery_level,
                bandwidth_constraint=0.4,
                latency_constraint=0.3,
            )

        return UnifiedContext(
            context_id="IOT_API",
            domain=Domain.IOT,
            security=security,
            resources=resources,
        )
