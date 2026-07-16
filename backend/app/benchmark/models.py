from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkResult:
    algorithm: str

    operation: str

    execution_time_ms: float

    input_size_bytes: int

    output_size_bytes: int

    success: bool
