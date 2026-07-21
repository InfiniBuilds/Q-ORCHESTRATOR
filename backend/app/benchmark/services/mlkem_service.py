from dataclasses import dataclass

from app.crypto.providers.mlkem_provider import MLKEMProvider
from app.benchmark.timer import BenchmarkTimer


@dataclass(frozen=True)
class MLKEMBenchmarkResult:
    algorithm: str
    key_generation_ms: float
    encapsulation_ms: float
    decapsulation_ms: float


class MLKEMBenchmarkService:
    def benchmark(self, algorithm: str, iterations: int = 100) -> MLKEMBenchmarkResult:
        provider = MLKEMProvider(algorithm)

        keygen_times = []
        encapsulation_times = []
        decapsulation_times = []

        for _ in range(iterations):
            keys, elapsed = BenchmarkTimer.measure(
                provider.generate_keypair,
            )
            keygen_times.append(elapsed)

            sender, elapsed = BenchmarkTimer.measure(
                provider.encapsulate,
                keys.public_key,
            )
            encapsulation_times.append(elapsed)

            _, elapsed = BenchmarkTimer.measure(
                provider.decapsulate,
                secret_key=keys.secret_key,
                ciphertext=sender.ciphertext,
            )
            decapsulation_times.append(elapsed)

        return MLKEMBenchmarkResult(
            algorithm=algorithm,
            key_generation_ms=round(
                sum(keygen_times) / iterations,
                3,
            ),
            encapsulation_ms=round(
                sum(encapsulation_times) / iterations,
                3,
            ),
            decapsulation_ms=round(
                sum(decapsulation_times) / iterations,
                3,
            ),
        )
