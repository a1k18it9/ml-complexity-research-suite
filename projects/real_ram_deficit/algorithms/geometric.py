"""Geometric optimization algorithms for real-valued inputs."""

import numpy as np
from typing import Callable, List, Tuple
from dataclasses import dataclass


@dataclass
class OptimizationResult:
    optimal_value: float
    optimal_point: np.ndarray
    iterations: int
    function_evaluations: int
    gradient_evaluations: int
    converged: bool


def hill_climb(points: List[Tuple[float, float]], steps: int = 200, step_size: float = 0.05, seed: int = 42) -> OptimizationResult:
    np.random.seed(seed)
    points_arr = np.array(points)
    def cost(pts):
        centroid = pts.mean(axis=0)
        return np.sum(np.linalg.norm(pts - centroid, axis=1))
    best = points_arr.copy()
    best_cost = cost(best)
    func_evals = 1
    for _ in range(steps):
        candidate = best + np.random.uniform(-step_size, step_size, best.shape)
        candidate = np.clip(candidate, 0, 1)
        c_cost = cost(candidate)
        func_evals += 1
        if c_cost < best_cost:
            best, best_cost = candidate, c_cost
    return OptimizationResult(optimal_value=best_cost, optimal_point=best.flatten(), iterations=steps, function_evaluations=func_evals, gradient_evaluations=0, converged=True)


def gradient_descent(f: Callable, grad_f: Callable, x0: np.ndarray, learning_rate: float = 0.01, max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
    x = x0.copy()
    for i in range(max_iter):
        grad = grad_f(x)
        if np.linalg.norm(grad) < tol:
            return OptimizationResult(optimal_value=f(x), optimal_point=x, iterations=i, function_evaluations=i+1, gradient_evaluations=i+1, converged=True)
        x = x - learning_rate * grad
    return OptimizationResult(optimal_value=f(x), optimal_point=x, iterations=max_iter, function_evaluations=max_iter+1, gradient_evaluations=max_iter, converged=False)


class GeometricOptimizer:
    def __init__(self, dimension: int = 2, seed: int = 42):
        self.dimension = dimension
        np.random.seed(seed)
    
    def random_points(self, n: int) -> np.ndarray:
        return np.random.rand(n, self.dimension)
    
    def centroid_cost(self, points: np.ndarray) -> float:
        centroid = points.mean(axis=0)
        return np.sum(np.linalg.norm(points - centroid, axis=1))