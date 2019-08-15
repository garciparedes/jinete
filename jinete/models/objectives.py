from __future__ import annotations
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
from .constants import (
    OptimizationDirection,
)

if TYPE_CHECKING:
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


class Objective(ABC):
    direction: OptimizationDirection

    def __init__(self, name: str, direction: OptimizationDirection):
        self.name = name
        self.direction = direction

    def best(self, *args: Result) -> Result:
        return self.direction.fn(
            (arg for arg in args if arg is not None),
            key=lambda pt: self.scoring(pt)
        )

    def scoring(self, result: Result) -> float:
        return self._planning_optimization_function(result.planning)

    def _planning_optimization_function(self, planning: Planning) -> float:
        scoring = 0.0
        for route in planning:
            scoring += self._route_optimization_function(route)
        return scoring

    def _route_optimization_function(self, route: Route) -> float:
        scoring = 0.0
        for planned_trip in route:
            scoring += self._planned_trip_optimization_function(planned_trip)
        return scoring

    @abstractmethod
    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        pass


class DialARideObjective(Objective):

    def __init__(self):
        super().__init__(
            name='Dial-a-Ride',
            direction=OptimizationDirection.MINIMIZATION,
        )

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        return planned_trip.distance


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
        if trip.earliest == planned_trip.collection_time:
            scoring += trip.on_time_bonus
        return scoring
