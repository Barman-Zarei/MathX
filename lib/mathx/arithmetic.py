"""Basic arithmetic, powers, roots and logarithms."""

from __future__ import annotations

import math
from typing import Union

from . import _validate as v
from ._validate import Number

Numeric = Union[int, float, complex, Number]


def _flt(x: Number) -> Union[int, float]:
    return x if isinstance(x, int) else float(x)


def add(a: Number, b: Number) -> Number:
    return v.number(a, "a") + v.number(b, "b")


def subtract(a: Number, b: Number) -> Number:
    return v.number(a, "a") - v.number(b, "b")


def multiply(a: Number, b: Number) -> Number:
    return v.number(a, "a") * v.number(b, "b")


def divide(a: Number, b: Number) -> Number:
    """a / b. Raises ValueError when b is zero."""
    x, y = v.number(a, "a"), v.number(b, "b")
    if y == 0:
        raise ValueError("cannot divide by zero")
    return x / y


def power(base: Number, exponent: Number) -> Numeric:
    """base ** exponent (a negative base with a fractional exponent gives a complex number)."""
    b, e = v.number(base, "base"), v.number(exponent, "exponent")
    if b == 0 and e < 0:
        raise ValueError("zero cannot be raised to a negative power")
    if isinstance(b, int) and isinstance(e, int) and e > 0 and b.bit_length() * e > 1_000_000:
        raise ValueError("result is too large")
    try:
        return b**e
    except OverflowError:
        raise ValueError("result is too large") from None


def sqrt(x: Number) -> float:
    value = v.non_negative(x, "x")
    try:
        return math.sqrt(value)
    except OverflowError:
        raise ValueError("number is too large") from None


def log(x: Number, base: Number = math.e) -> float:
    """Logarithm of *x* in the given *base* (natural logarithm by default)."""
    value = _flt(v.positive(x, "x"))
    b = _flt(v.positive(base, "base"))
    if b == 1:
        raise ValueError("base must not be 1")
    if b == math.e:
        return math.log(value)
    if b == 10:
        return math.log10(value)
    if b == 2:
        return math.log2(value)
    return math.log(value) / math.log(b)


def ln(x: Number) -> float:
    return math.log(_flt(v.positive(x, "x")))


def log2(x: Number) -> float:
    return math.log2(_flt(v.positive(x, "x")))


def log10(x: Number) -> float:
    return math.log10(_flt(v.positive(x, "x")))
