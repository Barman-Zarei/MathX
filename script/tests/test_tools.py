import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import tools  # noqa: E402


def find(category, title):
    return next(t for t in tools.CATEGORIES[category] if t.title == title)


def run(category, title, **raw):
    return tools.run_tool(find(category, title), raw)


def test_expression_and_trapezoid():
    assert run("Calculator", "Expression", expression="2 + 3 * 4") == ("14", "")
    assert run("Shapes", "Trapezoid area", a="10", b="6", height="4")[0] == "32"


def test_degrees_toggle_and_expression_inputs():
    assert run("Trig", "sin", x="30", degrees=True)[0] == "0.5"
    assert run("Trig", "sin", x="pi/2", degrees=False)[0] == "1"


def test_optional_fields_use_defaults():
    assert run("Arithmetic", "Log", x="1000", base="10")[0] == "3"
    assert run("Arithmetic", "Log", x="e", base="")[0] == "1"
    assert run("Numbers", "Permutations", n="5", k="")[0] == "120"


def test_roots_and_system_formatting():
    assert run("Algebra", "Quadratic", a="1", b="-3", c="2")[0] == "x1 = 1\nx2 = 2"
    assert run("Algebra", "Quadratic", a="1", b="0", c="1")[0] == "x1 = -1i\nx2 = 1i"
    assert run("Algebra", "Linear system", matrix="2, 1; 1, 3", constants="5, 10")[0] == "x = 1\ny = 3"
    assert run("Algebra", "Simplify fraction", numerator="6", denominator="8") == ("3/4", "decimal: 0.75")


def test_lists_points_and_text():
    assert run("Stats", "Mean", data="1 2 3 4")[0] == "2.5"
    assert run("Stats", "Mode", data="1,2,2,3")[0] == "2"
    assert run("Coordinates", "Polygon area", points="0,0; 4,0; 4,3; 0,3")[0] == "12"
    assert run("Units", "Convert", value="100", from_unit="C", to_unit="F")[0] == "212"


def test_big_numbers_are_shortened():
    main, detail = run("Numbers", "Factorial", n="100")
    assert "e+" in main and detail == "158 digits"


def test_errors_are_readable():
    with pytest.raises(ValueError, match="Radius"):
        run("Circle", "Area", radius="")
    with pytest.raises(ValueError, match="whole number"):
        run("Numbers", "Is prime", n="2.5")
    with pytest.raises(ValueError, match="at most|up to"):
        run("Numbers", "Factorial", n="999999")
    with pytest.raises(ValueError):
        run("Arithmetic", "Divide", a="1", b="0")


def test_every_tool_has_valid_field_names():
    import inspect

    for tools_list in tools.CATEGORIES.values():
        for t in tools_list:
            params = inspect.signature(t.func).parameters
            for f in t.fields:
                assert f.key in params, (t.title, f.key)
