"""Flat (2D) shapes.

Rational inputs (int, Fraction, Decimal) keep their type where the formula
only needs + - * /; formulas that involve pi or square roots return floats.
"""

from __future__ import annotations

import math

from .. import _validate as v
from .._validate import Number


def _check_triangle(a: Number, b: Number, c: Number) -> None:
    a = v.positive(a, "a")
    b = v.positive(b, "b")
    c = v.positive(c, "c")
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("these sides cannot form a triangle")


def square_area(side: Number) -> Number:
    s = v.positive(side, "side")
    return s * s


def square_perimeter(side: Number) -> Number:
    return 4 * v.positive(side, "side")


def rectangle_area(length: Number, width: Number) -> Number:
    return v.positive(length, "length") * v.positive(width, "width")


def rectangle_perimeter(length: Number, width: Number) -> Number:
    return 2 * (v.positive(length, "length") + v.positive(width, "width"))


def triangle_area(base: Number, height: Number) -> Number:
    """Area from base and height: base * height / 2."""
    return v.positive(base, "base") * v.positive(height, "height") / 2


def triangle_area_from_sides(a: Number, b: Number, c: Number) -> float:
    """Area from three sides (Heron's formula)."""
    _check_triangle(a, b, c)
    x, y, z = float(a), float(b), float(c)
    s = (x + y + z) / 2
    return math.sqrt(s * (s - x) * (s - y) * (s - z))


def triangle_perimeter(a: Number, b: Number, c: Number) -> Number:
    """Perimeter of any triangle (the three sides must form a triangle)."""
    _check_triangle(a, b, c)
    return a + b + c


def rhombus_area(d1: Number, d2: Number) -> Number:
    """Area from the two diagonals: d1 * d2 / 2."""
    return v.positive(d1, "d1") * v.positive(d2, "d2") / 2


def rhombus_perimeter(side: Number) -> Number:
    return 4 * v.positive(side, "side")


def parallelogram_area(base: Number, height: Number) -> Number:
    return v.positive(base, "base") * v.positive(height, "height")


def parallelogram_perimeter(a: Number, b: Number) -> Number:
    return 2 * (v.positive(a, "a") + v.positive(b, "b"))


def trapezoid_area(a: Number, b: Number, height: Number) -> Number:
    """Area of a trapezoid with parallel sides a, b: (a + b) * height / 2."""
    return (v.positive(a, "a") + v.positive(b, "b")) * v.positive(height, "height") / 2


def trapezoid_perimeter(a: Number, b: Number, c: Number, d: Number) -> Number:
    """Perimeter of a trapezoid from its four sides."""
    return v.positive(a, "a") + v.positive(b, "b") + v.positive(c, "c") + v.positive(d, "d")


def regular_polygon_area(sides: int, length: Number) -> float:
    """Area of a regular polygon with *sides* sides of the given *length*."""
    n = v.integer(sides, "sides", minimum=3)
    s = float(v.positive(length, "length"))
    return n * s * s / (4 * math.tan(math.pi / n))


def regular_polygon_perimeter(sides: int, length: Number) -> Number:
    n = v.integer(sides, "sides", minimum=3)
    return n * v.positive(length, "length")
