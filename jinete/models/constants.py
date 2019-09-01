from __future__ import annotations

import heapq
import logging
from math import sqrt
from sys import maxsize
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

MAX_INT = maxsize
MIN_INT = -maxsize

MAX_FLOAT = float('inf')
MIN_FLOAT = float('-inf')


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

    def nbest(self, n: int, iterable: Iterable[T], key: Callable[[T], float], inplace: bool = False) -> List[T]:
        if self._reverse:
            return heapq.nlargest(n, iterable, key=key)
        else:
            return heapq.nsmallest(n, iterable, key=key)


@unique
class DistanceMetric(Enum):

    @staticmethod
    def _euclidean_distance(a: Iterable[Number], b: Iterable[Number]) -> float:
        return sqrt(sum(pow(a_i - b_i, 2) for a_i, b_i in zip(a, b)))

    @staticmethod
    def _manhattan_distance(a: Iterable[Number], b: Iterable[Number]) -> float:
        return sum(abs(a_i - b_i) for a_i, b_i in zip(a, b))

    EUCLIDEAN = _euclidean_distance
    MANHATTAN = _manhattan_distance

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def __str__(self):
        return f'{self.name.capitalize()}'
