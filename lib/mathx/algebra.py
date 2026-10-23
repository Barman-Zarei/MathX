"""Equations and fractions."""

from __future__ import annotations

import cmath
import math
from fractions import Fraction
from typing import List, Sequence, Tuple, Union

from . import _validate as v
from ._validate import Number

Root = Union[float, complex]


def solve_quadratic(a: Number, b: Number, c: Number) -> Tuple[Root, Root]:
    """Roots of a*x^2 + b*x + c = 0.

    Returns two floats (equal for a double root) or two complex numbers when
    the discriminant is negative.
    """
    a = v.as_float(a, "a")
    b = v.as_float(b, "b")
    c = v.as_float(c, "c")
    if a == 0:
        raise ValueError("a must not be zero (the equation is not quadratic)")
    disc = b * b - 4 * a * c
    if disc >= 0:
        root = math.sqrt(disc)
        q = -0.5 * (b + math.copysign(root, b))
        if q == 0:
            return 0.0, 0.0
        r1, r2 = q / a, c / q
        return (r1, r2) if r1 <= r2 else (r2, r1)
    root = cmath.sqrt(disc)
    return (-b - root) / (2 * a), (-b + root) / (2 * a)


def solve_linear_system(
    matrix: Sequence[Sequence[Number]], constants: Sequence[Number]
) -> List[Number]:
    """Solve A x = b for a square system (Gaussian elimination).

    With only int/Fraction inputs the answer is exact (a list of Fractions);
    otherwise floats are used. Raises ValueError if there is no unique solution.
    """
    rows = [v.number_list(r, f"matrix[{i}]") for i, r in enumerate(matrix)]
    consts = v.number_list(constants, "constants")
    n = len(rows)
    if n == 0 or any(len(r) != n for r in rows):
        raise ValueError("matrix must be square")
    if len(consts) != n:
        raise ValueError("constants must have one value per row")
    exact = all(isinstance(x, (int, Fraction)) for r in rows for x in r) and all(
        isinstance(x, (int, Fraction)) for x in consts
    )
    conv = Fraction if exact else float
    aug = [[conv(x) for x in rows[i]] + [conv(consts[i])] for i in range(n)]
    eps = 0 if exact else 1e-12
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) <= eps:
            raise ValueError("the system has no unique solution")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for r in range(col + 1, n):
            factor = aug[r][col] / aug[col][col]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    x: List[Number] = [conv(0)] * n
    for i in reversed(range(n)):
        s = sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (aug[i][n] - s) / aug[i][i]
    return x


def simplify_fraction(numerator: int, denominator: int) -> Fraction:
    """Reduce numerator/denominator to lowest terms (sign kept on the numerator)."""
    n = v.integer(numerator, "numerator")
    d = v.integer(denominator, "denominator")
    if d == 0:
        raise ValueError("denominator must not be zero")
    return Fraction(n, d)
