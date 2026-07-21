from enum import Enum

from pydantic import BaseModel


class DeviceType(str, Enum):
    SMART_METER = "SMART_METER"
    CAMERA = "CAMERA"
    MEDICAL_SENSOR = "MEDICAL_SENSOR"
    INDUSTRIAL_SENSOR = "INDUSTRIAL_SENSOR"
    SMART_LOCK = "SMART_LOCK"


class IoTRequest(BaseModel):
    device_type: DeviceType
    battery_level: float
    trusted_device: bool
    anomaly_detected: bool
