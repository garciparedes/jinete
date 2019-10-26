from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .constants import (
    MAX_FLOAT,
)
from .abc import (
    Model,
)
from .services import (
    Service,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Any,
        Dict,
        Generator,
        Tuple,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Vehicle(Model):
    identifier: str
    origin: Service
    destination: Service
    capacity: float

    def __init__(self, identifier: str, origin: Service, destination: Service = None, capacity: float = 1.0,
                 timeout: float = MAX_FLOAT):
        self.identifier = identifier

        self.origin = origin
        self._destination = destination
        self.capacity = capacity
        self.timeout = timeout

    @property
    def origin_position(self) -> Position:
        return self.origin.position

    @property
    def origin_earliest(self) -> float:
        return self.origin.earliest

    @property
    def origin_latest(self) -> float:
        return self.origin.latest

    @property
    def origin_duration(self) -> float:
        return self.origin.duration

    @property
    def destination(self) -> Service:
        if self._destination is None:
            return self.origin
        return self._destination

    @property
    def destination_position(self) -> Position:
        return self.destination.position

    @property
    def destination_earliest(self) -> float:
        return self.destination.earliest

    @property
    def destination_latest(self) -> float:
        return self.destination.latest

    @property
    def destination_duration(self) -> float:
        return self.destination.duration

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('identifier', self.identifier),
            ('origin', tuple(self.origin)),
            ('destination', tuple(self.destination)),
            ('capacity', self.capacity),
            ('timeout', self.timeout),
        )

    def __deepcopy__(self, memo: Dict[int, Any]) -> Vehicle:
        return self


class Fleet(Model):
    vehicles: Set[Vehicle]

    def __init__(self, vehicles: Set[Vehicle]):
        self.vehicles = vehicles

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('vehicle_identifiers', tuple(vehicle.identifier for vehicle in self.vehicles)),
        )

    def __deepcopy__(self, memo: Dict[int, Any]) -> Fleet:
        return self
