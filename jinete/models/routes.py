from __future__ import (
    annotations,
)

import itertools as it
import logging
from copy import (
    deepcopy,
)
from functools import (
    reduce,
)
from operator import (
    and_,
)
from typing import (
    TYPE_CHECKING,
)

from cached_property import (
    cached_property,
)

from ..exceptions import (
    PreviousStopNotInRouteException,
)
from .abc import (
    Model,
)
from .constants import (
    ERROR_BOUND,
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
    from .vehicles import Vehicle
    from .trips import Trip
    from .positions import Position

logger = logging.getLogger(__name__)


class Route(Model):
    __slots__ = (
        "vehicle",
        "stops",
    )

    vehicle: Vehicle
    stops: List[Stop]

    def __init__(self, vehicle: Vehicle, stops: List[Stop] = None):

        self.vehicle = vehicle

        if stops is None:
            first = Stop(self.vehicle, self.vehicle.origin_position, None)
            last = Stop(self.vehicle, self.vehicle.destination_position, first)
            self.stops = [
                first,
                last,
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
        cloner = RouteCloner(self, idx)
        return cloner.clone()

    @property
    def identifier(self):
        return "|".join(stop.identifier for stop in self.stops)

    @property
    def planned_trips(self) -> Iterator[PlannedTrip]:
        return self.pickups

    @property
    def pickups(self) -> Iterator[PlannedTrip]:
        return it.chain.from_iterable(stop.pickup_planned_trips for stop in self.stops)

    @property
    def deliveries(self) -> Iterator[PlannedTrip]:
        return it.chain.from_iterable(stop.delivery_planned_trips for stop in self.stops)

    @property
    def positions(self) -> Iterator[Position]:
        yield from (stop.position for stop in self.stops)

    @property
    def feasible_stops(self) -> bool:
        return reduce(and_, (stop.feasible for stop in self.stops), True)

    @property
    def feasible_planned_trips(self) -> bool:
        return reduce(and_, (planned_trip.feasible for planned_trip in self.planned_trips), True)

    @cached_property
    def feasible(self) -> bool:
        if not self.first_stop.position == self.vehicle.origin_position:
            return False
        if not self.vehicle.origin_earliest - ERROR_BOUND <= self.first_stop.arrival_time:
            return False
        if not self.last_position == self.vehicle.destination_position:
            return False
        if not self.last_departure_time <= self.vehicle.destination_latest + ERROR_BOUND:
            return False
        if not self.duration <= self.vehicle.timeout + ERROR_BOUND:
            return False
        if not self.feasible_planned_trips:
            return False
        return True

    def flush(self):
        self.__dict__.pop("feasible", None)

        for stop in self.stops:
            stop.flush()
        for planned_trip in self.planned_trips:
            planned_trip.flush()

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
    def first_departure_time(self) -> float:
        return self.first_stop.departure_time

    @property
    def last_stop(self) -> Stop:
        stop = self.stops[-1]
        return stop

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
        return self.last_departure_time - self.first_departure_time

    @property
    def transit_time(self) -> float:
        return sum((planned_trip.duration for planned_trip in self.planned_trips), 0.0)

    @property
    def waiting_time(self) -> float:
        return sum((stop.waiting_time for stop in self.stops), 0.0)

    @property
    def distance(self) -> float:
        return sum(stop.distance for stop in self.stops)

    @property
    def vehicle_identifier(self) -> Optional[str]:
        if self.vehicle is None:
            return None
        return self.vehicle.identifier

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ("vehicle_identifier", self.vehicle_identifier),
            ("stops_identifiers", tuple(stop.identifier for stop in self.stops)),
        )

    def insert_stop(self, stop: Stop) -> Stop:
        if stop.previous is None:
            self.remove_stop_at(0)
            return self.insert_stop_at(0, stop)
        for idx in range(len(self.stops)):
            if self.stops[idx] != stop.previous:
                continue
            return self.insert_stop_at(idx + 1, stop)
        raise PreviousStopNotInRouteException(self, stop)

    def insert_stop_at(self, idx: int, stop: Stop) -> Stop:
        following_stop = self.stops[idx] or None

        assert set(stop.pickup_planned_trips).isdisjoint(stop.delivery_planned_trips)

        if following_stop is not None:
            following_stop.previous = stop

        self.stops.insert(idx, stop)

        for stop in self.stops[idx:]:
            stop.flush()

        return stop

    def remove_stop_at(self, idx: int) -> Stop:
        previous_stop = self.stops[idx - 1]
        following_stop = self.stops[idx + 1] or None

        if following_stop is not None:
            following_stop.previous = previous_stop

        removed_stop = self.stops.pop(idx)

        for stop in self.stops[idx:]:
            stop.flush()
        return removed_stop

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

    def remove_trip(self, trip: Trip) -> None:

        old_len = len(self.stops)

        for i in reversed(range(len(self.stops))):
            stop = self.stops[i]
            if trip not in stop.trips:
                continue
            self.remove_stop_at(i)

        assert old_len - 2 == len(self.stops)
        assert all(s1 == s2.previous for s1, s2 in zip(self.stops[:-1], self.stops[1:]))
        assert all(s1.departure_time <= s2.arrival_time for s1, s2 in zip(self.stops[:-1], self.stops[1:]))


class RouteCloner(object):
    def __init__(self, route: Route, idx: int = 0):
        self.route = route
        self.desired_idx = idx

        self._idx = None
        self._mapper = None

    @property
    def stops(self) -> List[Stop]:
        return self.route.stops

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

    @property
    def idx(self) -> int:
        if self._idx is None:
            self._initialize()
        return self._idx

    @property
    def mapper(self) -> Dict[PlannedTrip, PlannedTrip]:
        if self._mapper is None:
            self._initialize()
        return self._mapper

    def _initialize(self) -> None:
        idx = len(self.stops)
        mapper = dict()
        mismatches = set()
        while (idx > 0) and (any(mismatches) or not idx < self.desired_idx):
            idx -= 1

            for planned_trip in self.stops[idx].delivery_planned_trips:
                mapper[planned_trip] = PlannedTrip(planned_trip.vehicle, planned_trip.trip)

            mismatches = (mismatches | self.stops[idx].delivery_planned_trips) - self.stops[idx].pickup_planned_trips
        if idx == 1:
            idx -= 1
        assert not any(mismatches)
        self._mapper = mapper
        self._idx = idx

    def map_pickup(self, stop: Stop, planned_trip: PlannedTrip):
        new_planner_trip = self.mapper[planned_trip]
        new_planner_trip.pickup = stop
        return new_planner_trip

    def map_delivery(self, stop: Stop, planned_trip: PlannedTrip):
        new_planned_trip = self.mapper[planned_trip]
        new_planned_trip.delivery = stop
        return new_planned_trip

    def clone(self) -> Route:
        threshold = self.idx
        cloned_stops = self.stops[:threshold]
        for stop in self.stops[threshold:]:
            new_stop = Stop(
                stop.vehicle,
                stop.position,
                cloned_stops[-1] if len(cloned_stops) else None,
                starting_time=stop._starting_time,
            )

            new_stop.pickup_planned_trips = set(
                self.map_pickup(new_stop, pickup) for pickup in stop.pickup_planned_trips
            )
            new_stop.delivery_planned_trips = set(
                self.map_delivery(new_stop, delivery) for delivery in stop.delivery_planned_trips
            )

            cloned_stops.append(new_stop)

        cloned_route = Route(self.vehicle, cloned_stops)
        return cloned_route
