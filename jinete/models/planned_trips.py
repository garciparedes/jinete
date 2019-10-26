from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cached_property import cached_property

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
        Any,
        Optional,
        Generator,
        Tuple,
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
    def route_duration(self) -> float:
        return self.delivery_time - self.route.first_stop.arrival_time

    @property
    def origin(self) -> Position:
        return self.trip.origin_position

    @property
    def destination(self) -> Position:
        return self.trip.destination_position

    @property
    def distance(self) -> float:
        return self.trip.distance

    @property
    def duration(self) -> float:
        return self.delivery_time - self.pickup_time

    @property
    def capacity(self):
        return self.trip.capacity

    @cached_property
    def feasible(self) -> bool:
        if not self.trip.origin_earliest <= self.pickup_time <= self.trip.origin_latest:
            return False
        if not self.trip.destination_earliest <= self.delivery_time <= self.trip.destination_latest:
            return False

        time_to_return = self.trip.destination_position.time_to(self.vehicle.destination_position, self.delivery_time)
        vehicle_finish_time = self.delivery_time + time_to_return

        if not vehicle_finish_time <= self.vehicle.origin_latest:
            return False

        if not self.route_duration <= self.vehicle.timeout:
            return False

        if not self.duration <= self.trip.timeout:
            return False

        return True

    @property
    def empty(self) -> bool:
        return self.trip.empty

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('route_uuid', self.route_uuid),
            ('trip_identifier', self.trip_identifier),
            ('pickup', self.pickup),
            ('delivery', self.delivery),
            ('down_time', self.down_time),
            ('feasible', self.feasible),
        )

    def flush(self) -> None:
        self._feasible = None
