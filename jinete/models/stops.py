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
        Iterable,
        Tuple,
        List,
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
        'following',
        '_previous_departure_time',
        '_down_time',
        '_load_time',
        '_earliest',
        '_arrival_time',
    ]
    route: Route
    position: Position
    previous: Optional[Stop]
    following: Optional[Stop]
    pickups: Tuple[PlannedTrip, ...]
    deliveries: Tuple[PlannedTrip, ...]

    _down_time: Optional[float]
    _load_time: Optional[float]
    _earliest: Optional[float]
    _arrival_time: Optional[float]
    _previous_departure_time: Optional[float]

    def __init__(self, route: Route, position: Position, previous: Optional[Stop], following: Optional[Stop] = None,
                 pickups: Tuple[PlannedTrip, ...] = tuple(), deliveries: Tuple[PlannedTrip, ...] = tuple()):

        self.route = route
        self.position = position

        self.pickups = pickups
        self.deliveries = deliveries

        self.previous = previous
        self.following = following

        self._previous_departure_time = None
        self._down_time = None
        self._load_time = None
        self._earliest = None
        self._arrival_time = None

    def append_pickup(self, planned_trip: PlannedTrip) -> None:
        self.extend_pickups((planned_trip,))

    def append_delivery(self, planned_trip: PlannedTrip) -> None:
        self.extend_deliveries((planned_trip,))

    def extend_pickups(self, iterable: Iterable[PlannedTrip]) -> None:
        self.pickups = (*self.pickups, *iterable)

    def extend_deliveries(self, iterable: Iterable[PlannedTrip]) -> None:
        self.deliveries = (*self.deliveries, *iterable)

    @property
    def down_time(self) -> float:
        if self._down_time is None:
            if not any(self.pickups):
                self._down_time = 0.0
            else:
                self._down_time = max((pt.down_time for pt in self.pickups))
        return self._down_time

    @property
    def earliest(self):
        if self._earliest is None:
            if not any(self.pickups):
                self._earliest = 0.0
            else:
                self._earliest = max((pt.trip.earliest for pt in self.pickups))
        return self._earliest

    @property
    def load_time(self) -> float:
        if self._load_time is None:
            if not any(self.pickups):
                self._load_time = 0.0
            else:
                self._load_time = max((pt.trip.load_time for pt in self.pickups))
        return self._load_time

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

    @property
    def vehicle_uuid(self) -> UUID:
        return self.vehicle.uuid

    @property
    def stops(self) -> List[Stop]:
        return self.route.stops

    @property
    def index(self) -> int:
        return self.stops.index(self)

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
    def distance(self) -> float:
        return self.position.distance_to(self.previous_position)

    @property
    def navigation_time(self):
        return self.previous_position.time_to(self.position, self.previous_departure_time)

    @property
    def waiting_time(self):
        return max(self.earliest - self.arrival_time, 0.0)

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

    def flush(self) -> None:
        self._down_time = None
        self._load_time = None
        self._earliest = None
        self._arrival_time = None

    def flush_all_previous(self):
        self.flush()
        if self.previous is not None:
            self.previous.flush_all_previous()

    def flush_all_following(self):
        self.flush()
        if self.following is not None:
            self.following.flush_all_following()

    def merge(self, other: Stop) -> None:
        if self == other:
            return
        assert self.route == other.route
        assert self.position == other.position
        assert self.following == other.following

        self.extend_pickups(other.pickups)
        for planned_trip in other.pickups:
            planned_trip.pickup = self

        self.extend_deliveries(other.deliveries)
        for planned_trip in other.deliveries:
            planned_trip.delivery = self

        self.flush()

    def flip(self, other: Stop) -> None:
        # assert other.previous == self
        assert self.route == other.route

        self_index = self.index
        other_index = other.index
        self.stops[self_index], self.stops[other_index] = self.stops[other_index], self.stops[self_index]

        following = other.following
        other.following = self
        if following is not None:
            following.previous = self
        self.following = following

        previous = self.previous
        other.previous = previous
        if previous is not None:
            previous.following = other
        self.previous = other

        other.flush_all_following()

    def flip_with_following(self):
        self.flip(self.following)
