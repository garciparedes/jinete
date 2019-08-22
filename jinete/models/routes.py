from __future__ import annotations

import logging
from collections import deque
from math import isnan
from typing import (
    TYPE_CHECKING,
    Iterator)
import itertools as it
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
    StopKind)

if TYPE_CHECKING:
    from typing import (
        Tuple,
        List,
        Any,
        Dict,
        Optional,
    )
    from uuid import (
        UUID,
    )
    from .vehicles import (
        Vehicle,
    )
    from .stops import (
        StopCause,
    )
    from .trips import (
        Trip,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Route(Model):
    planned_trips: List[PlannedTrip]
    vehicle: Vehicle
    uuid: UUID
    stops: List[Stop]

    def __init__(self, vehicle: Vehicle, stops: List[Stop] = None,
                 uuid: UUID = None):

        if uuid is None:
            uuid = uuid4()
        self.uuid = uuid

        self.vehicle = vehicle

        if stops is None:
            stops = (
                Stop(self, self.vehicle.initial, None),
            )
        self.stops = list(stops)

    def __iter__(self):
        yield from self.planned_trips

    @property
    def planned_trips(self) -> Iterator[PlannedTrip]:
        return iter(
            stop_cause.planned_trip
            for stop_cause in self.stop_causes
            if stop_cause.kind == StopKind.DELIVERY
        )

    @property
    def stop_causes(self) -> Iterator[StopCause]:
        return it.chain.from_iterable(stop.causes for stop in self.stops)

    @property
    def feasible(self) -> bool:
        if any(self.planned_trips):
            if not self.first_stop.position == self.vehicle.initial:
                return False
            if not self.vehicle.earliest <= self.first_stop.earliest:
                return False
            if not self.last_position == self.vehicle.final:
                return False
            if not self.last_planned_trip.delivery_time <= self.vehicle.latest:
                return False

        for planned_trip in self.planned_trips:
            if not planned_trip.feasible:
                return False
        return True

    @property
    def loaded(self):
        return any(self.planned_trips)

    @property
    def trips(self) -> Tuple[Trip]:
        return tuple(planned_trip.trip for planned_trip in self.planned_trips)

    @property
    def loaded_planned_trips(self) -> Tuple[PlannedTrip]:
        return tuple(planned_trip for planned_trip in self.planned_trips if not planned_trip.empty)

    @property
    def loaded_trips(self) -> Tuple[Trip]:
        return tuple(planned_trip.trip for planned_trip in self.planned_trips if not planned_trip.empty)

    @property
    def first_planned_trip(self) -> Optional[PlannedTrip]:
        if any(self.planned_trips):
            return None
        # return min(self.planned_trips, key=lambda pt: pt.pickup_time)
        return next(self.planned_trips)

    @property
    def first_trip(self) -> Trip:
        return self.first_planned_trip.trip

    @property
    def last_planned_trip(self) -> Optional[PlannedTrip]:
        if not any(self.planned_trips):
            return None
        # return max(self.planned_trips, key=lambda pt: pt.delivery_time)
        return deque(self.planned_trips, maxlen=1).pop()

    @property
    def last_trip(self) -> Trip:
        return self.last_planned_trip.trip

    @property
    def earliest(self) -> float:
        return self.first_stop.arrival_time

    @property
    def latest(self) -> float:
        return self.last_stop.departure_time

    @property
    def duration(self) -> float:
        return self.latest - self.earliest

    @property
    def last_position(self) -> Position:
        return self.last_stop.position

    @property
    def first_stop(self) -> Stop:
        return self.stops[0]

    @property
    def last_stop(self) -> Stop:
        return self.stops[-1]

    @property
    def last_time(self) -> float:
        if not any(self.planned_trips):
            return self.vehicle.earliest
        return self.last_planned_trip.delivery_time

    def time_at(self, idx: int) -> float:
        if idx < 0:
            return self.vehicle.earliest
        return self.loaded_planned_trips[idx].delivery_time

    @property
    def vehicle_uuid(self) -> Optional[UUID]:
        if self.vehicle is None:
            return None
        return self.vehicle.uuid

    def as_dict(self) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'vehicle_uuid': self.vehicle_uuid,
        }

    def conjecture_trip(self, trip: Trip) -> Optional[PlannedTrip]:
        pickup_stop = self.last_stop
        if pickup_stop.position != trip.origin:
            pickup_stop = Stop(self, trip.origin, self.last_stop)

        delivery_stop = Stop(self, trip.destination, pickup_stop)

        return PlannedTrip(
            route=self,
            trip=trip,
            pickup_stop=pickup_stop,
            delivery_stop=delivery_stop,
        )

    def _append_empty_planned_trip(self, destination: Position, pickup_stop: Stop, delivery_stop: Stop) -> PlannedTrip:
        planned_trip = PlannedTrip.build_empty(
            route=self,
            origin=self.last_position,
            destination=destination,
            pickup_stop=pickup_stop,
            delivery_stop=delivery_stop,
        )
        self.append_planned_trip(planned_trip)
        return planned_trip

    def finish(self):
        if self.loaded and self.last_stop.position != self.vehicle.final:
            self._append_empty_planned_trip(
                self.vehicle.final,
                pickup_stop=self.last_stop,
                delivery_stop=Stop(self, self.vehicle.final, self.last_stop),
            )

    def append_planned_trip(self, planned_trip: PlannedTrip):
        assert planned_trip.delivery_stop is not None
        assert planned_trip.pickup_stop is not None
        assert planned_trip.delivery_stop.previous is not None
        if len(self.stops) > 1:
            assert planned_trip.pickup_stop.previous is not None
            assert self.last_planned_trip.delivery_time <= planned_trip.pickup_time
        assert planned_trip.pickup_stop == planned_trip.delivery_stop.previous
        assert planned_trip.pickup_stop.latest <= planned_trip.delivery_stop.earliest
        assert isnan(planned_trip.duration) or planned_trip.duration > 0

        if not self.last_stop.position == planned_trip.origin:
            self._append_empty_planned_trip(
                planned_trip.origin,
                pickup_stop=self.last_stop,
                delivery_stop=planned_trip.pickup_stop,
            )

        self.stops.append(planned_trip.delivery_stop)

        logger.info(f'Append trip "{planned_trip.trip.identifier}" identifier to route "{self.uuid}".')
