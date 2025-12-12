"""Integer Sumset algorithms demonstrating Real RAM vs Word RAM gaps."""

import numpy as np
from typing import List, Set
from dataclasses import dataclass
import random


@dataclass
class SumsetResult:
    sumset: Set[int]
    size: int
    algorithm: str
    operations: int


def naive_sumset(a: List[int], b: List[int]) -> SumsetResult:
    operations = 0
    result = set()
    for x in a:
        for y in b:
            result.add(x + y)
            operations += 1
    return SumsetResult(sumset=result, size=len(result), algorithm="naive", operations=operations)


def bucket_sumset(a: List[int], b: List[int]) -> SumsetResult:
    if not a or not b:
        return SumsetResult(set(), 0, "bucket", 0)
    min_sum = min(a) + min(b)
    max_sum = max(a) + max(b)
    hit = [False] * (max_sum - min_sum + 1)
    operations = 0
    for x in a:
        for y in b:
            hit[(x + y) - min_sum] = True
            operations += 1
    result = {i + min_sum for i, v in enumerate(hit) if v}
    return SumsetResult(sumset=result, size=len(result), algorithm="bucket", operations=operations)


def fft_sumset(a: List[int], b: List[int]) -> SumsetResult:
    if not a or not b:
        return SumsetResult(set(), 0, "fft", 0)
    min_a, min_b = min(a), min(b)
    a_shifted = [x - min_a for x in a]
    b_shifted = [x - min_b for x in b]
    size = max(a_shifted) + max(b_shifted) + 1
    fft_size = 1
    while fft_size < size:
        fft_size *= 2
    fft_size *= 2
    poly_a = np.zeros(fft_size)
    poly_b = np.zeros(fft_size)
    for x in a_shifted:
        poly_a[x] = 1
    for x in b_shifted:
        poly_b[x] = 1
    product = np.fft.ifft(np.fft.fft(poly_a) * np.fft.fft(poly_b)).real
    result = {i + min_a + min_b for i, c in enumerate(product) if c > 0.5}
    operations = 3 * fft_size * int(np.log2(fft_size))
    return SumsetResult(sumset=result, size=len(result), algorithm="fft", operations=operations)


class IntegerSumset:
    def __init__(self, size: int = 1000, value_range: int = None, seed: int = 42):
        self.size = size
        self.value_range = value_range or size * 2
        random.seed(seed)
        self.a = [random.randint(-self.value_range, self.value_range) for _ in range(size)]
        self.b = [random.randint(-self.value_range, self.value_range) for _ in range(size)]
    
    def naive_sumset(self) -> SumsetResult:
        return naive_sumset(self.a, self.b)
    
    def bucket_sumset(self) -> SumsetResult:
        return bucket_sumset(self.a, self.b)
    
    def fft_sumset(self) -> SumsetResult:
        return fft_sumset(self.a, self.b)