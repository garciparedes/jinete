from __future__ import annotations
from abc import ABC

from typing import (
    TYPE_CHECKING,
    TypeVar)
from .constants import (
    OptimizationDirection,
)

from .routes import (
    Route,
)
from .plannings import (
    Planning,
)
from .planned_trips import (
    PlannedTrip,
)
from .results import (
    Result,
)
from .stops import (
    Stop,
)

if TYPE_CHECKING:
    from typing import (
        Optional
    )

    Optimizable = TypeVar('Optimizable', Result, Planning, Route, Stop, PlannedTrip)


class Objective(ABC):
    direction: OptimizationDirection

    def __init__(self, name: str, direction: OptimizationDirection):
        self.name = name
        self.direction = direction

    def best(self, *args: Optional[Optimizable]) -> Optimizable:
        return self.direction(
            (arg for arg in args if arg is not None),
            key=self.optimization_function,
            default=None,
        )

    def optimization_function(self, value: Optimizable) -> float:
        if isinstance(value, Result):
            return self._result_optimization_function(value)
        elif isinstance(value, Planning):
            return self._planning_optimization_function(value)
        elif isinstance(value, Route):
            return self._route_optimization_function(value)
        elif isinstance(value, Stop):
            return self._stop_optimization_function(value)
        elif isinstance(value, PlannedTrip):
            return self._planned_trip_optimization_function(value)
        else:
            raise ValueError

    def _result_optimization_function(self, result: Result) -> float:
        return self._planning_optimization_function(result.planning)

    def _planning_optimization_function(self, planning: Planning) -> float:
        scoring = 0.0
        for route in planning.routes:
            scoring += self._route_optimization_function(route)
        return scoring

    def _route_optimization_function(self, route: Route) -> float:
        scoring = 0.0
        for stop in route.stops:
            scoring += self._stop_optimization_function(stop)
        return scoring

    def _stop_optimization_function(self, stop: Stop) -> float:
        scoring = 0.0
        for planned_trip in stop.pickups:
            scoring += self._planned_trip_optimization_function(planned_trip)
        return scoring

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        raise NotImplementedError


class DialARideObjective(Objective):

    def __init__(self):
        super().__init__(
            name='Dial-a-Ride',
            direction=OptimizationDirection.MINIMIZATION,
        )

    def _route_optimization_function(self, route: Route) -> float:
        scoring = 0.0
        for stop in route.stops:
            scoring += stop.distance
        return scoring

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        scoring = 0.0
        current = planned_trip.pickup
        while current != planned_trip.delivery and current.following is not None:
            current = current.following
            scoring += current.distance
        return scoring


class TaxiSharingObjective(Objective):

    def __init__(self):
        super().__init__(
            name='Taxi-Sharing',
            direction=OptimizationDirection.MAXIMIZATION,
        )

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        if planned_trip.capacity == 0:
            return 0.0
        return planned_trip.duration


class HashCodeObjective(Objective):
    def __init__(self):
        super().__init__(
            name='HashCode-2018',
            direction=OptimizationDirection.MAXIMIZATION,
        )

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        if planned_trip.capacity == 0:
            return 0.0
        trip = planned_trip.trip
        scoring = trip.distance
        if trip.origin_earliest == planned_trip.pickup_time:
            scoring += trip.on_time_bonus
        return scoring
