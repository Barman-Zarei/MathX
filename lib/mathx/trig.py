"""Trigonometric and hyperbolic functions.

Functions that take an angle use radians unless ``degrees=True``; the inverse
functions return radians unless ``degrees=True``. Results whose magnitude is
below 1e-15 are returned as exactly 0.0, so sin(180, degrees=True) == 0.0.
"""

from __future__ import annotations

import math

from . import _validate as v
from ._validate import Number


def _clean(x: float) -> float:
    return 0.0 if abs(x) < 1e-15 else x


def _out(radians: float, degrees: bool) -> float:
    return _clean(math.degrees(radians)) if degrees else radians


def sin(x: Number, degrees: bool = False) -> float:
    return _clean(math.sin(v.angle_in_radians(x, degrees, "x")))


def cos(x: Number, degrees: bool = False) -> float:
    return _clean(math.cos(v.angle_in_radians(x, degrees, "x")))


def tan(x: Number, degrees: bool = False) -> float:
    r = v.angle_in_radians(x, degrees, "x")
    if abs(math.cos(r)) < 1e-12:
        raise ValueError("tan is undefined at this angle")
    return _clean(math.tan(r))


def asin(x: Number, degrees: bool = False) -> float:
    value = v.as_float(x, "x")
    if not -1 <= value <= 1:
        raise ValueError("asin needs a value between -1 and 1")
    return _out(math.asin(value), degrees)


def acos(x: Number, degrees: bool = False) -> float:
    value = v.as_float(x, "x")
    if not -1 <= value <= 1:
        raise ValueError("acos needs a value between -1 and 1")
    return _out(math.acos(value), degrees)


def atan(x: Number, degrees: bool = False) -> float:
    return _out(math.atan(v.as_float(x, "x")), degrees)


def atan2(y: Number, x: Number, degrees: bool = False) -> float:
    return _out(math.atan2(v.as_float(y, "y"), v.as_float(x, "x")), degrees)


def _hyper(func, x: Number) -> float:
    try:
        return func(v.as_float(x, "x"))
    except OverflowError:
        raise ValueError("result is too large") from None


def sinh(x: Number) -> float:
    return _hyper(math.sinh, x)


def cosh(x: Number) -> float:
    return _hyper(math.cosh, x)


def tanh(x: Number) -> float:
    return _hyper(math.tanh, x)


def to_radians(value: Number) -> float:
    """Convert degrees to radians."""
    return math.radians(v.as_float(value, "value"))


def to_degrees(value: Number) -> float:
    """Convert radians to degrees."""
    return math.degrees(v.as_float(value, "value"))
