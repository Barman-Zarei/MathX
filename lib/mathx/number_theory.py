"""Integer functions: gcd, lcm, primes, factorials and counting."""

from __future__ import annotations

import math
from functools import reduce
from typing import List, Optional

from . import _validate as v

_WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def _ints(numbers, name: str = "numbers") -> List[int]:
    items = [v.integer(n, f"{name}[{i}]") for i, n in enumerate(numbers)]
    if not items:
        raise ValueError(f"{name} needs at least one number")
    return items


def gcd(*numbers: int) -> int:
    """Greatest common divisor of one or more integers."""
    return reduce(math.gcd, _ints(numbers))


def lcm(*numbers: int) -> int:
    """Least common multiple of one or more integers."""
    return reduce(lambda a, b: abs(a * b) // math.gcd(a, b) if a and b else 0, _ints(numbers))


def is_prime(n: int) -> bool:
    """Primality test (Miller-Rabin; exact for n below about 3.3e24)."""
    n = v.integer(n, "n")
    if n < 2:
        return False
    for p in _WITNESSES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _WITNESSES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> List[int]:
    """Prime factors of n >= 2 in ascending order, repeated by multiplicity."""
    n = v.integer(n, "n", minimum=2)
    factors: List[int] = []
    for p in (2, 3):
        while n % p == 0:
            factors.append(p)
            n //= p
    f = 5
    while f * f <= n:
        for step in (0, 2):
            p = f + step
            while n % p == 0:
                factors.append(p)
                n //= p
        f += 6
    if n > 1:
        factors.append(n)
    return factors


def factorial(n: int) -> int:
    return math.factorial(v.integer(n, "n", minimum=0))


def _fib_pair(n: int):
    if n == 0:
        return 0, 1
    a, b = _fib_pair(n >> 1)
    c = a * (2 * b - a)
    d = a * a + b * b
    return (d, c + d) if n & 1 else (c, d)


def fibonacci(n: int) -> int:
    """The n-th Fibonacci number (fibonacci(0) == 0, fibonacci(1) == 1)."""
    return _fib_pair(v.integer(n, "n", minimum=0))[0]


def combinations(n: int, k: int) -> int:
    """Number of ways to choose k items from n (order ignored)."""
    return math.comb(v.integer(n, "n", minimum=0), v.integer(k, "k", minimum=0))


def permutations(n: int, k: Optional[int] = None) -> int:
    """Number of ordered selections of k items from n (all n by default)."""
    n = v.integer(n, "n", minimum=0)
    k = n if k is None else v.integer(k, "k", minimum=0)
    return math.perm(n, k)
