from __future__ import annotations

import logging
from copy import deepcopy
from math import isnan
from typing import (
    TYPE_CHECKING,
)
from uuid import (
    uuid4,
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
        Iterable,
        Generator,
        Tuple,
    )
    from uuid import (
        UUID,
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
    vehicle: Vehicle
    uuid: UUID
    stops: List[Stop]

    def __init__(self, vehicle: Vehicle, stops: List[Stop] = None, uuid: UUID = None):

        if uuid is None:
            uuid = uuid4()
        self.uuid = uuid

        self.vehicle = vehicle

        if stops is None:
            self.stops = [
                Stop(self, self.vehicle.origin_position, None),
            ]
        else:
            self.stops = list(stops)

    def __deepcopy__(self, memo: Dict[int, Any]) -> Route:
        vehicle = deepcopy(self.vehicle, memo)

        route = Route(vehicle)
        memo[id(self)] = route

        route.stops = deepcopy(self.stops, memo)

        return route

    @property
    def planned_trips(self) -> Iterator[PlannedTrip]:
        yield from self.deliveries

    @property
    def pickups(self) -> Iterator[PlannedTrip]:
        for stop in self.stops:
            yield from stop.pickups

    @property
    def deliveries(self) -> Iterator[PlannedTrip]:
        for stop in self.stops:
            yield from stop.deliveries

    @property
    def feasible(self) -> bool:
        if any(self.planned_trips):
            if not self.first_stop.position == self.vehicle.origin_position:
                return False
            if not self.vehicle.origin_earliest <= self.first_stop.arrival_time:
                return False
            if not self.last_position == self.vehicle.destination_position:
                return False
            if not self.last_departure_time <= self.vehicle.origin_latest:
                return False

        if __debug__:
            for stop in self.stops:
                assert stop.route == self

            for one, two in zip(self.stops[:-1], self.stops[1:]):
                assert one.following == two
                assert two.previous == one
                assert one.position != two.position

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
    def first_arrival_time(self) -> float:
        return self.first_stop.arrival_time

    @property
    def first_departure_time(self) -> float:
        return self.first_stop.departure_time

    @property
    def last_arrival_time(self) -> float:
        return self.last_stop.arrival_time

    @property
    def last_departure_time(self) -> float:
        return self.last_stop.departure_time

    @property
    def duration(self) -> float:
        return self.last_departure_time - self.first_arrival_time

    @property
    def last_position(self) -> Position:
        return self.last_stop.position

    @property
    def first_stop(self) -> Stop:
        stop = self.stops[0]
        assert stop.previous is None
        return stop

    @property
    def last_stop(self) -> Stop:
        stop = self.stops[-1]
        assert stop.following is None
        return stop

    @property
    def vehicle_identifier(self) -> Optional[str]:
        if self.vehicle is None:
            return None
        return self.vehicle.identifier

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('uuid', self.uuid),
            ('vehicle_identifier', self.vehicle_identifier),
            ('trip_identifiers', tuple(trip.identifier for trip in self.trips))
        )

    def conjecture_trip(self, trip: Trip) -> PlannedTrip:
        pickup = Stop(self, trip.origin_position, self.last_stop)
        delivery = Stop(self, trip.destination_position, pickup)
        planned_trip = PlannedTrip(route=self, trip=trip, pickup=pickup, delivery=delivery)
        return planned_trip

    def conjecture_trip_in_batch(self, iterable: Iterable[Trip]) -> List[PlannedTrip]:
        return [self.conjecture_trip(trip) for trip in iterable]

    def finish(self):
        # if self.loaded and self.last_stop.position != self.vehicle.final:
        if self.last_stop.position != self.vehicle.destination_position:
            finish_stop = Stop(self, self.vehicle.destination_position, self.last_stop)
            if not self.last_stop.position == finish_stop.position:
                self.append_stop(finish_stop)

    def append_stop(self, stop: Stop) -> None:
        assert stop.previous == self.last_stop
        assert set(stop.pickups).isdisjoint(stop.deliveries)
        if __debug__:
            for planned_trip in stop.pickups:
                assert planned_trip.pickup == stop
            for planned_trip in stop.deliveries:
                assert planned_trip.delivery == stop
        self.last_stop.following = stop
        self.stops.append(stop)

    def append_planned_trip(self, planned_trip: PlannedTrip):
        assert planned_trip.delivery is not None
        assert planned_trip.pickup is not None
        assert planned_trip.delivery.previous is not None
        assert planned_trip.pickup_time <= planned_trip.delivery_time
        assert isnan(planned_trip.duration) or planned_trip.duration > 0

        if not planned_trip.pickup == self.last_stop:
            if self.last_stop.position == planned_trip.pickup.position:
                self.last_stop.merge(planned_trip.pickup)
                planned_trip.delivery.previous = self.last_stop  # FIXME: should be inside merge?
            else:
                self.append_stop(planned_trip.pickup)

        self.append_stop(planned_trip.delivery)

        logger.info(f'Append trip "{planned_trip.trip_identifier}" identifier to route "{self.uuid}".')
