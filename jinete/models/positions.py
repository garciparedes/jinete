from __future__ import annotations

import logging
from abc import (
    ABC,
)
from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from typing import (
        Tuple,
        Sequence,
        Dict,
        Any,
    )
    from .surfaces import (
        Surface,
    )

logger = logging.getLogger(__name__)


class Position(ABC):
    def __init__(self, surface: Surface):
        self.surface = surface

    def __eq__(self, other):
        return hash(self) == hash(other)

    def distance_to(self, other: Position) -> float:
        return self.surface.distance(self, other)

    def time_to(self, other: Position, now: float) -> float:
        return self.surface.time(self, other, now)

    def __deepcopy__(self, memo: Dict[int, Any]) -> Position:
        return self


class GeometricPosition(Position):
    __slots__ = (
        'coordinates',
    )

    coordinates: Tuple[float, ...]

    def __init__(self, coordinates: Sequence[float], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coordinates = tuple(coordinates)

    def __hash__(self):
        return hash(self.coordinates)

    def __eq__(self, other) -> bool:
        return self.coordinates == other.coordinates

    def __ne__(self, other) -> bool:
        return self.coordinates != other.coordinates

    def __str__(self):
        c = ",".join(f"{x:07.3f}" for x in self)
        return f'({c})'

    def __getitem__(self, item):
        return self.coordinates[item]
