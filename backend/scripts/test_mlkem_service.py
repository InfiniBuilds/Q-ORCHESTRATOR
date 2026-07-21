from app.benchmark.services.mlkem_service import (
    MLKEMBenchmarkService,
)

service = MLKEMBenchmarkService()

result = service.benchmark(
    "ML-KEM-768",
)

print(result)
