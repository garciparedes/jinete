from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)
from .abc import (
    Model,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
    from typing import (
        Dict,
        Any,
        Optional,
    )
    from .positions import (
        Position,
    )
    from .planned_trips import (
        PlannedTrip
    )
    from .routes import (
        Route,
    )
    from .vehicles import (
        Vehicle,
    )

logger = logging.getLogger(__name__)


class Stop(Model):
    __slots__ = [
        'route',
        'position',
        'pickups',
        'deliveries',
        'previous',
        '_previous_departure_time',
        '_down_time',
        '_load_time',
        '_earliest',
        '_arrival_time',
    ]
    route: Route
    position: Position

    def __init__(self, route: Route, position: Position, previous: Optional[Stop]):

        self.route = route
        self.position = position

        self.pickups = set()
        self.deliveries = set()

        self.previous = previous

        self._previous_departure_time = None

        self._down_time = None
        self._load_time = None
        self._earliest = None
        self._arrival_time = None

    def append_pickup(self, planned_trip: PlannedTrip) -> None:
        self.pickups.add(planned_trip)

    def append_delivery(self, planned_trip: PlannedTrip) -> None:
        self.deliveries.add(planned_trip)

    @property
    def down_time(self) -> float:
        if self._down_time is None:
            self._down_time = max((pt.down_time for pt in self.pickups), default=0.0)
        return self._down_time

    @property
    def earliest(self):
        if self._earliest is None:
            self._earliest = max((pt.trip.earliest for pt in self.pickups), default=0.0)
        return self._earliest

    @property
    def load_time(self) -> float:
        if self._load_time is None:
            self._load_time = max((pt.trip.load_time for pt in self.pickups), default=0.0)
        return self._load_time

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

    @property
    def vehicle_uuid(self) -> UUID:
        return self.vehicle.uuid

    @property
    def previous_departure_time(self) -> float:
        if self.previous is None:
            return self.vehicle.earliest
        if self._previous_departure_time is None:
            self._previous_departure_time = self.previous.departure_time
        return self._previous_departure_time

    @property
    def previous_position(self) -> Position:
        if self.previous is None:
            return self.vehicle.initial
        return self.previous.position

    @property
    def navigation_time(self):
        return self.previous_position.time_to(self.position, self.previous_departure_time)

    @property
    def waiting_time(self):
        return self.arrival_time - self.earliest

    @property
    def arrival_time(self):
        if self._arrival_time is None:
            arrival_time = self.previous_departure_time + self.down_time + self.navigation_time
            self._arrival_time = max(arrival_time, self.earliest)
        return self._arrival_time

    @property
    def departure_time(self) -> float:
        return self.arrival_time + self.load_time

    def as_dict(self) -> Dict[str, Any]:
        return {
            'vehicle_uuid': self.vehicle_uuid,
            'position': self.position,
        }
