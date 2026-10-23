"""Safe evaluation of maths expressions such as ``"2 + 3 * sqrt(16)"``.

The text is parsed with ``ast`` and only a whitelist of operators, functions
and constants is evaluated, so no arbitrary code can run.
"""

from __future__ import annotations

import ast
import math
import operator
from typing import Any, Callable, Dict

from . import arithmetic, number_theory, trig

MAX_LENGTH = 200
_MAX_EXPONENT = 10_000
_MAX_FACTORIAL = 1_000


def _pow(a: Any, b: Any) -> Any:
    if abs(b) > _MAX_EXPONENT:
        raise ValueError("exponent is too large")
    return arithmetic.power(a, b)


def _factorial(n: Any) -> int:
    if isinstance(n, int) and n > _MAX_FACTORIAL:
        raise ValueError(f"factorial is limited to {_MAX_FACTORIAL}")
    return number_theory.factorial(n)


_BINARY: Dict[type, Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: arithmetic.divide,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: _pow,
}
_UNARY: Dict[type, Callable[[Any], Any]] = {ast.UAdd: operator.pos, ast.USub: operator.neg}

_FUNCTIONS: Dict[str, Callable[..., Any]] = {
    "sqrt": arithmetic.sqrt,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
    "ln": arithmetic.ln,
    "log": arithmetic.log,
    "log2": arithmetic.log2,
    "log10": arithmetic.log10,
    "factorial": _factorial,
    "sin": trig.sin,
    "cos": trig.cos,
    "tan": trig.tan,
    "asin": trig.asin,
    "acos": trig.acos,
    "atan": trig.atan,
    "sinh": trig.sinh,
    "cosh": trig.cosh,
    "tanh": trig.tanh,
    "sind": lambda x: trig.sin(x, degrees=True),
    "cosd": lambda x: trig.cos(x, degrees=True),
    "tand": lambda x: trig.tan(x, degrees=True),
}
_CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau}


def _eval(node: ast.AST) -> Any:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError("only numbers are allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
        return _BINARY[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"unknown name {node.id!r}")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTIONS or node.keywords:
            raise ValueError("unsupported function call")
        return _FUNCTIONS[node.func.id](*[_eval(arg) for arg in node.args])
    raise ValueError("unsupported expression")


def evaluate(expression: str) -> Any:
    """Evaluate a maths expression and return an int, float (or complex).

    Supports + - * / // % ** (and ^ for powers), parentheses, the constants
    pi, e, tau, and the functions sqrt, abs, floor, ceil, round, ln, log,
    log2, log10, factorial, sin, cos, tan, asin, acos, atan, sinh, cosh,
    tanh (radians) and sind, cosd, tand (degrees).
    """
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    text = expression.strip().replace("^", "**")
    if not text:
        raise ValueError("expression is empty")
    if len(text) > MAX_LENGTH:
        raise ValueError(f"expression is longer than {MAX_LENGTH} characters")
    try:
        tree = ast.parse(text, mode="eval")
        return _eval(tree)
    except SyntaxError:
        raise ValueError("invalid expression") from None
    except ZeroDivisionError:
        raise ValueError("cannot divide by zero") from None
    except OverflowError:
        raise ValueError("result is too large") from None
    except RecursionError:
        raise ValueError("expression is too deeply nested") from None
    except TypeError as exc:
        raise ValueError(f"invalid arguments: {exc}") from None
