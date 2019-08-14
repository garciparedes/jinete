from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        Callable,
        Sequence,
        Any,
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


class DirectionObjective(Enum):
    MAXIMIZE = 1
    MINIMIZE = -1


class Objective(ABC):
    direction: DirectionObjective

    def __init__(self, name: str, direction: DirectionObjective):
        self.name = name
        self.direction = direction

    @property
    def _direction_function(self) -> Callable[[Sequence[Any]], float]:
        if self.direction == DirectionObjective.MAXIMIZE:
            return max
        else:
            return min

    def result_optimization_function(self, result: Result) -> float:
        return self.planning_optimization_function(result.planning)

    def planning_optimization_function(self, planning: Planning) -> float:
        scoring = 0.0
        for route in planning:
            scoring += self.route_optimization_function(route)
        return scoring

    def route_optimization_function(self, route: Route) -> float:
        scoring = 0.0
        for planned_trip in route:
            scoring += self.planned_trip_optimization_function(planned_trip)
        return scoring

    @abstractmethod
    def planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        pass

    def planned_trip_scoring_function(self, planned_trip: PlannedTrip) -> float:
        return planned_trip.collection_time - planned_trip.route.last_time

    def best_planned_trip(self, *args) -> float:
        return self._direction_function(
            (arg for arg in args if arg is not None),
            key=lambda pt: self.planned_trip_scoring_function(pt),
        )

    def best_result(self, *args) -> float:
        return self._direction_function(
            (arg for arg in args if arg is not None),
            key=lambda pt: self.result_optimization_function(pt)
        )


class DialARideObjective(Objective):

    def __init__(self):
        super().__init__(
            name='Dial-a-Ride',
            direction=DirectionObjective.MINIMIZE,
        )

    def planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        return planned_trip.cost


class TaxiSharingObjective(Objective):

    def __init__(self):
        super().__init__(
            name='Taxi-Sharing',
            direction=DirectionObjective.MAXIMIZE,
        )

    def planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        if planned_trip.capacity == 0:
            return 0.0
        return planned_trip.duration


class HashCodeObjective(Objective):
    def __init__(self):
        super().__init__(
            name='HashCode-2018',
            direction=DirectionObjective.MAXIMIZE,
        )

    def planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> float:
        if planned_trip.capacity == 0:
            return 0.0
        trip = planned_trip.trip
        scoring = trip.distance
        if trip.earliest == planned_trip.collection_time:
            scoring += trip.on_time_bonus
        return scoring
