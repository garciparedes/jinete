from __future__ import annotations

import logging
from dataclasses import dataclass, field
from sys import maxsize
from typing import (
    TYPE_CHECKING,
    Optional,
)

from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Trip(object):
    origin: Position
    destination: Position

    earliest: float = field(default=0.0)
    timeout: Optional[float] = field(default=None)

    load_time: float = field(default=0.0)

    capacity: int = field(default=1)
    uuid: UUID = field(default_factory=uuid4)

    @staticmethod
    def empty(origin: Position, destination: Position) -> 'Trip':
        return Trip(origin, destination, capacity=0)

    @property
    def latest(self) -> float:
        if self.timeout is None:
            return maxsize
        return self.earliest + self.timeout


@dataclass(frozen=True)
class PlannedTrip(object):
    trip: Trip
    collection_time: float
    delivery_time: float

    @staticmethod
    def empty(collection_time, delivery_time, *args, **kwargs) -> 'PlannedTrip':
        trip = Trip.empty(*args, **kwargs)
        return PlannedTrip(trip, collection_time, delivery_time)

    @property
    def origin(self) -> Position:
        return self.trip.origin

    @property
    def destination(self) -> Position:
        return self.trip.destination

    @property
    def duration(self) -> float:
        return self.delivery_time - self.collection_time

    @property
    def capacity(self):
        return self.trip.capacity

    @property
    def feasible(self) -> bool:
        return self.trip.earliest <= self.collection_time and self.delivery_time <= self.trip.latest
