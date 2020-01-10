from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)
import itertools as it

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
        Set,
    )
    from .positions import (
        Position,
    )
    from .planned_trips import (
        PlannedTrip
    )
    from .vehicles import (
        Vehicle,
    )

logger = logging.getLogger(__name__)


class Stop(Model):
    __slots__ = [
        'vehicle',
        'position',
        'pickups',
        'deliveries',
        'previous',
    ]
    vehicle: Vehicle
    position: Position
    previous: Optional[Stop]
    pickups: Set[PlannedTrip, ...]
    deliveries: Set[PlannedTrip, ...]

    def __init__(self, vehicle: Vehicle, position: Position, previous: Optional[Stop],
                 pickups: Set[PlannedTrip, ...] = None, deliveries: Set[PlannedTrip, ...] = None):

        if pickups is None:
            pickups = set()
        if deliveries is None:
            deliveries = set()

        self.vehicle = vehicle
        self.position = position

        self.pickups = pickups
        self.deliveries = deliveries

        self.previous = previous

    @property
    def identifier(self) -> str:
        trips_sequence = ''.join(
            it.chain(
                (f'P{planned_trip.trip_identifier}' for planned_trip in self.pickups),
                (f'D{planned_trip.trip_identifier}' for planned_trip in self.deliveries),
            )
        )
        return ','.join((
            f'{self.position}',
            f'{self.arrival_time:.2f}:{self.departure_time:.2f}',
            f'({trips_sequence})',
        ))

    @property
    def planned_trips(self) -> Iterable[PlannedTrip]:
        yield from self.pickups
        yield from self.deliveries

    @property
    def trips(self):
        yield from (planned_trip.trip for planned_trip in self.planned_trips)

    @property
    def capacity(self) -> float:
        result = sum(trip.capacity for trip in self.planned_trips)
        assert 0 <= result
        return result

    @property
    def all_previous(self) -> List[Stop]:
        if self.previous is None:
            return []
        return [self.previous] + self.previous.all_previous

    def append_pickup(self, planned_trip: PlannedTrip) -> None:
        assert planned_trip.origin == self.position
        self.pickups.add(planned_trip)

    def append_delivery(self, planned_trip: PlannedTrip) -> None:
        assert planned_trip.destination == self.position
        self.deliveries.add(planned_trip)

    def extend_pickups(self, iterable: Iterable[PlannedTrip]) -> None:
        self.pickups.update(iterable)

    def extend_deliveries(self, iterable: Iterable[PlannedTrip]) -> None:
        self.deliveries.update(iterable)

    @property
    def down_time(self) -> float:
        if not any(self.pickups):
            return 0.0
        return max(pt.down_time for pt in self.pickups)

    @property
    def earliest(self):
        if not any(self.pickups):
            return 0.0
        return max(pt.trip.origin_earliest for pt in self.pickups)

    @property
    def load_time(self) -> float:
        if not any(self.planned_trips):
            return 0.0
        return max(pt.trip.origin_duration for pt in self.planned_trips)

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
            ('position', self.position),
            ('identifier', self.identifier),
        )

    def flush(self) -> None:
        for key in ('arrival_time', 'departure_time',):
            self.__dict__.pop(key, None)
        for planned_trip in self.planned_trips:
            planned_trip.flush()

    def flush_all_previous(self):
        self.flush()
        if self.previous is not None:
            self.previous.flush_all_previous()

    def merge(self, other: Stop) -> None:
        if self == other:
            return
        assert self.position == other.position

        self.extend_pickups(other.pickups)
        for planned_trip in other.pickups:
            planned_trip.pickup = self

        self.extend_deliveries(other.deliveries)
        for planned_trip in other.deliveries:
            planned_trip.delivery = self
