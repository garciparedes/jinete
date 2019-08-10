from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Any, Dict, Optional)
from uuid import (
    uuid4,
)
from .abc import (
    Model,
)
from .trips import (
    PlannedTrip,
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

    def __init__(self, vehicle: Vehicle, planned_trips: Iterable[PlannedTrip] = None, uuid=None):
        if planned_trips is None:
            planned_trips = tuple()
        if uuid is None:
            uuid = uuid4()

        self.vehicle = vehicle
        self.planned_trips = list(planned_trips)
        self.uuid = uuid

    @property
    def feasible(self) -> bool:
        if len(self.planned_trips) > 0:
            if not self.first_trip.origin == self.vehicle.initial:
                return False
            if not self.vehicle.earliest <= self.first_planned_trip.collection_time:
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
    def cost(self) -> float:
        cost = 0.0
        for planned_trip in self.planned_trips:
            cost += planned_trip.cost
        return cost

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
    def loaded_trips(self) -> Tuple[Trip]:
        return tuple(planned_trip.trip for planned_trip in self.planned_trips if not planned_trip.empty)

    @property
    def first_planned_trip(self) -> PlannedTrip:
        return min(self.planned_trips, key=lambda pt: pt.collection_time)

    @property
    def first_trip(self) -> Trip:
        return self.first_planned_trip.trip

    @property
    def last_planned_trip(self) -> PlannedTrip:
        # return max(self.planned_trips, key=lambda pt: pt.delivery_time)
        return self.planned_trips[-1]

    @property
    def last_trip(self) -> Trip:
        return self.last_planned_trip.trip

    @property
    def duration(self) -> float:
        return self.last_planned_trip.delivery_time - self.first_planned_trip.collection_time

    @property
    def last_position(self) -> Position:
        if len(self.planned_trips) == 0:
            return self.vehicle.initial
        return self.last_trip.destination

    @property
    def last_time(self) -> float:
        if len(self.planned_trips) == 0:
            return self.vehicle.earliest
        return self.last_planned_trip.delivery_time

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

    def feasible_trip(self, trip: Trip) -> Optional[PlannedTrip]:
        if not self.last_time <= trip.latest:
            return None

        time_to_go = self.last_position.distance_to(trip.origin)
        time_to_travel = trip.duration(time_to_go)
        trip_start_time = max(self.last_time + time_to_go, trip.earliest)
        trip_finish_time = trip_start_time + time_to_travel
        if not trip_finish_time <= trip.latest:
            return None

        time_to_return = trip.destination.time_to(self.vehicle.final, trip_finish_time)
        vehicle_finish_time = trip_finish_time + time_to_return
        if not vehicle_finish_time <= self.vehicle.latest:
            return None

        return PlannedTrip(self, trip, trip_start_time, trip_finish_time)

    def _append_empty_planned_trip(self, destination: Position) -> PlannedTrip:
        planned_trip = PlannedTrip.build_empty(
            route=self,
            collection_time=self.last_time,
            delivery_time=self.last_time + self.last_position.time_to(destination, self.last_time),
            origin=self.last_position,
            destination=destination,
        )
        self.append_planned_trip(planned_trip)
        return planned_trip

    def _append_finish_planned_trip(self) -> PlannedTrip:
        return self._append_empty_planned_trip(self.vehicle.final)

    def finish(self):
        if self.loaded:
            self._append_finish_planned_trip()

    def append_planned_trip(self, planned_trip: PlannedTrip):
        if not self.last_position.is_equal(planned_trip.origin):
            self._append_empty_planned_trip(planned_trip.origin)
        self.planned_trips.append(planned_trip)
        logger.info(f'Append trip "{planned_trip.trip.identifier}" identifier to route "{self.uuid}".')
