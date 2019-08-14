from __future__ import annotations

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
    )

    T = TypeVar('T')


@unique
class OptimizationDirection(Enum):
    MAXIMIZATION = max
    MINIMIZATION = min

    @property
    def fn(self) -> Callable[[Iterable[T]], T]:
        return self.value

    def __str__(self):
        return f'{self.name.capitalize()}'
