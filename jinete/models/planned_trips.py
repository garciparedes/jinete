from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)

from cached_property import (
    cached_property,
)

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
        Generator,
        Tuple,
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
        'vehicle',
        'trip',
        'down_time',
        'pickup',
        'delivery',
    ]

    vehicle: Vehicle
    trip: Trip
    down_time: float
    pickup: Stop
    delivery: Stop

    def __init__(self, vehicle: Vehicle, trip: Trip, pickup: Stop = None, delivery: Stop = None,
                 down_time: float = 0.0):
        self.vehicle = vehicle
        self.trip = trip
        self.down_time = down_time

        self.pickup = pickup
        self.delivery = delivery

        if self.pickup is not None:
            self.pickup.append_pickup(self)
        if self.delivery is not None:
            self.delivery.append_delivery(self)

    @property
    def pickup_time(self) -> float:
        return self.pickup.arrival_time

    @property
    def delivery_time(self) -> float:
        return self.delivery.arrival_time

    @property
    def trip_identifier(self) -> str:
        return self.trip.identifier

    @property
    def vehicle_identifier(self) -> str:
        return self.vehicle.identifier

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
        assert self.pickup in self.delivery.all_previous
        assert self.pickup_time <= self.delivery_time

        if not self.pickup_time <= self.trip.origin_latest:
            return False

        if not self.delivery_time <= self.trip.destination_latest:
            return False

        if not self.pickup.capacity <= self.vehicle.capacity:
            return False

        if not self.duration <= self.trip.timeout:
            return False

        return True

    @property
    def empty(self) -> bool:
        return self.trip.empty

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('trip_identifier', self.trip_identifier),
            ('pickup', self.pickup),
            ('delivery', self.delivery),
            ('down_time', self.down_time),
            ('feasible', self.feasible),
        )

    def flush(self) -> None:
        for key in ('feasible',):
            self.__dict__.pop(key, None)
