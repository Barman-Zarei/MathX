"""Descriptive statistics."""

from __future__ import annotations

import statistics as _st
from typing import Iterable, List

from . import _validate as v
from ._validate import Number


def _data(data: Iterable[Number]) -> List[Number]:
    return v.number_list(data, "data")


def mean(data: Iterable[Number]) -> Number:
    return _st.mean(_data(data))


def median(data: Iterable[Number]) -> Number:
    return _st.median(_data(data))


def mode(data: Iterable[Number]) -> List[Number]:
    """All most-common values (a list, because there can be several)."""
    return _st.multimode(_data(data))


def variance(data: Iterable[Number], sample: bool = True) -> Number:
    """Sample variance by default; sample=False gives the population variance."""
    items = _data(data)
    try:
        return _st.variance(items) if sample else _st.pvariance(items)
    except _st.StatisticsError as exc:
        raise ValueError(str(exc)) from None


def std_dev(data: Iterable[Number], sample: bool = True) -> Number:
    """Sample standard deviation by default; sample=False for the population one."""
    items = _data(data)
    try:
        return _st.stdev(items) if sample else _st.pstdev(items)
    except _st.StatisticsError as exc:
        raise ValueError(str(exc)) from None
