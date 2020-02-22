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
from .constants import (
    MAX_FLOAT,
    ERROR_BOUND,
)

if TYPE_CHECKING:
    from typing import (
        Generator,
        Tuple,
        Any,
        Optional,
        Iterator,
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
        '_starting_time',
    ]
    vehicle: Vehicle
    position: Position
    previous: Optional[Stop]
    pickups: Set[PlannedTrip, ...]
    deliveries: Set[PlannedTrip, ...]

    def __init__(self, vehicle: Vehicle, position: Position, previous: Optional[Stop],
                 pickups: Set[PlannedTrip, ...] = None, deliveries: Set[PlannedTrip, ...] = None,
                 starting_time: float = None):

        if pickups is None:
            pickups = set()
        if deliveries is None:
            deliveries = set()

        self.vehicle = vehicle
        self.position = position

        self.pickups = pickups
        self.deliveries = deliveries

        self.previous = previous
        self._starting_time = starting_time

    @property
    def identifier(self) -> str:
        iterable = it.chain(
            (f'P{planned_trip.trip_identifier}' for planned_trip in self.pickups),
            (f'D{planned_trip.trip_identifier}' for planned_trip in self.deliveries),
        )
        identifier = '|'.join(iterable)
        identifier = f'[{identifier}]'
        return identifier

    @property
    def planned_trips(self) -> Iterator[PlannedTrip]:
        yield from self.pickups
        yield from self.deliveries

    @property
    def trips(self):
        yield from (planned_trip.trip for planned_trip in self.planned_trips)

    @cached_property
    def capacity(self) -> float:
        result = self.previous_capacity
        result += sum(trip.capacity for trip in self.pickups)
        result -= sum(trip.capacity for trip in self.deliveries)
        assert 0 <= result
        return result

    @property
    def previous_capacity(self) -> float:
        if self.previous is None:
            return 0
        return self.previous.capacity

    @property
    def all_previous(self) -> List[Stop]:
        if self.previous is None:
            return []
        return [self.previous] + self.previous.all_previous

    @property
    def all_previous_pickups(self) -> Iterator[PlannedTrip]:
        return it.chain.from_iterable(stop.pickups for stop in self.all_previous)

    def append_pickup(self, planned_trip: PlannedTrip) -> None:
        assert planned_trip.origin == self.position
        self.pickups.add(planned_trip)

    def append_delivery(self, planned_trip: PlannedTrip) -> None:
        assert planned_trip.destination == self.position
        self.deliveries.add(planned_trip)

    @cached_property
    def feasible(self) -> bool:
        if not self.earliest <= self.starting_time + ERROR_BOUND:
            return False

        if not self.starting_time <= self.latest + ERROR_BOUND:
            return False

        if not self.capacity <= self.vehicle.capacity + ERROR_BOUND:
            return False

        return True

    @property
    def previous_position(self) -> Position:
        if self.previous is None:
            return self.vehicle.origin_position
        return self.previous.position

    @property
    def distance(self) -> float:
        return self.position.distance_to(self.previous_position)

    @cached_property
    def arrival_time(self):
        return self.previous_departure_time + self.transit_time

    @property
    def previous_departure_time(self) -> float:
        if self.previous is None:
            return self.vehicle.origin_earliest
        return self.previous.departure_time

    @property
    def transit_time(self):
        return self.previous_position.time_to(self.position, self.previous_departure_time)

    @property
    def waiting_time(self):
        waiting_time = self.starting_time - self.arrival_time
        assert waiting_time >= 0 - ERROR_BOUND
        return waiting_time

    @cached_property
    def departure_time(self) -> float:
        return self.starting_time + self.load_time

    @property
    def starting_time(self) -> float:
        value = self._starting_time
        if value is None:
            value = self.arrival_time
        return max((value, self.earliest, self.arrival_time))

    @starting_time.setter
    def starting_time(self, value: float) -> None:
        self._starting_time = value
        self.flush()

    @property
    def earliest(self) -> float:
        return max(it.chain(
            (pt.trip.origin_earliest for pt in self.pickups),
            (pt.trip.destination_earliest for pt in self.deliveries),
        ), default=0.0)

    @property
    def latest(self) -> float:
        return min(it.chain(
            (pt.trip.origin_latest for pt in self.pickups),
            (pt.trip.destination_latest for pt in self.deliveries),
        ), default=MAX_FLOAT)

    @property
    def load_time(self) -> float:
        return max(it.chain(
            (pt.trip.origin_duration for pt in self.pickups),
            (pt.trip.destination_duration for pt in self.deliveries),
        ), default=0.0)

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('position', self.position),
            ('identifier', self.identifier),
        )

    def flush(self) -> None:
        for key in ('arrival_time', 'departure_time', 'capacity',):
            self.__dict__.pop(key, None)
        for planned_trip in self.planned_trips:
            planned_trip.flush()

    def flush_all_previous(self):
        self.flush()
        if self.previous is not None:
            self.previous.flush_all_previous()
