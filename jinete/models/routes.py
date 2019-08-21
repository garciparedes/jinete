from __future__ import annotations

import logging
from math import isnan
from typing import (
    TYPE_CHECKING,
    Any, Dict, Optional)
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
        Tuple,
        Iterable,
        List,
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
    planned_trips: List[PlannedTrip]
    vehicle: Vehicle
    uuid: UUID
    stops: List[Stop]

    def __init__(self, vehicle: Vehicle, planned_trips: Iterable[PlannedTrip] = None, stops: Iterable[Stop] = None,
                 uuid: UUID = None):
        if planned_trips is None:
            planned_trips = tuple()
        if stops is None:
            stops = tuple()
        if uuid is None:
            uuid = uuid4()

        self.vehicle = vehicle
        self.planned_trips = list(planned_trips)
        self.stops = list(stops)
        self.uuid = uuid

        self._loaded_planned_trips_count = 0

    def __iter__(self):
        yield from self.planned_trips

    @property
    def feasible(self) -> bool:
        if len(self.planned_trips) > 0:
            if not self.first_trip.origin == self.vehicle.initial:
                return False
            if not self.vehicle.earliest <= self.first_planned_trip.pickup_time:
                return False
            if not self.last_trip.destination == self.vehicle.final:
                return False
            if not self.last_planned_trip.delivery_time <= self.vehicle.latest:
                return False

        for planned_trip in self.planned_trips:
            if not planned_trip.feasible:
                return False
        return True

    @property
    def loaded(self):
        return len(self.planned_trips) > 0

    @property
    def trips(self) -> Tuple[Trip]:
        return tuple(planned_trip.trip for planned_trip in self.planned_trips)

    @property
    def loaded_planned_trips(self) -> Tuple[PlannedTrip]:
        return tuple(planned_trip for planned_trip in self.planned_trips if not planned_trip.empty)

    @property
    def loaded_planned_trips_count(self) -> int:
        return self._loaded_planned_trips_count

    @property
    def loaded_trips(self) -> Tuple[Trip]:
        return tuple(planned_trip.trip for planned_trip in self.planned_trips if not planned_trip.empty)

    @property
    def first_planned_trip(self) -> Optional[PlannedTrip]:
        if len(self.planned_trips) == 0:
            return None
        # return min(self.planned_trips, key=lambda pt: pt.pickup_time)
        return self.planned_trips[0]

    @property
    def first_trip(self) -> Trip:
        return self.first_planned_trip.trip

    @property
    def last_planned_trip(self) -> Optional[PlannedTrip]:
        if len(self.planned_trips) is 0:
            return None
        # return max(self.planned_trips, key=lambda pt: pt.delivery_time)
        return self.planned_trips[-1]

    @property
    def last_trip(self) -> Trip:
        return self.last_planned_trip.trip

    @property
    def duration(self) -> float:
        if len(self.planned_trips) == 0:
            return 0.0
        return self.last_planned_trip.delivery_time - self.first_planned_trip.pickup_time

    @property
    def last_position(self) -> Position:
        if len(self.planned_trips) == 0:
            return self.vehicle.initial
        return self.last_trip.destination

    @property
    def last_stop(self) -> Stop:
        if len(self.stops) == 0:
            self.stops.append(
                Stop(self, self.vehicle.initial, None)
            )
        return self.stops[-1]

    def position_at(self, idx: int) -> Position:
        if idx < 0:
            return self.vehicle.initial
        return self.loaded_planned_trips[idx].trip.destination

    @property
    def last_time(self) -> float:
        if len(self.planned_trips) == 0:
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

    def get_stop(self, idx: int) -> Optional[Stop]:
        if (idx < 0 and len(self.stops) < abs(idx)) or len(self.stops) <= idx:
            return None
        return self.stops[idx]

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
        if len(self.planned_trips) > 0:
            assert planned_trip.pickup_stop.previous is not None
            assert self.planned_trips[-1].delivery_time <= planned_trip.pickup_time
        assert planned_trip.pickup_stop == planned_trip.delivery_stop.previous
        assert planned_trip.pickup_stop.latest <= planned_trip.delivery_stop.earliest
        assert isnan(planned_trip.duration) or planned_trip.duration > 0

        if not self.last_stop.position == planned_trip.origin:
            self._append_empty_planned_trip(
                planned_trip.origin,
                pickup_stop=self.last_stop,
                delivery_stop=planned_trip.pickup_stop,
            )
            self._loaded_planned_trips_count += 1

        self.planned_trips.append(planned_trip)

        self.stops.append(planned_trip.delivery_stop)

        logger.info(f'Append trip "{planned_trip.trip.identifier}" identifier to route "{self.uuid}".')
