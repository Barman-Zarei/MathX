"""A small reference of geometry and algebra formulas as text or LaTeX."""

from __future__ import annotations

import difflib
from typing import Dict, List, Tuple

_FORMULAS: Dict[str, Tuple[str, str]] = {
    "circle area": ("pi * r^2", r"A = \pi r^2"),
    "circle circumference": ("2 * pi * r", r"C = 2 \pi r"),
    "sector area": ("r^2 * angle / 2  (angle in radians)", r"A = \frac{r^2 \theta}{2}"),
    "arc length": ("r * angle  (angle in radians)", r"s = r \theta"),
    "ellipse area": ("pi * a * b", r"A = \pi a b"),
    "square area": ("side * side", r"A = s^2"),
    "square perimeter": ("4 * side", r"P = 4s"),
    "rectangle area": ("length * width", r"A = l w"),
    "rectangle perimeter": ("2 * (length + width)", r"P = 2(l + w)"),
    "triangle area": ("base * height / 2", r"A = \frac{b h}{2}"),
    "triangle area heron": (
        "sqrt(s * (s - a) * (s - b) * (s - c)), where s = (a + b + c) / 2",
        r"A = \sqrt{s(s-a)(s-b)(s-c)},\ s = \frac{a+b+c}{2}",
    ),
    "triangle perimeter": ("a + b + c", r"P = a + b + c"),
    "rhombus area": ("d1 * d2 / 2", r"A = \frac{d_1 d_2}{2}"),
    "rhombus perimeter": ("4 * side", r"P = 4s"),
    "parallelogram area": ("base * height", r"A = b h"),
    "parallelogram perimeter": ("2 * (a + b)", r"P = 2(a + b)"),
    "trapezoid area": ("(a + b) * height / 2", r"A = \frac{(a + b) h}{2}"),
    "trapezoid perimeter": ("a + b + c + d", r"P = a + b + c + d"),
    "regular polygon area": ("n * s^2 / (4 * tan(pi / n))", r"A = \frac{n s^2}{4 \tan(\pi / n)}"),
    "cube volume": ("side^3", r"V = s^3"),
    "cube surface area": ("6 * side^2", r"S = 6 s^2"),
    "cuboid volume": ("length * width * height", r"V = l w h"),
    "cylinder volume": ("pi * r^2 * h", r"V = \pi r^2 h"),
    "cylinder surface area": ("2 * pi * r * (r + h)", r"S = 2 \pi r (r + h)"),
    "cone volume": ("pi * r^2 * h / 3", r"V = \frac{\pi r^2 h}{3}"),
    "sphere volume": ("4/3 * pi * r^3", r"V = \frac{4}{3} \pi r^3"),
    "sphere surface area": ("4 * pi * r^2", r"S = 4 \pi r^2"),
    "pyramid volume": ("base area * height / 3", r"V = \frac{B h}{3}"),
    "pythagorean theorem": ("a^2 + b^2 = c^2", r"a^2 + b^2 = c^2"),
    "quadratic formula": (
        "x = (-b +- sqrt(b^2 - 4ac)) / (2a)",
        r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
    ),
    "distance": ("sqrt((x2 - x1)^2 + (y2 - y1)^2)", r"d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}"),
    "midpoint": (
        "((x1 + x2) / 2, (y1 + y2) / 2)",
        r"M = \left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right)",
    ),
    "slope": ("(y2 - y1) / (x2 - x1)", r"m = \frac{y_2 - y_1}{x_2 - x_1}"),
    "mean": ("sum of values / number of values", r"\bar{x} = \frac{1}{n} \sum x_i"),
    "variance": (
        "sum((x - mean)^2) / (n - 1)  (sample)",
        r"s^2 = \frac{1}{n-1} \sum (x_i - \bar{x})^2",
    ),
    "combinations": ("n! / (k! * (n - k)!)", r"\binom{n}{k} = \frac{n!}{k!(n-k)!}"),
    "permutations": ("n! / (n - k)!", r"P(n, k) = \frac{n!}{(n-k)!}"),
}

_ALIASES = {
    "circumference": "circle circumference",
    "pythagoras": "pythagorean theorem",
    "heron": "triangle area heron",
    "quadratic": "quadratic formula",
}


def _key(name: str) -> str:
    return " ".join(str(name).lower().replace("_", " ").replace("-", " ").split())


def list_formulas() -> List[str]:
    """Names accepted by formula(), sorted alphabetically."""
    return sorted(_FORMULAS)


def formula(name: str, latex: bool = False) -> str:
    """Return a formula as plain text, or as LaTeX with latex=True."""
    key = _key(name)
    key = _ALIASES.get(key, key)
    if key not in _FORMULAS:
        close = difflib.get_close_matches(key, _FORMULAS, n=3)
        hint = f" Did you mean: {', '.join(close)}?" if close else " See list_formulas()."
        raise ValueError(f"unknown formula {name!r}.{hint}")
    text, tex = _FORMULAS[key]
    return tex if latex else text
