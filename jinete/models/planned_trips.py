from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from .trips import (
    Trip,
)

if TYPE_CHECKING:
    from .routes import (
        Route,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


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
    def capacity(self):
        return self.trip.capacity

    @property
    def feasible(self) -> bool:
        return self.trip.earliest <= self.collection_time and self.delivery_time <= self.trip.latest

    @property
    def empty(self) -> bool:
        return self.trip.empty
