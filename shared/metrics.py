"""Metrics collection and timing utilities."""

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
import numpy as np


@dataclass
class TimingResult:
    """Result of a timing measurement."""
    name: str
    duration: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class Timer:
    """Context manager for timing code blocks."""
    
    def __init__(self, name: str = "operation"):
        self.name = name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.duration: Optional[float] = None
    
    def __enter__(self) -> "Timer":
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args) -> None:
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time
    
    def to_result(self) -> TimingResult:
        return TimingResult(name=self.name, duration=self.duration or 0.0, timestamp=datetime.now())


class MetricsCollector:
    """Collect and aggregate metrics from experiments."""
    
    def __init__(self):
        self._metrics: Dict[str, List[float]] = {}
        self._timings: List[TimingResult] = []
        self._metadata: Dict[str, Any] = {}
    
    def record(self, name: str, value: float) -> None:
        """Record a metric value."""
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(value)
    
    def record_timing(self, result: TimingResult) -> None:
        """Record a timing result."""
        self._timings.append(result)
    
    @contextmanager
    def time(self, name: str):
        """Context manager to time and record a code block."""
        timer = Timer(name)
        with timer:
            yield timer
        self.record_timing(timer.to_result())
        self.record(f"{name}_time", timer.duration)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics for all metrics."""
        summary = {}
        for name, values in self._metrics.items():
            arr = np.array(values)
            summary[name] = {
                "count": len(values), "mean": float(np.mean(arr)), "std": float(np.std(arr)),
                "min": float(np.min(arr)), "max": float(np.max(arr)), "median": float(np.median(arr)),
            }
        return summary
    
    def reset(self) -> None:
        """Reset all collected metrics."""
        self._metrics.clear()
        self._timings.clear()
        self._metadata.clear()


def benchmark(func: Callable, *args, iterations: int = 10, warmup: int = 2, **kwargs) -> Dict[str, float]:
    """Benchmark a function with multiple iterations."""
    for _ in range(warmup):
        func(*args, **kwargs)
    
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func(*args, **kwargs)
        times.append(time.perf_counter() - start)
    
    arr = np.array(times)
    return {"mean": float(np.mean(arr)), "std": float(np.std(arr)), "min": float(np.min(arr)), "max": float(np.max(arr)), "median": float(np.median(arr)), "iterations": iterations}
