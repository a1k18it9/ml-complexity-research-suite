"""Real RAM Deficit Explorer - Main Project File."""

from typing import Any, Dict, List
from shared.base import BaseProject, BaseExperiment, ExperimentResult
from shared.metrics import MetricsCollector, benchmark
from projects.real_ram_deficit.models.real_ram import ExactReal, reset_operation_count, get_operation_count
from projects.real_ram_deficit.algorithms.sumset import IntegerSumset
from projects.real_ram_deficit.algorithms.geometric import GeometricOptimizer, hill_climb


class SumsetExperiment(BaseExperiment):
    def __init__(self, sizes: List[int] = None, **kwargs):
        super().__init__("sumset_comparison", **kwargs)
        self.sizes = sizes or [100, 200, 500, 1000]
    
    def setup(self) -> None:
        self.metrics = MetricsCollector()
    
    def run(self) -> Dict[str, Any]:
        results = {"naive": [], "bucket": [], "fft": []}
        for size in self.sizes:
            sumset = IntegerSumset(size=size)
            for name, method in [("naive", sumset.naive_sumset), ("bucket", sumset.bucket_sumset), ("fft", sumset.fft_sumset)]:
                timing = benchmark(method, iterations=3, warmup=1)
                results[name].append({"size": size, "time": timing["mean"]})
        return results
    
    def teardown(self) -> None:
        pass


class RealRAMOperationsExperiment(BaseExperiment):
    def __init__(self, n_points: int = 50, **kwargs):
        super().__init__("real_ram_operations", **kwargs)
        self.n_points = n_points
    
    def setup(self) -> None:
        reset_operation_count()
    
    def run(self) -> Dict[str, Any]:
        points = [ExactReal(i) for i in range(self.n_points)]
        reset_operation_count()
        total = ExactReal(0)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                diff = points[i] - points[j]
                total = total + diff * diff
        ops = get_operation_count()
        return {"n_points": self.n_points, "additions": ops.additions, "multiplications": ops.multiplications, "total": ops.total_algebraic()}
    
    def teardown(self) -> None:
        reset_operation_count()


class RealRAMDeficitProject(BaseProject):
    PROJECT_NAME = "real_ram_deficit"
    VERSION = "1.0.0"
    
    def get_description(self) -> str:
        return "Explores the computational gap between Real RAM and Word RAM models."
    
    def get_experiments(self) -> List[str]:
        return ["sumset_comparison", "real_ram_operations"]
    
    def run_experiment(self, name: str, **kwargs) -> ExperimentResult:
        experiments = {"sumset_comparison": SumsetExperiment, "real_ram_operations": RealRAMOperationsExperiment}
        if name not in experiments:
            raise ValueError(f"Unknown experiment: {name}")
        return experiments[name](**kwargs).execute()