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
    from .routes import (
        Route,
    )

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Trip(object):
    identifier: str
    origin: Position
    destination: Position

    earliest: float = field(default=0.0)
    timeout: Optional[float] = field(default=None)

    load_time: float = field(default=0.0)

    capacity: int = field(default=1)
    uuid: UUID = field(default_factory=uuid4)

    @staticmethod
    def build_empty(origin: Position, destination: Position) -> 'Trip':
        return Trip('EMPTY', origin, destination, capacity=0)

    @property
    def latest(self) -> float:
        if self.timeout is None:
            return maxsize
        return self.earliest + self.timeout

    @property
    def empty(self) -> bool:
        return self.capacity == 0

    @property
    def distance(self) -> float:
        return self.origin.distance_to(self.destination)

    def duration(self, now: float):
        return self.origin.time_to(self.destination, now)

    def __lt__(self, other):
        return self.latest < other.latest

@dataclass(frozen=True)
class PlannedTrip(object):
    route: Route
    trip: Trip
    collection_time: float
    delivery_time: float

    @staticmethod
    def build_empty(route, collection_time, delivery_time, *args, **kwargs) -> 'PlannedTrip':
        trip = Trip.build_empty(*args, **kwargs)
        return PlannedTrip(route, trip, collection_time, delivery_time)

    @property
    def trip_uuid(self) -> UUID:
        return self.trip.uuid

    @property
    def route_uuid(self) -> UUID:
        return self.route.uuid

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
    def cost(self) -> float:
        return self.duration

    @property
    def capacity(self):
        return self.trip.capacity

    def __lt__(self, other):
        return self.scoring < other.scoring

    @property
    def scoring(self):
        return self.collection_time - self.route.last_time

    @property
    def feasible(self) -> bool:
        return self.trip.earliest <= self.collection_time and self.delivery_time <= self.trip.latest

    @property
    def empty(self) -> bool:
        return self.trip.empty
