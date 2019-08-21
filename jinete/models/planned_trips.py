from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from uuid import (
    uuid4,
)
from .abc import (
    Model,
)
from .trips import (
    Trip,
)
from .stops import (
    Stop,
    StopCause,
    StopKind,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
    )
    from uuid import (
        UUID,
    )
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


class PlannedTrip(Model):
    uuid: UUID
    route: Route
    trip: Trip
    initial: Position
    route_idx: int
    down_time: float

    def __init__(self, route: Route, trip: Trip, pickup_stop: Stop, delivery_stop: Stop, down_time: float = 0.0):
        self.uuid = uuid4()
        self.route = route
        self.trip = trip
        self.down_time = down_time

        assert pickup_stop == delivery_stop.previous

        pickup_stop.append_stop_cause(
            StopCause(self, StopKind.PICKUP)
        )
        delivery_stop.append_stop_cause(
            StopCause(self, StopKind.DELIVERY)
        )
        self.pickup_stop = pickup_stop
        self.delivery_stop = delivery_stop

        self._pickup_time = None
        self._delivery_time = None
        self._feasible = None

    @staticmethod
    def build_empty(route: Route, pickup_stop: Stop, delivery_stop: Stop, *args, **kwargs) -> 'PlannedTrip':
        trip = Trip.build_empty(
            *args, **kwargs,
        )
        return PlannedTrip(
            route=route,
            trip=trip,
            pickup_stop=pickup_stop,
            delivery_stop=delivery_stop,
        )

    @property
    def pickup_time(self) -> float:
        if self._pickup_time is None:
            self._pickup_time = self._calculate_pickup_time()
        return self._pickup_time

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
        return self.delivery_time - self.pickup_time

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

    def as_dict(self) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'route_uuid': self.route_uuid,
            'trip_uuid': self.trip_uuid,
            'pickup_stop': self.pickup_stop,
            'delivery_stop': self.delivery_stop,
            'down_time': self.down_time,
            'feasible': self.feasible,
        }

    def flush(self) -> None:
        self._pickup_time = None
        self._delivery_time = None
        self._feasible = None

    def _calculate_pickup_time(self) -> float:
        return self.pickup_stop.earliest

    def _calculate_delivery_time(self) -> float:
        return self.delivery_stop.earliest

    def _calculate_feasible(self) -> bool:
        if not self.pickup_stop.previous_time <= self.trip.latest:
            return False

        if self.trip.inbound:
            if not self.trip.earliest <= self.delivery_time <= self.trip.latest:
                return False
        else:
            if not self.trip.earliest <= self.pickup_time <= self.trip.latest:
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
