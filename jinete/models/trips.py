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


class Trip(object):
    identifier: str
    origin: Position
    destination: Position
    earliest: float
    timeout: Optional[float]
    on_time_bonus: float
    load_time: float
    capacity: float
    uuid: UUID

    def __init__(self, identifier: str, origin: Position, destination: Position, earliest: float = 0.0,
                 timeout: Optional[float] = None, on_time_bonus: float = 0.0, load_time: float = 0.0,
                 capacity: float = 1, uuid: UUID = None):
        if uuid is None:
            uuid = uuid4()
        self.identifier = identifier
        self.origin = origin
        self.destination = destination
        self.earliest = earliest
        self.timeout = timeout
        self.on_time_bonus = on_time_bonus
        self.load_time = load_time
        self.capacity = capacity
        self.uuid = uuid

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
    def distance(self) -> float:
        return self.trip.distance

    @property
    def duration(self) -> float:
        return self.delivery_time - self.collection_time

    @property
    def cost(self) -> float:
        return self.duration

    @property
    def capacity(self):
        return self.trip.capacity

    @property
    def feasible(self) -> bool:
        return self.trip.earliest <= self.collection_time and self.delivery_time <= self.trip.latest

    @property
    def empty(self) -> bool:
        return self.trip.empty
