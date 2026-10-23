"""Unit conversion for length, mass, time, angle and temperature."""

from __future__ import annotations

import math
from typing import Dict, List

from . import _validate as v
from ._validate import Number

_LINEAR: Dict[str, Dict[str, float]] = {
    "length": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.344,
    },
    "mass": {"mg": 1e-6, "g": 1e-3, "kg": 1.0, "t": 1000.0, "oz": 0.028349523125, "lb": 0.45359237},
    "time": {"ms": 0.001, "s": 1.0, "min": 60.0, "h": 3600.0, "d": 86400.0},
    "angle": {"rad": 1.0, "deg": math.pi / 180, "grad": math.pi / 200, "turn": 2 * math.pi},
}
_TEMPERATURE = ("c", "f", "k")

_ALIASES = {
    "millimeter": "mm",
    "millimeters": "mm",
    "centimeter": "cm",
    "centimeters": "cm",
    "meter": "m",
    "meters": "m",
    "metre": "m",
    "metres": "m",
    "kilometer": "km",
    "kilometers": "km",
    "inch": "in",
    "inches": "in",
    "foot": "ft",
    "feet": "ft",
    "yard": "yd",
    "yards": "yd",
    "mile": "mi",
    "miles": "mi",
    "milligram": "mg",
    "milligrams": "mg",
    "gram": "g",
    "grams": "g",
    "kilogram": "kg",
    "kilograms": "kg",
    "tonne": "t",
    "ton": "t",
    "tonnes": "t",
    "ounce": "oz",
    "ounces": "oz",
    "pound": "lb",
    "pounds": "lb",
    "lbs": "lb",
    "millisecond": "ms",
    "milliseconds": "ms",
    "second": "s",
    "seconds": "s",
    "sec": "s",
    "minute": "min",
    "minutes": "min",
    "hour": "h",
    "hours": "h",
    "hr": "h",
    "day": "d",
    "days": "d",
    "radian": "rad",
    "radians": "rad",
    "degree": "deg",
    "degrees": "deg",
    "gradian": "grad",
    "gradians": "grad",
    "gon": "grad",
    "turns": "turn",
    "celsius": "c",
    "fahrenheit": "f",
    "kelvin": "k",
}


def _norm(unit: str) -> str:
    if not isinstance(unit, str):
        raise TypeError("unit must be a string")
    key = unit.strip().lower().lstrip("\u00b0")
    return _ALIASES.get(key, key)


def _category(unit: str) -> str:
    if unit in _TEMPERATURE:
        return "temperature"
    for name, table in _LINEAR.items():
        if unit in table:
            return name
    raise ValueError(f"unknown unit {unit!r}; see list_units()")


def _tidy(x: float) -> float:
    return float(f"{x:.12g}")


def _temperature(x: float, source: str, target: str) -> float:
    kelvin = {"c": x + 273.15, "f": (x - 32) * 5 / 9 + 273.15, "k": x}[source]
    if kelvin < 0:
        raise ValueError("temperature is below absolute zero")
    return {"c": kelvin - 273.15, "f": (kelvin - 273.15) * 9 / 5 + 32, "k": kelvin}[target]


def convert(value: Number, from_unit: str, to_unit: str) -> float:
    """Convert *value* between two units of the same kind, e.g. convert(1, "mi", "km")."""
    x = v.as_float(value, "value")
    a, b = _norm(from_unit), _norm(to_unit)
    kind_a, kind_b = _category(a), _category(b)
    if kind_a != kind_b:
        raise ValueError(f"cannot convert {kind_a} to {kind_b}")
    if kind_a == "temperature":
        return _tidy(_temperature(x, a, b))
    table = _LINEAR[kind_a]
    return _tidy(x * table[a] / table[b])


def list_units() -> Dict[str, List[str]]:
    """Supported unit symbols grouped by kind."""
    units = {name: list(table) for name, table in _LINEAR.items()}
    units["temperature"] = ["C", "F", "K"]
    return units
