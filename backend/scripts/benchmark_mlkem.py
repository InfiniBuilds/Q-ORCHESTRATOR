import time
import oqs

ITERATIONS = 100

ALGORITHMS = [
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024",
]


def benchmark_algorithm(name):

    keygen = []
    encaps = []
    decaps = []

    for _ in range(ITERATIONS):

        kem = oqs.KeyEncapsulation(name)

        start = time.perf_counter()
        public_key = kem.generate_keypair()
        keygen.append((time.perf_counter() - start) * 1000)

        client = oqs.KeyEncapsulation(name)

        start = time.perf_counter()
        ciphertext, secret1 = client.encap_secret(public_key)
        encaps.append((time.perf_counter() - start) * 1000)

        start = time.perf_counter()
        secret2 = kem.decap_secret(ciphertext)
        decaps.append((time.perf_counter() - start) * 1000)

        assert secret1 == secret2

    print(f"\n{name}")
    print("-" * 40)
    print(f"Average Key Generation : {sum(keygen)/ITERATIONS:.3f} ms")
    print(f"Average Encapsulation  : {sum(encaps)/ITERATIONS:.3f} ms")
    print(f"Average Decapsulation  : {sum(decaps)/ITERATIONS:.3f} ms")


if __name__ == "__main__":

    print("=" * 50)
    print("ML-KEM PERFORMANCE BENCHMARK")
    print("=" * 50)

    for algorithm in ALGORITHMS:
        benchmark_algorithm(algorithm)
