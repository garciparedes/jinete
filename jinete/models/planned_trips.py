from __future__ import annotations

import logging
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
    from .vehicles import (
        Vehicle,
    )

logger = logging.getLogger(__name__)


class PlannedTrip(object):
    route: Route
    trip: Trip
    initial: Position
    route_idx: int
    down_time: float

    def __init__(self, route: Route, trip: Trip, initial: Position, route_idx: int, down_time: float = 0.0):
        self.route = route
        self.trip = trip
        self.initial = initial
        self.route_idx = route_idx
        self.down_time = down_time

        self._collection_time = None
        self._delivery_time = None
        self._feasible = None

    @staticmethod
    def build_empty(route: Route, route_idx: int,
                    *args, **kwargs) -> 'PlannedTrip':
        trip = Trip.build_empty(*args, **kwargs)
        return PlannedTrip(
            route=route,
            trip=trip,
            initial=route.last_position,
            route_idx=route_idx,
        )

    @property
    def collection_time(self) -> float:
        if self._collection_time is None:
            self._collection_time = self._calculate_collection_time()
        return self._collection_time

    @property
    def delivery_time(self) -> float:
        if self._delivery_time is None:
            self._delivery_time = self._calculate_delivery_time()
        return self._delivery_time

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

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
        if self._feasible is None:
            self._feasible = self._calculate_feasible()
        return self._feasible

    @property
    def empty(self) -> bool:
        return self.trip.empty

    def flush(self) -> None:
        self._collection_time = None
        self._delivery_time = None
        self._feasible = None

    def _calculate_collection_time(self) -> float:
        time_to_origin = self.route.position_at(self.route_idx - 1).distance_to(self.trip.origin)
        trip_start_time = max(self.route.time_at(self.route_idx - 1) + time_to_origin, self.trip.earliest)
        trip_start_time += self.down_time
        return trip_start_time

    def _calculate_delivery_time(self) -> float:
        time_to_travel = self.trip.duration(self.collection_time)
        trip_finish_time = self.collection_time + time_to_travel + self.trip.load_time
        return trip_finish_time

    def _calculate_feasible(self) -> bool:
        if not self.route.time_at(self.route_idx - 1) <= self.trip.latest:
            return False

        if self.trip.inbound:
            if not self.trip.earliest <= self.delivery_time <= self.trip.latest:
                return False
        else:
            if not self.trip.earliest <= self.collection_time <= self.trip.latest:
                return False

        time_to_return = self.trip.destination.time_to(self.vehicle.final, self.delivery_time)
        vehicle_finish_time = self.delivery_time + time_to_return
        if not vehicle_finish_time <= self.vehicle.latest:
            return False

        if self.vehicle.vehicle_timeout is not None:
            if not self.duration <= self.vehicle.vehicle_timeout:
                return False

        if self.vehicle.trip_timeout is not None:
            if not self.duration <= self.vehicle.trip_timeout:
                return False

        return True
