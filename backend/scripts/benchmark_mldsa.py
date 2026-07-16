import time
import oqs

ITERATIONS = 100

ALGORITHMS = [
    "ML-DSA-44",
    "ML-DSA-65",
]


MESSAGE = b"Q-ORCHESTRATOR Benchmark"


def benchmark_algorithm(name):

    keygen = []
    sign = []
    verify = []

    for _ in range(ITERATIONS):

        sig = oqs.Signature(name)

        start = time.perf_counter()
        public_key = sig.generate_keypair()
        keygen.append((time.perf_counter() - start) * 1000)

        start = time.perf_counter()
        signature = sig.sign(MESSAGE)
        sign.append((time.perf_counter() - start) * 1000)

        verifier = oqs.Signature(name)

        start = time.perf_counter()
        verifier.verify(MESSAGE, signature, public_key)
        verify.append((time.perf_counter() - start) * 1000)

    print(f"\n{name}")
    print("-" * 40)
    print(f"Average Key Generation : {sum(keygen)/ITERATIONS:.3f} ms")
    print(f"Average Signing        : {sum(sign)/ITERATIONS:.3f} ms")
    print(f"Average Verification   : {sum(verify)/ITERATIONS:.3f} ms")


if __name__ == "__main__":

    print("=" * 50)
    print("ML-DSA PERFORMANCE BENCHMARK")
    print("=" * 50)

    for algorithm in ALGORITHMS:
        benchmark_algorithm(algorithm)
