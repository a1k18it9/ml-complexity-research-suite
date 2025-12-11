"""Proper Real RAM model abstraction with complexity tracking.

References:
- Shamos, M.I. (1978). Computational Geometry. PhD Thesis, Yale.
- Preparata & Shamos (1985). Computational Geometry: An Introduction.
- Ben-Or, M. (1983). Lower bounds for algebraic computation trees.
"""

from dataclasses import dataclass, field
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Union, Optional
from enum import Enum
from functools import total_ordering
import sympy as sp

getcontext().prec = 100


class ArithmeticModel(Enum):
    REAL_RAM = "real_ram"
    WORD_RAM = "word_ram"
    BIT_COMPLEXITY = "bit"
    ALGEBRAIC_RAM = "algebraic"


@dataclass
class OperationCost:
    additions: int = 0
    multiplications: int = 0
    divisions: int = 0
    comparisons: int = 0
    square_roots: int = 0
    transcendental: int = 0
    
    def total_algebraic(self) -> int:
        return (self.additions + self.multiplications + 
                self.divisions + self.comparisons + self.square_roots)
    
    def reset(self) -> None:
        self.additions = 0
        self.multiplications = 0
        self.divisions = 0
        self.comparisons = 0
        self.square_roots = 0
        self.transcendental = 0


_operation_counter = OperationCost()


def get_operation_count() -> OperationCost:
    return _operation_counter


def reset_operation_count() -> None:
    _operation_counter.reset()


@total_ordering
class ExactReal:
    def __init__(self, value: Union[int, float, str, Fraction, "ExactReal", sp.Expr]):
        if isinstance(value, ExactReal):
            self._symbolic = value._symbolic
            self._numeric = value._numeric
        elif isinstance(value, sp.Expr):
            self._symbolic = value
            self._numeric = Decimal(str(float(value.evalf(100))))
        elif isinstance(value, Fraction):
            self._symbolic = sp.Rational(value.numerator, value.denominator)
            self._numeric = Decimal(value.numerator) / Decimal(value.denominator)
        elif isinstance(value, int):
            self._symbolic = sp.Integer(value)
            self._numeric = Decimal(value)
        elif isinstance(value, float):
            frac = Fraction(value).limit_denominator(10**15)
            self._symbolic = sp.Rational(frac.numerator, frac.denominator)
            self._numeric = Decimal(str(value))
        else:
            self._symbolic = sp.sympify(value)
            self._numeric = Decimal(str(value))
    
    def __add__(self, other):
        global _operation_counter
        _operation_counter.additions += 1
        other = other if isinstance(other, ExactReal) else ExactReal(other)
        return ExactReal(self._symbolic + other._symbolic)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        global _operation_counter
        _operation_counter.additions += 1
        other = other if isinstance(other, ExactReal) else ExactReal(other)
        return ExactReal(self._symbolic - other._symbolic)
    
    def __mul__(self, other):
        global _operation_counter
        _operation_counter.multiplications += 1
        other = other if isinstance(other, ExactReal) else ExactReal(other)
        return ExactReal(self._symbolic * other._symbolic)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        global _operation_counter
        _operation_counter.divisions += 1
        other = other if isinstance(other, ExactReal) else ExactReal(other)
        return ExactReal(self._symbolic / other._symbolic)
    
    def __lt__(self, other) -> bool:
        global _operation_counter
        _operation_counter.comparisons += 1
        other = other if isinstance(other, ExactReal) else ExactReal(other)
        return bool(sp.simplify(self._symbolic - other._symbolic) < 0)
    
    def __eq__(self, other) -> bool:
        global _operation_counter
        _operation_counter.comparisons += 1
        other = other if isinstance(other, ExactReal) else ExactReal(other)
        return bool(sp.simplify(self._symbolic - other._symbolic) == 0)
    
    def sqrt(self):
        global _operation_counter
        _operation_counter.square_roots += 1
        return ExactReal(sp.sqrt(self._symbolic))
    
    def to_float(self) -> float:
        return float(self._numeric)
    
    def __float__(self) -> float:
        return self.to_float()
    
    def __repr__(self) -> str:
        return f"ExactReal({self._symbolic})"


class ExactPoint2D:
    def __init__(self, x, y):
        self.x = x if isinstance(x, ExactReal) else ExactReal(x)
        self.y = y if isinstance(y, ExactReal) else ExactReal(y)
    
    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy).sqrt()
    
    def distance_squared_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy