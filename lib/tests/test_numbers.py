from fractions import Fraction

import pytest

import mathx


def test_trig_degrees_and_cleanup():
    assert mathx.sin(30, degrees=True) == pytest.approx(0.5)
    assert mathx.sin(180, degrees=True) == 0.0
    assert mathx.cos(90, degrees=True) == 0.0
    assert mathx.asin(1, degrees=True) == pytest.approx(90)
    with pytest.raises(ValueError):
        mathx.tan(90, degrees=True)
    with pytest.raises(ValueError):
        mathx.acos(2)


def test_arithmetic_errors():
    with pytest.raises(ValueError):
        mathx.divide(1, 0)
    with pytest.raises(ValueError):
        mathx.sqrt(-1)
    with pytest.raises(ValueError):
        mathx.log(0)
    with pytest.raises(ValueError):
        mathx.log(5, 1)
    with pytest.raises(ValueError):
        mathx.power(10, 10**9)


def test_logs():
    assert mathx.log(1000, 10) == 3.0
    assert mathx.log(8, 2) == 3.0
    assert mathx.log(27, 3) == pytest.approx(3)


def test_number_theory():
    assert mathx.gcd(12, 18, 24) == 6
    assert mathx.lcm(4, 6) == 12
    assert mathx.is_prime(97) and not mathx.is_prime(91)
    assert mathx.is_prime(2**61 - 1)
    assert mathx.prime_factors(360) == [2, 2, 2, 3, 3, 5]
    assert mathx.factorial(5) == 120
    assert mathx.fibonacci(10) == 55 and mathx.fibonacci(0) == 0
    assert mathx.combinations(5, 2) == 10
    assert mathx.permutations(5, 2) == 20
    with pytest.raises(TypeError):
        mathx.factorial(2.5)


def test_algebra():
    assert mathx.solve_quadratic(1, -3, 2) == (1.0, 2.0)
    r1, r2 = mathx.solve_quadratic(1, 0, 1)
    assert r1 == -1j and r2 == 1j
    assert mathx.solve_linear_system([[2, 1], [1, 3]], [5, 10]) == [1, 3]
    assert mathx.solve_linear_system([[1, 2], [3, 4]], [1, 1])[0] == Fraction(-1)
    with pytest.raises(ValueError):
        mathx.solve_linear_system([[1, 2], [2, 4]], [1, 2])
    with pytest.raises(ValueError):
        mathx.solve_quadratic(0, 1, 1)
    assert mathx.simplify_fraction(6, -8) == Fraction(-3, 4)


def test_stats():
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    assert mathx.mean(data) == 5
    assert mathx.median(data) == 4.5
    assert mathx.mode(data) == [4]
    assert mathx.std_dev(data, sample=False) == 2
    with pytest.raises(ValueError):
        mathx.variance([1])
    with pytest.raises(ValueError):
        mathx.mean([])


def test_units():
    assert mathx.convert(1, "mi", "km") == 1.609344
    assert mathx.convert(100, "C", "F") == 212
    assert mathx.convert(180, "deg", "rad") == pytest.approx(3.141592653589793)
    with pytest.raises(ValueError):
        mathx.convert(1, "m", "kg")
    with pytest.raises(ValueError):
        mathx.convert(-300, "C", "K")


def test_formula():
    assert mathx.formula("Trapezoid_Area") == "(a + b) * height / 2"
    assert "\\frac" in mathx.formula("trapezoid area", latex=True)
    with pytest.raises(ValueError, match="Did you mean"):
        mathx.formula("trapezoid aera")


def test_evaluate():
    assert mathx.evaluate("2 + 3 * 4") == 14
    assert mathx.evaluate("2^10") == 1024
    assert mathx.evaluate("sqrt(16) + sind(30)") == pytest.approx(4.5)
    for bad in ["__import__('os')", "1 +", "open('x')", "x + 1", "1/0", "9**9**9", "", "a.b"]:
        with pytest.raises(ValueError):
            mathx.evaluate(bad)
