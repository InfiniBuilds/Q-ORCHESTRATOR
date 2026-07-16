from app.benchmark.models import BenchmarkResult
from app.benchmark.timer import BenchmarkTimer


class BenchmarkRunner:

    @staticmethod
    def run(
        algorithm: str,
        operation: str,
        function,
        input_size_bytes: int,
        output_size_getter,
    ):

        result, execution_time = BenchmarkTimer.measure(function)

        output_size = output_size_getter(result)

        return BenchmarkResult(
            algorithm=algorithm,
            operation=operation,
            execution_time_ms=round(execution_time, 3),
            input_size_bytes=input_size_bytes,
            output_size_bytes=output_size,
            success=True,
        )
