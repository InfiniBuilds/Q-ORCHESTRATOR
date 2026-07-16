import time

from app.benchmark.runner import BenchmarkRunner


def sample_operation():
    time.sleep(0.01)
    return b"hello world"


def output_size(result):
    return len(result)


if __name__ == "__main__":

    benchmark = BenchmarkRunner.run(
        algorithm="TEST",
        operation="Sleep",
        function=sample_operation,
        input_size_bytes=0,
        output_size_getter=output_size,
    )

    print(benchmark)

    print("\nBENCHMARK FRAMEWORK PASSED")
