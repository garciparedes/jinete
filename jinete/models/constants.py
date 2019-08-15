from __future__ import annotations

import logging
from math import sqrt
import functools as ft
from typing import TYPE_CHECKING
from enum import (
    Enum,
    unique,
)

if TYPE_CHECKING:
    from typing import (
        Callable,
        Iterable,
        TypeVar,
        List,
        Union,
    )

    T = TypeVar('T')
    Number = Union[int, float]

logger = logging.getLogger(__name__)


@unique
class OptimizationDirection(Enum):
    MAXIMIZATION = max
    MINIMIZATION = min

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def __str__(self):
        return f'{self.name.capitalize()}'

    @property
    def _reverse(self):
        return self.value == max

    def sorted(self, iterable: Iterable[T], key: Callable[[T], float], inplace: bool = False) -> List[T]:
        if isinstance(iterable, list) and inplace:
            iterable.sort(key=key, reverse=self._reverse)
        else:
            if inplace:
                logger.warning('"inplace" sorting is possible only over list objects.')
            iterable = sorted(iterable, key=key, reverse=self._reverse)
        return iterable


@unique
class DistanceMetric(Enum):
    def _euclidean_distance(a: Iterable[Number], b: Iterable[Number]) -> float:
        return sqrt(sum(pow(a_i - b_i, 2) for a_i, b_i in zip(a, b)))

    def _manhattan_distance(a: Iterable[Number], b: Iterable[Number]) -> float:
        return sum(abs(a_i - b_i) for a_i, b_i in zip(a, b))

    EUCLIDEAN = _euclidean_distance
    MANHATTAN = _manhattan_distance

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def __str__(self):
        return f'{self.name.capitalize()}'
