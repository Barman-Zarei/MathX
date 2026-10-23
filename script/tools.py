"""Tool registry and input/output helpers for the MathX app.

Everything here is plain Python (no Kivy), so it can be tested on its own.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Tuple

import mathx

MAX_FACTORIAL = 5000
MAX_FIBONACCI = 100_000
MAX_FACTORING = 10 ** 14


@dataclass(frozen=True)
class Field:
    key: str  # keyword argument name passed to the tool function
    label: str
    kind: str = "num"  # num | int | list | point | points | matrix | text | bool
    hint: str = ""
    required: bool = True


@dataclass(frozen=True)
class Tool:
    title: str
    func: Callable[..., Any]
    fields: Tuple[Field, ...] = ()
    note: str = ""
    formatter: Optional[Callable[[Any], Tuple[str, str]]] = None


# ---------------------------------------------------------------- parsing


def _number(text: str, label: str) -> Any:
    text = text.strip()
    if not text:
        raise ValueError(f"{label}: enter a value")
    try:
        value = mathx.evaluate(text)
    except ValueError as exc:
        raise ValueError(f"{label}: {exc}") from None
    if isinstance(value, complex):
        raise ValueError(f"{label}: enter a real number")
    return value


def _integer(text: str, label: str) -> int:
    value = _number(text, label)
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    if not isinstance(value, int):
        raise ValueError(f"{label}: enter a whole number")
    return value


def _split_items(text: str) -> List[str]:
    parts = re.split(r"[,;]", text) if re.search(r"[,;]", text) else text.split()
    return [p for p in (s.strip() for s in parts) if p]


def _numbers(text: str, label: str) -> List[Any]:
    items = [_number(p, label) for p in _split_items(text)]
    if not items:
        raise ValueError(f"{label}: enter at least one number")
    return items


def parse_field(field: Field, raw: Any) -> Any:
    """Turn what the person typed into the Python value the tool expects."""
    if field.kind == "bool":
        return bool(raw)
    text = (raw or "").strip()
    kind = field.kind
    if kind == "text":
        if not text:
            raise ValueError(f"{field.label}: enter some text")
        return text
    if kind == "num":
        return _number(text, field.label)
    if kind == "int":
        return _integer(text, field.label)
    if kind == "list":
        return _numbers(text, field.label)
    if kind == "point":
        return tuple(_numbers(text, field.label))
    if kind == "points":
        rows = [r for r in re.split(r"[;\n]", text) if r.strip()]
        if not rows:
            raise ValueError(f"{field.label}: enter points like 0,0; 4,0; 4,3")
        return [tuple(_numbers(r, field.label)) for r in rows]
    if kind == "matrix":
        rows = [r for r in text.split(";") if r.strip()]
        if not rows:
            raise ValueError(f"{field.label}: enter rows like 2, 1; 1, 3")
        return [_numbers(r, field.label) for r in rows]
    raise ValueError(f"unknown field kind {kind!r}")


def collect_kwargs(tool: Tool, raw_values: Dict[str, Any]) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {}
    for field in tool.fields:
        raw = raw_values.get(field.key)
        if field.kind != "bool" and not field.required and not (raw or "").strip():
            continue
        kwargs[field.key] = parse_field(field, raw)
    return kwargs


# ------------------------------------------------------------- formatting


def _float(x: float) -> str:
    if x == 0:
        return "0"
    if abs(x) >= 1e12 or abs(x) < 1e-6:
        return f"{x:.10g}"
    return f"{x:.12g}"


def _complex(z: complex) -> str:
    if z.imag == 0:
        return _float(z.real)
    real = _float(z.real) if z.real != 0 else ""
    sign = "-" if z.imag < 0 else ("+ " if real else "")
    sep = " " if real and sign == "-" else ""
    return f"{real} {sign}{sep}{_float(abs(z.imag))}i".strip().replace("  ", " ")


def format_result(value: Any) -> Tuple[str, str]:
    """Return (main text, detail text) for any value a tool can produce."""
    if isinstance(value, bool):
        return ("Yes" if value else "No"), ""
    if isinstance(value, int):
        digits = len(str(abs(value)))
        if digits > 24:
            return f"{value:.8e}", f"{digits} digits"
        return str(value), ""
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator), ""
        return str(value), f"decimal: {_float(float(value))}"
    if isinstance(value, float):
        return _float(value), ""
    if isinstance(value, complex):
        return _complex(value), ""
    if isinstance(value, (list, tuple)):
        items = [format_result(item)[0] for item in value]
        return ", ".join(items) if items else "none", ""
    return str(value), ""


def _roots(value: Tuple[Any, Any]) -> Tuple[str, str]:
    a, b = (format_result(r)[0] for r in value)
    if a == b:
        return f"x = {a}", "double root"
    return f"x1 = {a}\nx2 = {b}", ""


def _solution(values: List[Any]) -> Tuple[str, str]:
    names = "xyzuvwst"
    lines = [
        f"{names[i] if i < len(names) else 'x' + str(i + 1)} = {format_result(x)[0]}"
        for i, x in enumerate(values)
    ]
    return "\n".join(lines), ""


def _unit_list(table: Dict[str, List[str]]) -> Tuple[str, str]:
    return "\n".join(f"{kind}: {', '.join(units)}" for kind, units in table.items()), ""


# --------------------------------------------------------------- registry


def F(key: str, label: str, kind: str = "num", hint: str = "", required: bool = True) -> Field:
    return Field(key, label, kind, hint, required)


def tool(title: str, func: Callable[..., Any], *fields: Field, note: str = "",
         fmt: Optional[Callable[[Any], Tuple[str, str]]] = None) -> Tool:
    return Tool(title, func, tuple(fields), note, fmt)


def _capped(limit: int, name: str, func: Callable[[int], Any]) -> Callable[[int], Any]:
    def run(n: int) -> Any:
        if n > limit:
            raise ValueError(f"{name}: the app accepts values up to {limit:,}")
        return func(n)

    return run


_ANGLE = F("x", "Angle", hint="30")
_DEG = F("degrees", "Angle is in degrees", "bool")
_OUT_DEG = F("degrees", "Answer in degrees", "bool")
_R = F("radius", "Radius", hint="5")
_H = F("height", "Height", hint="10")
_SIDE = F("side", "Side", hint="4")

CATEGORIES: Dict[str, List[Tool]] = {
    "Calculator": [
        tool("Expression", mathx.evaluate, F("expression", "Expression", "text", "2 + 3 * sqrt(16)"),
             note="Use + - * / ^ ( ), pi, e, sqrt, sin, cos, tan, log, ln, factorial, sind..."),
    ],
    "Shapes": [
        tool("Square area", mathx.square_area, _SIDE),
        tool("Square perimeter", mathx.square_perimeter, _SIDE),
        tool("Rectangle area", mathx.rectangle_area, F("length", "Length", hint="8"), F("width", "Width", hint="3")),
        tool("Rectangle perimeter", mathx.rectangle_perimeter, F("length", "Length", hint="8"), F("width", "Width", hint="3")),
        tool("Triangle area", mathx.triangle_area, F("base", "Base", hint="6"), _H),
        tool("Triangle area (3 sides)", mathx.triangle_area_from_sides, F("a", "Side a", hint="3"), F("b", "Side b", hint="4"), F("c", "Side c", hint="5"), note="Heron's formula"),
        tool("Triangle perimeter", mathx.triangle_perimeter, F("a", "Side a", hint="3"), F("b", "Side b", hint="4"), F("c", "Side c", hint="5")),
        tool("Rhombus area", mathx.rhombus_area, F("d1", "Big diagonal", hint="10"), F("d2", "Small diagonal", hint="6")),
        tool("Rhombus perimeter", mathx.rhombus_perimeter, _SIDE),
        tool("Parallelogram area", mathx.parallelogram_area, F("base", "Base", hint="7"), _H),
        tool("Parallelogram perimeter", mathx.parallelogram_perimeter, F("a", "Big side", hint="7"), F("b", "Small side", hint="4")),
        tool("Trapezoid area", mathx.trapezoid_area, F("a", "Big base", hint="10"), F("b", "Small base", hint="6"), _H),
        tool("Trapezoid perimeter", mathx.trapezoid_perimeter, F("a", "Base a", hint="10"), F("b", "Base b", hint="6"), F("c", "Leg c", hint="5"), F("d", "Leg d", hint="5")),
        tool("Polygon area", mathx.regular_polygon_area, F("sides", "Number of sides", "int", "6"), F("length", "Side length", hint="4"), note="Regular polygon"),
        tool("Polygon perimeter", mathx.regular_polygon_perimeter, F("sides", "Number of sides", "int", "6"), F("length", "Side length", hint="4"), note="Regular polygon"),
    ],
    "Circle": [
        tool("Area", mathx.circle_area, _R),
        tool("Circumference", mathx.circle_circumference, _R),
        tool("Sector area", mathx.sector_area, _R, F("angle", "Angle", hint="90"), F("degrees", "Angle is in degrees", "bool")),
        tool("Arc length", mathx.arc_length, _R, F("angle", "Angle", hint="90"), F("degrees", "Angle is in degrees", "bool")),
        tool("Ellipse area", mathx.ellipse_area, F("a", "Semi-axis a", hint="5"), F("b", "Semi-axis b", hint="3")),
        tool("Ellipse perimeter", mathx.ellipse_perimeter, F("a", "Semi-axis a", hint="5"), F("b", "Semi-axis b", hint="3"), note="Ramanujan approximation"),
    ],
    "Solids": [
        tool("Cube volume", mathx.cube_volume, _SIDE),
        tool("Cube surface", mathx.cube_surface_area, _SIDE),
        tool("Cuboid volume", mathx.cuboid_volume, F("length", "Length", hint="5"), F("width", "Width", hint="4"), _H),
        tool("Cuboid surface", mathx.cuboid_surface_area, F("length", "Length", hint="5"), F("width", "Width", hint="4"), _H),
        tool("Cylinder volume", mathx.cylinder_volume, _R, _H),
        tool("Cylinder surface", mathx.cylinder_surface_area, _R, _H),
        tool("Cone volume", mathx.cone_volume, _R, _H),
        tool("Cone surface", mathx.cone_surface_area, _R, _H),
        tool("Sphere volume", mathx.sphere_volume, _R),
        tool("Sphere surface", mathx.sphere_surface_area, _R),
        tool("Prism volume", mathx.prism_volume, F("base_area", "Base area", hint="12"), _H),
        tool("Pyramid volume", mathx.pyramid_volume, F("base_area", "Base area", hint="12"), _H),
    ],
    "Trig": [
        tool("sin", mathx.sin, _ANGLE, _DEG),
        tool("cos", mathx.cos, _ANGLE, _DEG),
        tool("tan", mathx.tan, _ANGLE, _DEG),
        tool("asin", mathx.asin, F("x", "Value (-1 to 1)", hint="0.5"), _OUT_DEG),
        tool("acos", mathx.acos, F("x", "Value (-1 to 1)", hint="0.5"), _OUT_DEG),
        tool("atan", mathx.atan, F("x", "Value", hint="1"), _OUT_DEG),
        tool("atan2", mathx.atan2, F("y", "y", hint="1"), F("x", "x", hint="1"), _OUT_DEG),
        tool("sinh", mathx.sinh, F("x", "Value", hint="1")),
        tool("cosh", mathx.cosh, F("x", "Value", hint="1")),
        tool("tanh", mathx.tanh, F("x", "Value", hint="1")),
        tool("To radians", mathx.to_radians, F("value", "Degrees", hint="180")),
        tool("To degrees", mathx.to_degrees, F("value", "Radians", hint="pi")),
    ],
    "Arithmetic": [
        tool("Add", mathx.add, F("a", "First number", hint="12"), F("b", "Second number", hint="8")),
        tool("Subtract", mathx.subtract, F("a", "First number", hint="12"), F("b", "Second number", hint="8")),
        tool("Multiply", mathx.multiply, F("a", "First number", hint="12"), F("b", "Second number", hint="8")),
        tool("Divide", mathx.divide, F("a", "First number", hint="12"), F("b", "Second number", hint="8")),
        tool("Power", mathx.power, F("base", "Base", hint="2"), F("exponent", "Exponent", hint="10")),
        tool("Square root", mathx.sqrt, F("x", "Number", hint="144")),
        tool("Log", mathx.log, F("x", "Number", hint="1000"), F("base", "Base (empty = e)", hint="10", required=False)),
        tool("Log2", mathx.log2, F("x", "Number", hint="8")),
        tool("Log10", mathx.log10, F("x", "Number", hint="1000")),
        tool("Ln", mathx.ln, F("x", "Number", hint="e")),
    ],
    "Numbers": [
        tool("GCD", lambda numbers: mathx.gcd(*numbers), F("numbers", "Whole numbers", "list", "12, 18, 24"), note="Greatest common divisor"),
        tool("LCM", lambda numbers: mathx.lcm(*numbers), F("numbers", "Whole numbers", "list", "4, 6, 10"), note="Least common multiple"),
        tool("Is prime", mathx.is_prime, F("n", "Number", "int", "97")),
        tool("Prime factors", _capped(MAX_FACTORING, "Prime factors", mathx.prime_factors), F("n", "Number (2 or more)", "int", "360")),
        tool("Factorial", _capped(MAX_FACTORIAL, "Factorial", mathx.factorial), F("n", "n", "int", "10")),
        tool("Fibonacci", _capped(MAX_FIBONACCI, "Fibonacci", mathx.fibonacci), F("n", "Position n", "int", "10")),
        tool("Combinations", mathx.combinations, F("n", "n (total)", "int", "5"), F("k", "k (chosen)", "int", "2"), note="Order does not matter"),
        tool("Permutations", mathx.permutations, F("n", "n (total)", "int", "5"), F("k", "k (empty = n)", "int", "2", required=False), note="Order matters"),
    ],
    "Algebra": [
        tool("Quadratic", mathx.solve_quadratic, F("a", "a", hint="1"), F("b", "b", hint="-3"), F("c", "c", hint="2"), note="Solves a*x^2 + b*x + c = 0", fmt=_roots),
        tool("Linear system", mathx.solve_linear_system, F("matrix", "Coefficients (rows split by ;)", "matrix", "2, 1; 1, 3"), F("constants", "Constants", "list", "5, 10"), note="Whole numbers give exact fractions", fmt=_solution),
        tool("Simplify fraction", mathx.simplify_fraction, F("numerator", "Numerator", "int", "6"), F("denominator", "Denominator", "int", "8")),
    ],
    "Stats": [
        tool("Mean", mathx.mean, F("data", "Numbers", "list", "2, 4, 4, 4, 5, 5, 7, 9")),
        tool("Median", mathx.median, F("data", "Numbers", "list", "2, 4, 4, 4, 5, 5, 7, 9")),
        tool("Mode", mathx.mode, F("data", "Numbers", "list", "2, 4, 4, 4, 5, 5, 7, 9")),
        tool("Variance", lambda data, population=False: mathx.variance(data, sample=not population), F("data", "Numbers", "list", "2, 4, 4, 4, 5, 5, 7, 9"), F("population", "Whole population (not a sample)", "bool")),
        tool("Std deviation", lambda data, population=False: mathx.std_dev(data, sample=not population), F("data", "Numbers", "list", "2, 4, 4, 4, 5, 5, 7, 9"), F("population", "Whole population (not a sample)", "bool")),
    ],
    "Coordinates": [
        tool("Distance", mathx.distance, F("p", "Point 1", "point", "0, 0"), F("q", "Point 2", "point", "3, 4")),
        tool("Midpoint", mathx.midpoint, F("p", "Point 1", "point", "0, 0"), F("q", "Point 2", "point", "4, 2")),
        tool("Slope", mathx.slope, F("p", "Point 1", "point", "0, 0"), F("q", "Point 2", "point", "2, 4")),
        tool("Polygon area", mathx.polygon_area, F("points", "Corners in order (split by ;)", "points", "0,0; 4,0; 4,3; 0,3")),
        tool("Polygon perimeter", mathx.polygon_perimeter, F("points", "Corners in order (split by ;)", "points", "0,0; 4,0; 4,3; 0,3")),
    ],
    "Units": [
        tool("Convert", mathx.convert, F("value", "Value", hint="1"), F("from_unit", "From", "text", "mi"), F("to_unit", "To", "text", "km"), note="Length, mass, time, angle, temperature"),
        tool("Unit list", lambda: mathx.list_units(), note="Every unit you can type", fmt=_unit_list),
    ],
    "Formulas": [
        tool("Show formula", mathx.formula, F("name", "Name", "text", "trapezoid area"), F("latex", "Show as LaTeX", "bool")),
        tool("All formulas", lambda: "\n".join(mathx.list_formulas()), note="Names you can look up"),
    ],
}


def pick_formatter(tool_: Tool) -> Callable[[Any], Tuple[str, str]]:
    return tool_.formatter or format_result


def run_tool(tool_: Tool, raw_values: Dict[str, Any]) -> Tuple[str, str]:
    """Parse inputs, call the tool and format the answer. Raises ValueError/TypeError."""
    kwargs = collect_kwargs(tool_, raw_values)
    return pick_formatter(tool_)(tool_.func(**kwargs))
