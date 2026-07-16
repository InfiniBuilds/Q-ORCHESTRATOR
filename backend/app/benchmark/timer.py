import time
from typing import Callable, Any


class BenchmarkTimer:
    """
    High-resolution timer for benchmark measurements.
    """

    @staticmethod
    def measure(function: Callable, *args, **kwargs) -> tuple[Any, float]:
        """
        Executes a function and returns:
        (result, execution_time_ms)
        """

        start = time.perf_counter()

        result = function(*args, **kwargs)

        end = time.perf_counter()

        execution_time_ms = (end - start) * 1000

        return result, execution_time_ms
