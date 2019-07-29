from __future__ import annotations

import logging
from sys import maxsize
from typing import (
    TYPE_CHECKING,
    Set,
    Any,
    Dict,
)
from uuid import (
    uuid4,
)

from .abc import (
    Model,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Vehicle(Model):
    initial: Position
    capacity: int
    earliest: float
    timeout: float
    uuid: UUID

    def __init__(self, initial: Position, final: Position = None, capacity: int = 1, earliest: float = 0.0,
                 timeout: float = None, uuid: UUID = None):

        if uuid is None:
            uuid = uuid4()

        self.initial = initial
        self._final = final
        self.capacity = capacity
        self.earliest = earliest
        self.timeout = timeout
        self.uuid = uuid

    @property
    def latest(self) -> float:
        if self.timeout is None:
            return maxsize
        return self.earliest + self.timeout

    @property
    def final(self) -> Position:
        if self._final is None:
            return self.initial
        return self._final

    def as_dict(self) -> Dict[str, Any]:
        return {
            'initial': self.initial,
            'final': self.final,
            'capacity': self.capacity,
            'earliest': self.earliest,
            'timeout': self.timeout,
            'latest': self.latest,
            'uuid': self.uuid,
        }


class Fleet(Model):
    vehicles: Set[Vehicle]

    def __init__(self, vehicles: Set[Vehicle]):
        self.vehicles = vehicles

    def __iter__(self):
        yield from self.vehicles

    def as_dict(self) -> Dict[str, Any]:
        vehicles_str = ', '.join(str(vehicle) for vehicle in self.vehicles)
        dict_values = {
            'vehicles': f'{{{vehicles_str}}}'
        }
        return dict_values
