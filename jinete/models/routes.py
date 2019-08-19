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
from .planned_trips import (
    PlannedTrip,
)
from .stops import (
    Stop,
    StopKind,
    StopCause,
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

    def __init__(self, vehicle: Vehicle, planned_trips: Iterable[PlannedTrip] = None, stops: Iterable[Stop] = None,
                 uuid: UUID = None):
        if planned_trips is None:
            planned_trips = tuple()
        if uuid is None:
            uuid = uuid4()

        self.vehicle = vehicle
        self.planned_trips = list(planned_trips)

        if stops is None:
            # planned_trip = PlannedTrip.build_empty(
            #     route=self,
            #     origin=vehicle.initial,
            #     destination=vehicle.final,
            # )
            #
            # initial = Stop(self, vehicle.initial)
            # initial.append_stop_cause(
            #     StopCause(planned_trip, StopKind.PICKUP)
            # )
            #
            # final = Stop(self, vehicle.final)
            # final.append_stop_cause(
            #     StopCause(planned_trip, StopKind.DELIVERY)
            # )
            #
            # stops = (
            #     initial,
            #     final,
            # )
            stops = tuple()
        self.stops = list(stops)
        self.uuid = uuid

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
    def last_stop(self) -> Optional[Stop]:
        return self.get_stop(-1)

    def get_stop(self, idx: int) -> Optional[Stop]:
        if (idx < 0 and len(self.stops) < abs(idx)) or len(self.stops) <= idx:
            return None
        return self.stops[idx]

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

    def conjecture_trip(self, trip: Trip) -> Optional[PlannedTrip]:

        first = self.get_stop(-2)
        if first is None:
            first = Stop(self, self.vehicle.initial)

        last = self.get_stop(-1)
        if last is None:
            last = Stop(self, self.vehicle.final)

        planned_trip = PlannedTrip(
            route=self,
            trip=trip,
            first=first,
            last=last,
        )
        return planned_trip

    def _append_empty_planned_trip(self, destination: Position, first, initial, final, last) -> PlannedTrip:
        planned_trip = PlannedTrip.build_empty(
            route=self,
            first=first,
            initial=initial,
            final=final,
            last=last,
            origin=self.last_position,
            destination=destination,
        )
        self.append_planned_trip(planned_trip)
        return planned_trip

    def _append_finish_planned_trip(self) -> PlannedTrip:
        return self._append_empty_planned_trip(
            self.vehicle.final,
            self.get_stop(-2),
            self.get_stop(-2),
            self.get_stop(-1),
            self.get_stop(-1),
        )

    def finish(self):
        if self.loaded:
            self._append_finish_planned_trip()

    def append_planned_trip(self, planned_trip: PlannedTrip):
        if not self.last_position.is_equal(planned_trip.origin):
            first = self.get_stop(-2)
            if first is None:
                first = planned_trip.stops[0]
            last = self.get_stop(-1)
            if last is None:
                last = planned_trip.stops[-1]
            self._append_empty_planned_trip(
                planned_trip.origin,
                first,
                planned_trip.stops[0],
                planned_trip.stops[1],
                last,
            )

        if len(self.stops) > 0:
            for pt in self.last_stop.planned_trips:
                pt.stops[-1] = planned_trip.first_stop

            if self.get_stop(-2) != planned_trip.pickup_stop:
                self.stops.insert(-1, planned_trip.pickup_stop)
            if self.get_stop(-2) != planned_trip.delivery_stop:
                self.stops.insert(-1, planned_trip.delivery_stop)
        else:
            self.stops += planned_trip.stops

        self.planned_trips.append(planned_trip)

        logger.info(f'Append trip "{planned_trip.trip.identifier}" identifier to route "{self.uuid}".')
