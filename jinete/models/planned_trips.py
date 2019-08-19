from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from uuid import (
    uuid4,
)
from .abc import (
    Model,
)
from .trips import (
    Trip,
)

from .stops import (
    Stop,
    StopKind,
    StopCause,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
        List,
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
    uuid: UUID
    route: Route
    stops: List[Stop]
    trip: Trip
    down_time: float

    def __init__(self, route: Route, trip: Trip, first: Stop, last: Stop, initial: Stop = None, final: Stop = None,
                 down_time: float = 0.0):

        self.uuid = uuid4()
        self.route = route
        self.trip = trip
        self.down_time = down_time

        self.stops = list()

        self.stops.append(first)
        if first.position == trip.origin:
            initial = first
        else:
            if initial is None:
                initial = Stop(route, trip.origin)
            self.stops.append(initial)
        initial.append_stop_cause(
            StopCause(self, StopKind.PICKUP)
        )

        if last.position == trip.destination:
            final = last
        else:
            if final is None:
                final = Stop(route, trip.destination)
            self.stops.append(final)
        final.append_stop_cause(
            StopCause(self, StopKind.DELIVERY)
        )
        self.stops.append(last)

        self._pickup_time = None
        self._delivery_time = None
        self._feasible = None

    @staticmethod
    def build_empty(route: Route, first, last, initial, final,
                    *args, **kwargs) -> 'PlannedTrip':
        trip = Trip.build_empty(*args, **kwargs)
        return PlannedTrip(
            route=route,
            first=first,
            last=last,
            initial=initial,
            final=final,
            trip=trip,
        )

    @property
    def first_stop(self) -> Stop:
        return self.stops[0]

    @property
    def last_stop(self) -> Stop:
        return self.stops[-1]

    @property
    def pickup_stop(self) -> Stop:
        for stop in self.stops:
            if self not in stop.planned_trips:
                continue
            return stop
        # TODO: Improve this exception
        raise Exception

    @property
    def delivery_stop(self) -> Stop:
        for stop in reversed(self.stops):
            if self not in stop.planned_trips:
                continue
            return stop
        # TODO: Improve this exception
        raise Exception

    @property
    def pickup_time(self) -> float:
        if self._pickup_time is None:
            self._pickup_time = self._calculate_pickup_time()
        return self._pickup_time

    @property
    def delivery_time(self) -> float:
        if self._delivery_time is None:
            self._delivery_time = self._calculate_delivery_time()
        return self._delivery_time

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

    @property
    def trip_uuid(self) -> UUID:
        return self.trip.uuid

    @property
    def route_uuid(self) -> UUID:
        return self.route.uuid

    @property
    def origin(self) -> Position:
        return self.trip.origin

    @property
    def destination(self) -> Position:
        return self.trip.destination

    @property
    def distance(self) -> float:
        return self.trip.distance

    @property
    def duration(self) -> float:
        return self.delivery_time - self.pickup_time

    @property
    def capacity(self):
        return self.trip.capacity

    @property
    def feasible(self) -> bool:
        if self._feasible is None:
            self._feasible = self._calculate_feasible()
        return self._feasible

    @property
    def empty(self) -> bool:
        return self.trip.empty

    @property
    def first_position(self) -> Position:
        if self in self.first_stop.planned_trips:
            return self.vehicle.initial
        return self.first_stop.position

    @property
    def first_delivery_time(self) -> float:
        if self in self.first_stop.planned_trips:
            return self.vehicle.earliest
        return self.first_stop.time

    def as_dict(self) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'route_uuid': self.route_uuid,
            'trip_uuid': self.trip_uuid,
            # 'initial': self.initial,
            'down_time': self.down_time,
            'feasible': self.feasible,
        }

    def flush(self) -> None:
        self._pickup_time = None
        self._delivery_time = None
        self._feasible = None

    def _calculate_pickup_time(self) -> float:
        trip_start_time = max(self.first_delivery_time, self.trip.earliest)
        trip_start_time += self.down_time
        return trip_start_time

    def _calculate_delivery_time(self) -> float:
        time_to_travel = self.trip.duration(self.pickup_time)
        trip_finish_time = self.pickup_time + time_to_travel + self.trip.load_time
        return trip_finish_time

    def _calculate_feasible(self) -> bool:
        if not self.first_delivery_time <= self.trip.latest:
            return False

        if self.trip.inbound:
            if not self.trip.earliest <= self.delivery_time <= self.trip.latest:
                return False
        else:
            if not self.trip.earliest <= self.pickup_time <= self.trip.latest:
                return False

        time_to_return = self.trip.destination.time_to(self.vehicle.final, self.delivery_time)
        vehicle_finish_time = self.delivery_time + time_to_return
        if not vehicle_finish_time <= self.vehicle.latest:
            return False

        if self.vehicle.vehicle_timeout is not None:
            if not self.duration <= self.vehicle.vehicle_timeout:
                return False

        if self.vehicle.trip_timeout is not None:
            if not self.duration <= self.vehicle.trip_timeout:
                return False

        return True
