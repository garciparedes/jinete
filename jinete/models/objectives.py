from __future__ import annotations

import logging
from abc import ABC
from functools import reduce
from operator import add

from typing import (
    TYPE_CHECKING,
)
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
        Optional,
        TypeVar,
        Tuple,
    )

    Optimizable = TypeVar('Optimizable', Result, Planning, Route, Stop, PlannedTrip, Tuple[float, ...])

logger = logging.getLogger(__name__)


class Objective(ABC):
    direction: OptimizationDirection

    def __init__(self, name: str, dimension_count: int):
        self.name = name
        self.direction = OptimizationDirection.MAXIMIZATION
        self.dimension_count = dimension_count

    def best(self, *args: Optional[Optimizable]) -> Optimizable:
        return self.direction(
            (arg for arg in args if arg is not None),
            key=self.optimization_function,
            default=None,
        )

    def optimization_function(self, value: Optimizable) -> Tuple[float, ...]:
        if isinstance(value, Result):
            result = self._result_optimization_function(value)
        elif isinstance(value, Planning):
            result = self._planning_optimization_function(value)
        elif isinstance(value, Route):
            result = self._route_optimization_function(value)
        elif isinstance(value, Stop):
            result = self._stop_optimization_function(value)
        elif isinstance(value, PlannedTrip):
            result = self._planned_trip_optimization_function(value)
        else:
            result = value
        logger.debug(f'Computed optimization function value and obtained "{result}" from "{value}".')
        return result

    def _result_optimization_function(self, result: Result) -> Tuple[float, ...]:
        return self._planning_optimization_function(result.planning)

    def _planning_optimization_function(self, planning: Planning) -> Tuple[float, ...]:
        return reduce(
            lambda a, b: tuple(map(add, a, b)),
            (self._route_optimization_function(route) for route in planning.routes),
            tuple(0 for _ in range(self.dimension_count)),
        )

    def _route_optimization_function(self, route: Route) -> Tuple[float, ...]:
        return reduce(
            lambda a, b: tuple(map(add, a, b)),
            (self._stop_optimization_function(stop) for stop in route.stops),
            tuple(0 for _ in range(self.dimension_count)),
        )

    def _stop_optimization_function(self, stop: Stop) -> Tuple[float, ...]:
        return reduce(
            lambda a, b: tuple(map(add, a, b)),
            (self._planned_trip_optimization_function(planned_trip) for planned_trip in stop.pickups),
            tuple(0 for _ in range(self.dimension_count)),
        )

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> Tuple[float, ...]:
        raise NotImplementedError


class DialARideObjective(Objective):

    def __init__(self):
        super().__init__(
            name='Dial-a-Ride',
            dimension_count=2,
        )

    def _route_optimization_function(self, route: Route) -> Tuple[float, ...]:
        scoring = 0.0
        for stop in route.stops:
            scoring -= stop.distance
        return len(tuple(route.trips)), scoring

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> Tuple[float, ...]:
        scoring = 0.0
        current = planned_trip.delivery
        while current != planned_trip.pickup and current.previous is not None:
            scoring -= current.distance
            current = current.previous
        return 1, scoring


class TaxiSharingObjective(Objective):

    def __init__(self):
        super().__init__(
            name='Taxi-Sharing',
            dimension_count=1,
        )

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> Tuple[float, ...]:
        if planned_trip.capacity == 0:
            return 0.0,
        return planned_trip.duration,


class HashCodeObjective(Objective):
    def __init__(self):
        super().__init__(
            name='HashCode-2018',
            dimension_count=1,
        )

    def _planned_trip_optimization_function(self, planned_trip: PlannedTrip) -> Tuple[float, ...]:
        if planned_trip.capacity == 0:
            return 0.0,
        trip = planned_trip.trip
        scoring = trip.distance
        if trip.origin_earliest == planned_trip.pickup_time:
            scoring += trip.on_time_bonus
        return scoring,
