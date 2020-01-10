from __future__ import annotations

import logging
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
)
from cached_property import cached_property
import itertools as it

from ..exceptions import (
    PreviousStopNotInRouteException,
)
from .abc import (
    Model,
)
from .planned_trips import (
    PlannedTrip,
)
from .stops import (
    Stop,
)

if TYPE_CHECKING:
    from typing import (
        List,
        Iterator,
        Any,
        Dict,
        Optional,
        Generator,
        Tuple,
    )
    from .vehicles import (
        Vehicle,
    )
    from .trips import (
        Trip,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Route(Model):
    __slots__ = (
        'vehicle',
        'stops',
    )

    vehicle: Vehicle
    stops: List[Stop]

    def __init__(self, vehicle: Vehicle, stops: List[Stop] = None):

        self.vehicle = vehicle

        if stops is None:
            first = Stop(self.vehicle, self.vehicle.origin_position, None)
            last = Stop(self.vehicle, self.vehicle.destination_position, first)
            self.stops = [
                first, last,
            ]
        else:
            self.stops = list(stops)

    def __deepcopy__(self, memo: Dict[int, Any]) -> Route:
        vehicle = deepcopy(self.vehicle, memo)

        route = Route(vehicle)
        memo[id(self)] = route

        route.stops = deepcopy(self.stops, memo)

        return route

    def clone(self, idx: int = 0) -> Route:
        i = len(self.stops)
        mapper = dict()
        mismatches = set()
        while (i > 0) and (any(mismatches) or not i < idx):
            i -= 1

            for planned_trip in self.stops[i].deliveries:
                mapper[planned_trip] = PlannedTrip(planned_trip.vehicle, planned_trip.trip)

            mismatches = (mismatches | self.stops[i].deliveries) - self.stops[i].pickups
        assert not any(mismatches)
        idx = i

        def a(s, pt: PlannedTrip):
            npt = mapper[pt]
            npt.pickup = s
            return npt

        def b(s, pt: PlannedTrip):
            npt = mapper[pt]
            npt.delivery = s
            return npt

        cloned_stops = self.stops[:idx]
        for stop in self.stops[idx:]:
            new_stop = Stop(stop.vehicle, stop.position, cloned_stops[-1] if len(cloned_stops) else None)

            pickups = {a(new_stop, pickup) for pickup in stop.pickups}
            deliveries = {b(new_stop, delivery) for delivery in stop.deliveries}

            new_stop.pickups = pickups
            new_stop.deliveries = deliveries

            cloned_stops.append(new_stop)

        cloned_route = Route(self.vehicle, cloned_stops)
        return cloned_route

    @property
    def identifier(self):
        return '|'.join(stop.identifier for stop in self.stops)

    @property
    def planned_trips(self) -> Iterator[PlannedTrip]:
        return self.deliveries

    @property
    def pickups(self) -> Iterator[PlannedTrip]:
        return it.chain.from_iterable(stop.pickups for stop in self.stops)

    @property
    def deliveries(self) -> Iterator[PlannedTrip]:
        return it.chain.from_iterable(stop.deliveries for stop in self.stops)

    @property
    def positions(self) -> Iterator[Position]:
        yield from (stop.position for stop in self.stops)

    @cached_property
    def feasible(self) -> bool:
        if not self.first_stop.position == self.vehicle.origin_position:
            return False
        if not self.vehicle.origin_earliest <= self.first_stop.arrival_time:
            return False
        if not self.last_position == self.vehicle.destination_position:
            return False
        if not self.last_departure_time <= self.vehicle.destination_latest:
            return False
        if not self.duration <= self.vehicle.timeout:
            return False
        for planned_trip in self.planned_trips:
            if not planned_trip.feasible:
                return False
        return True

    @property
    def loaded(self):
        return any(self.planned_trips)

    @property
    def trips(self) -> Iterator[Trip]:
        yield from (planned_trip.trip for planned_trip in self.planned_trips)

    @property
    def loaded_planned_trips(self) -> Iterator[PlannedTrip]:
        yield from (planned_trip for planned_trip in self.planned_trips if not planned_trip.empty)

    @property
    def loaded_trips(self) -> Iterator[Trip]:
        yield from (planned_trip.trip for planned_trip in self.loaded_planned_trips)

    @property
    def loaded_trips_count(self) -> int:
        return sum(1 for _ in self.loaded_trips)

    @property
    def first_stop(self) -> Stop:
        stop = self.stops[0]
        assert stop.previous is None
        return stop

    @property
    def first_arrival_time(self) -> float:
        return self.first_stop.arrival_time

    @property
    def first_departure_time(self) -> float:
        return self.first_stop.departure_time

    @property
    def last_stop(self) -> Stop:
        stop = self.stops[-1]
        return stop

    @property
    def last_arrival_time(self) -> float:
        return self.last_stop.arrival_time

    @property
    def last_departure_time(self) -> float:
        return self.last_stop.departure_time

    @property
    def last_position(self) -> Position:
        return self.last_stop.position

    @property
    def current_stop(self) -> Stop:
        stop = self.stops[-2]
        return stop

    @property
    def current_arrival_time(self) -> float:
        return self.current_stop.arrival_time

    @property
    def current_departure_time(self) -> float:
        return self.current_stop.departure_time

    @property
    def current_position(self) -> Position:
        return self.current_stop.position

    @property
    def duration(self) -> float:
        return self.last_departure_time - self.first_arrival_time

    @property
    def vehicle_identifier(self) -> Optional[str]:
        if self.vehicle is None:
            return None
        return self.vehicle.identifier

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('vehicle_identifier', self.vehicle_identifier),
            ('trip_identifiers', tuple(trip.identifier for trip in self.trips))
        )

    def insert_stop(self, stop: Stop) -> Stop:
        for idx in range(len(self.stops)):
            if self.stops[idx] != stop.previous:
                continue
            return self.insert_stop_at(idx + 1, stop)
        raise PreviousStopNotInRouteException(stop)

    def insert_stop_at(self, idx: int, stop: Stop) -> Stop:
        previous_stop = self.stops[idx - 1]
        following_stop = self.stops[idx] or None

        if stop == previous_stop:
            # previous_stop.merge(stop)
            return stop

        assert set(stop.pickups).isdisjoint(stop.deliveries)

        if following_stop is not None:
            following_stop.previous = stop

        self.stops.insert(idx, stop)

        for stop in self.stops[idx + 1:]:
            stop.flush()
        return stop

    def append_planned_trip(self, planned_trip: PlannedTrip):
        assert planned_trip.delivery is not None
        assert planned_trip.pickup is not None
        assert all(s1 == s2.previous for s1, s2 in zip(self.stops[:-1], self.stops[1:]))
        assert all(s1.departure_time <= s2.arrival_time for s1, s2 in zip(self.stops[:-1], self.stops[1:]))

        self.insert_stop(planned_trip.pickup)
        self.insert_stop(planned_trip.delivery)

        assert all(s1 == s2.previous for s1, s2 in zip(self.stops[:-1], self.stops[1:]))
        assert all(s1.departure_time <= s2.arrival_time for s1, s2 in zip(self.stops[:-1], self.stops[1:]))
        logger.debug(f'Append trip with "{planned_trip.trip_identifier}" identifier to route.')
