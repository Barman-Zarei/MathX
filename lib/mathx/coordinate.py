"""Coordinate geometry. Points are sequences of numbers, e.g. (3, 4)."""

from __future__ import annotations

import math
from typing import Optional, Sequence, Tuple

from . import _validate as v
from ._validate import Number

Point = Sequence[Number]


def _pt(p: Point, name: str, dims: Optional[int] = None) -> Tuple[float, ...]:
    if isinstance(p, (str, bytes)) or not hasattr(p, "__iter__"):
        raise TypeError(f"{name} must be a sequence of numbers")
    coords = tuple(float(v.number(c, f"{name}[{i}]")) for i, c in enumerate(p))
    if len(coords) < 2:
        raise ValueError(f"{name} needs at least 2 coordinates")
    if dims is not None and len(coords) != dims:
        raise ValueError("points must have the same number of coordinates")
    return coords


def _polygon(points: Sequence[Point]) -> Tuple[Tuple[float, ...], ...]:
    pts = tuple(_pt(p, f"points[{i}]", 2) for i, p in enumerate(points))
    if len(pts) < 3:
        raise ValueError("a polygon needs at least 3 points")
    return pts


def distance(p: Point, q: Point) -> float:
    a = _pt(p, "p")
    return math.dist(a, _pt(q, "q", len(a)))


def midpoint(p: Point, q: Point) -> Tuple[float, ...]:
    a = _pt(p, "p")
    b = _pt(q, "q", len(a))
    return tuple((x + y) / 2 for x, y in zip(a, b))


def slope(p: Point, q: Point) -> float:
    (x1, y1), (x2, y2) = _pt(p, "p", 2), _pt(q, "q", 2)
    if x1 == x2:
        raise ValueError("a vertical line has no slope")
    return (y2 - y1) / (x2 - x1)


def polygon_area(points: Sequence[Point]) -> float:
    """Area of a simple polygon from its vertices in order (shoelace formula)."""
    pts = _polygon(points)
    total = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def polygon_perimeter(points: Sequence[Point]) -> float:
    pts = _polygon(points)
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:] + pts[:1]))
