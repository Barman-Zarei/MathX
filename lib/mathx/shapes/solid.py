"""Solid (3D) shapes."""

from __future__ import annotations

import math

from .. import _validate as v
from .._validate import Number


def cube_volume(side: Number) -> Number:
    s = v.positive(side, "side")
    return s * s * s


def cube_surface_area(side: Number) -> Number:
    s = v.positive(side, "side")
    return 6 * s * s


def cuboid_volume(length: Number, width: Number, height: Number) -> Number:
    return v.positive(length, "length") * v.positive(width, "width") * v.positive(height, "height")


def cuboid_surface_area(length: Number, width: Number, height: Number) -> Number:
    x = v.positive(length, "length")
    w = v.positive(width, "width")
    h = v.positive(height, "height")
    return 2 * (x * w + x * h + w * h)


def cylinder_volume(radius: Number, height: Number) -> float:
    r = float(v.positive(radius, "radius"))
    return math.pi * r * r * float(v.positive(height, "height"))


def cylinder_surface_area(radius: Number, height: Number) -> float:
    r = float(v.positive(radius, "radius"))
    return 2 * math.pi * r * (r + float(v.positive(height, "height")))


def cone_volume(radius: Number, height: Number) -> float:
    r = float(v.positive(radius, "radius"))
    return math.pi * r * r * float(v.positive(height, "height")) / 3


def cone_surface_area(radius: Number, height: Number) -> float:
    r = float(v.positive(radius, "radius"))
    h = float(v.positive(height, "height"))
    return math.pi * r * (r + math.hypot(r, h))


def sphere_volume(radius: Number) -> float:
    r = float(v.positive(radius, "radius"))
    return 4 / 3 * math.pi * r**3


def sphere_surface_area(radius: Number) -> float:
    r = float(v.positive(radius, "radius"))
    return 4 * math.pi * r * r


def prism_volume(base_area: Number, height: Number) -> Number:
    return v.positive(base_area, "base_area") * v.positive(height, "height")


def pyramid_volume(base_area: Number, height: Number) -> Number:
    return v.positive(base_area, "base_area") * v.positive(height, "height") / 3
