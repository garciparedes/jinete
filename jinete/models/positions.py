from __future__ import annotations

import logging
from abc import ABC
from typing import (
    TYPE_CHECKING,
)

from uuid import (
    uuid4,
)

if TYPE_CHECKING:
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


class XYPosition(Position):
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lat = lat
        self.lon = lon
