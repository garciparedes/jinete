from __future__ import annotations

import logging
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)
from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from typing import (
        List,
        Sequence,
    )
    from uuid import (
        UUID,
    )
    from .surfaces import (
        Surface,
    )

logger = logging.getLogger(__name__)


class Position(ABC):
    uuid: UUID

    def __init__(self, surface: Surface = None, uuid: UUID = None):
        if uuid is None:
            uuid = uuid4()
        self.surface = surface
        self.uuid = uuid

    def distance_to(self, other: Position) -> float:
        return self.surface.distance(self, other)

    def time_to(self, other: Position, now: float) -> float:
        return self.surface.time(self, other, now)

    @abstractmethod
    def is_equal(self, other: Position) -> bool:
        pass


class GeometricPosition(Position):
    coordinates: List[float]

    def __init__(self, coordinates: Sequence[float], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coordinates = list(coordinates)

    def __str__(self):
        c = ",".join(f"{x:07.3f}" for x in self)
        return f'({c})'

    def __getitem__(self, item):
        return self.coordinates[item]

    def is_equal(self, other: GeometricPosition) -> bool:
        return self.coordinates == other.coordinates
