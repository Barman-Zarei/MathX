"""Circles, sectors and ellipses."""

from __future__ import annotations

import math

from . import _validate as v
from ._validate import Number


def circle_area(radius: Number) -> float:
    """Area of a circle: pi * r^2."""
    r = float(v.positive(radius, "radius"))
    return math.pi * r * r


def circle_circumference(radius: Number) -> float:
    """Circumference of a circle: 2 * pi * r."""
    r = float(v.positive(radius, "radius"))
    return 2 * math.pi * r


def sector_area(radius: Number, angle: Number, degrees: bool = False) -> float:
    """Area of a circular sector. *angle* is in radians unless degrees=True."""
    r = float(v.positive(radius, "radius"))
    theta = v.angle_in_radians(v.positive(angle, "angle"), degrees)
    return 0.5 * r * r * theta


def arc_length(radius: Number, angle: Number, degrees: bool = False) -> float:
    """Length of a circular arc. *angle* is in radians unless degrees=True."""
    r = float(v.positive(radius, "radius"))
    theta = v.angle_in_radians(v.positive(angle, "angle"), degrees)
    return r * theta


def ellipse_area(a: Number, b: Number) -> float:
    """Area of an ellipse with semi-axes *a* and *b*: pi * a * b."""
    return math.pi * float(v.positive(a, "a")) * float(v.positive(b, "b"))


def ellipse_perimeter(a: Number, b: Number) -> float:
    """Perimeter of an ellipse (Ramanujan's approximation)."""
    x = float(v.positive(a, "a"))
    y = float(v.positive(b, "b"))
    return math.pi * (3 * (x + y) - math.sqrt((3 * x + y) * (x + 3 * y)))
