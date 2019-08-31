from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from .abc import (
    Model,
)
from .trips import (
    Trip,
)
from .stops import (
    Stop,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
        Optional,
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
    __slots__ = [
        'route',
        'trip',
        'down_time',
        'pickup',
        'delivery',
        '_feasible',
    ]

    route: Route
    trip: Trip
    down_time: float

    _feasible: Optional[bool]

    def __init__(self, route: Route, trip: Trip, pickup: Stop, delivery: Stop, down_time: float = 0.0):
        self.route = route
        self.trip = trip
        self.down_time = down_time

        self.pickup = pickup
        pickup.append_pickup(self)

        self.delivery = delivery
        delivery.append_delivery(self)

        self._feasible = None

    @property
    def pickup_time(self) -> float:
        return self.pickup.arrival_time

    @property
    def delivery_time(self) -> float:
        return self.delivery.arrival_time

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

    @property
    def trip_identifier(self) -> str:
        return self.trip.identifier

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
            'route_uuid': self.route_uuid,
            'trip_identifier': self.trip_identifier,
            'pickup': self.pickup,
            'delivery': self.delivery,
            'down_time': self.down_time,
            'feasible': self.feasible,
        }

    def flush(self) -> None:
        self._feasible = None

    def _calculate_feasible(self) -> bool:
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

        if self.vehicle.route_timeout is not None:
            if not self.duration <= self.vehicle.route_timeout:
                return False

        if self.vehicle.trip_timeout is not None:
            if not self.duration <= self.vehicle.trip_timeout:
                return False

        return True
