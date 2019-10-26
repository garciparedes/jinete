from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)

from cached_property import cached_property

from .abc import (
    Model,
)

if TYPE_CHECKING:
    from typing import (
        Generator,
        Tuple,
        Any,
        Optional,
        Iterable,
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
    ]
    route: Route
    position: Position
    previous: Optional[Stop]
    following: Optional[Stop]
    pickups: Tuple[PlannedTrip, ...]
    deliveries: Tuple[PlannedTrip, ...]

    def __init__(self, route: Route, position: Position, previous: Optional[Stop], following: Optional[Stop] = None,
                 pickups: Tuple[PlannedTrip, ...] = tuple(), deliveries: Tuple[PlannedTrip, ...] = tuple()):

        self.route = route
        self.position = position

        self.pickups = pickups
        self.deliveries = deliveries

        self.previous = previous
        self.following = following

    @property
    def planned_trips(self) -> Iterable[PlannedTrip]:
        yield from self.pickups
        yield from self.deliveries

    def append_pickup(self, planned_trip: PlannedTrip) -> None:
        assert planned_trip.origin == self.position
        self.extend_pickups((planned_trip,))

    def append_delivery(self, planned_trip: PlannedTrip) -> None:
        assert planned_trip.destination == self.position
        self.extend_deliveries((planned_trip,))

    def extend_pickups(self, iterable: Iterable[PlannedTrip]) -> None:
        self.pickups = (*self.pickups, *iterable)

    def extend_deliveries(self, iterable: Iterable[PlannedTrip]) -> None:
        self.deliveries = (*self.deliveries, *iterable)

    @property
    def down_time(self) -> float:
        return max((pt.down_time for pt in self.pickups), default=0.0)

    @property
    def earliest(self):
        return max((pt.trip.origin_earliest for pt in self.pickups), default=0.0)

    @property
    def load_time(self) -> float:
        return max((pt.trip.origin_duration for pt in self.planned_trips), default=0.0)

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

    @property
    def stops(self) -> List[Stop]:
        return self.route.stops

    @property
    def index(self) -> int:
        return self.stops.index(self)

    @property
    def previous_departure_time(self) -> float:
        if self.previous is None:
            return self.vehicle.origin_earliest
        return self.previous.departure_time

    @property
    def previous_position(self) -> Position:
        if self.previous is None:
            return self.vehicle.origin_position
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

    @cached_property
    def arrival_time(self):
        return max(self.previous_departure_time + self.down_time + self.navigation_time, self.earliest)

    @cached_property
    def departure_time(self) -> float:
        return self.arrival_time + self.load_time

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('route_uuid', self.route.uuid),
            ('position', self.position),
        )

    def flush(self) -> None:
        for key in ('arrival_time', 'departure_time',):
            self.__dict__.pop(key, None)

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
