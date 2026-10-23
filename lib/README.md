# MathX

A dependency-free maths toolkit for Python 3.8+.

> **Status:** early development (0.1.0).

## Installation

    pip install mathx

## Quick start

    import mathx

    mathx.trapezoid_area(4, 6, 3)          # 15.0
    mathx.sin(30, degrees=True)            # 0.5
    mathx.solve_quadratic(1, -3, 2)        # (1.0, 2.0)
    mathx.gcd(12, 18, 24)                  # 6
    mathx.convert(1, "mi", "km")           # 1.609344
    mathx.evaluate("2 + 3 * sqrt(16)")     # 14.0
    mathx.formula("trapezoid area")        # '(a + b) * height / 2'

## What is inside

| Area | Examples |
| --- | --- |
| Circle | `circle_area`, `circle_circumference`, `sector_area`, `arc_length`, `ellipse_area` |
| Plane shapes | `square_area`, `rectangle_perimeter`, `triangle_area_from_sides`, `trapezoid_area`, `regular_polygon_area` |
| Solids | `cube_volume`, `cuboid_volume`, `cylinder_volume`, `cone_volume`, `sphere_volume`, `pyramid_volume` |
| Trigonometry | `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh` |
| Arithmetic | `add`, `divide`, `power`, `sqrt`, `log(x, base)`, `ln`, `log2`, `log10` |
| Number theory | `gcd`, `lcm`, `is_prime`, `prime_factors`, `factorial`, `fibonacci`, `combinations`, `permutations` |
| Algebra | `solve_quadratic`, `solve_linear_system`, `simplify_fraction` |
| Statistics | `mean`, `median`, `mode`, `variance`, `std_dev` |
| Coordinates | `distance`, `midpoint`, `slope`, `polygon_area`, `polygon_perimeter` |
| Units | `convert`, `list_units` |
| Reference | `formula`, `list_formulas`, `evaluate` |

## Conventions

- Angles use radians unless you pass `degrees=True`.
- Invalid input raises `TypeError` (wrong type) or `ValueError` (wrong value) with a clear message.
- `int`, `float`, `Fraction` and `Decimal` are accepted. Formulas that only use `+ - * /`
  keep `Fraction` and `Decimal` exact; formulas with pi or roots return `float`.

## Development

    pip install -e ".[dev]"
    pytest
    ruff check .

## License

MIT
