"""Input validation helpers shared by every module (internal use only)."""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction
from typing import Any, Iterable, List, Optional, Union

Number = Union[int, float, Fraction, Decimal]
NUMERIC_TYPES = (int, float, Fraction, Decimal)


def number(value: Any, name: str = "value") -> Number:
    """Return *value* if it is a finite real number, otherwise raise."""
    if isinstance(value, bool) or not isinstance(value, NUMERIC_TYPES):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if isinstance(value, (float, Decimal)) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def positive(value: Any, name: str = "value") -> Number:
    value = number(value, name)
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def non_negative(value: Any, name: str = "value") -> Number:
    value = number(value, name)
    if value < 0:
        raise ValueError(f"{name} must not be negative")
    return value


def integer(value: Any, name: str = "value", minimum: Optional[int] = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def as_float(value: Any, name: str = "value") -> float:
    return float(number(value, name))


def angle_in_radians(value: Any, degrees: bool, name: str = "angle") -> float:
    """Convert an angle to radians; *degrees* says what the input unit is."""
    x = as_float(value, name)
    return math.radians(x) if degrees else x


def number_list(values: Iterable[Any], name: str = "values", min_length: int = 1) -> List[Number]:
    if isinstance(values, (str, bytes)) or not hasattr(values, "__iter__"):
        raise TypeError(f"{name} must be a list of numbers")
    items = [number(item, f"{name}[{i}]") for i, item in enumerate(values)]
    if len(items) < min_length:
        raise ValueError(f"{name} needs at least {min_length} value(s)")
    return items
