import math
from fractions import Fraction

import pytest

import mathx


def test_trapezoid_area_uses_both_bases_and_height():
    assert mathx.trapezoid_area(4, 6, 3) == 15
    assert mathx.trapezoid_perimeter(4, 6, 3, 3) == 16


def test_triangle_general_perimeter_and_heron():
    assert mathx.triangle_perimeter(3, 4, 5) == 12
    assert mathx.triangle_area_from_sides(3, 4, 5) == pytest.approx(6)
    with pytest.raises(ValueError):
        mathx.triangle_perimeter(1, 2, 10)


def test_circle():
    assert mathx.circle_area(2) == pytest.approx(4 * math.pi)
    assert mathx.circle_circumference(1) == pytest.approx(2 * math.pi)
    assert mathx.sector_area(2, 90, degrees=True) == pytest.approx(math.pi)


def test_fraction_stays_exact():
    assert mathx.rectangle_area(Fraction(1, 2), Fraction(1, 3)) == Fraction(1, 6)


def test_solids():
    assert mathx.cube_volume(3) == 27
    assert mathx.sphere_volume(1) == pytest.approx(4 / 3 * math.pi)
    assert mathx.cone_volume(3, 4) == pytest.approx(12 * math.pi)


@pytest.mark.parametrize("bad", [0, -1])
def test_dimensions_must_be_positive(bad):
    with pytest.raises(ValueError):
        mathx.square_area(bad)


def test_wrong_types():
    with pytest.raises(TypeError):
        mathx.square_area("3")
    with pytest.raises(TypeError):
        mathx.square_area(True)


def test_coordinates():
    assert mathx.distance((0, 0), (3, 4)) == 5
    assert mathx.midpoint((0, 0), (4, 2)) == (2, 1)
    assert mathx.slope((0, 0), (2, 4)) == 2
    assert mathx.polygon_area([(0, 0), (4, 0), (4, 3), (0, 3)]) == 12
    with pytest.raises(ValueError):
        mathx.slope((1, 0), (1, 5))
