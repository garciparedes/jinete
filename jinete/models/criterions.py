from __future__ import (
    annotations,
)

import logging
from abc import (
    ABC,
    abstractmethod,
)
from statistics import (
    mean,
)
from typing import (
    TYPE_CHECKING,
)

from .constants import (
    MAX_FLOAT,
    MIN_FLOAT,
    OptimizationDirection,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
        List,
        Iterable,
    )
    from .routes import Route

logger = logging.getLogger(__name__)


class RouteCriterion(ABC):
    def __init__(self, name: str, direction: OptimizationDirection, *args, **kwargs):
        self.name = name
        self.direction = direction

    @abstractmethod
    def scoring(self, route: Route) -> float:
        pass

    def best(self, *args: Optional[Route]) -> Route:
        return self.direction((arg for arg in args if arg is not None), key=self.scoring, default=None,)

    def sorted(self, routes: Iterable[Route], inplace: bool = False) -> List[Route]:
        return self.direction.sorted(routes, key=self.scoring, inplace=inplace)

    def nbest(self, n: int, routes: Iterable[Route], inplace: bool = False) -> List[Route]:
        return self.direction.nbest(n, routes, key=self.scoring, inplace=inplace)


class EarliestLastDepartureTimeRouteCriterion(RouteCriterion):
    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MINIMIZATION, name="Shortest-Time", *args, **kwargs,
        )

    def scoring(self, route: Route) -> float:
        if not route.feasible:
            return MAX_FLOAT

        return route.last_departure_time


class ShortestAveragePlannerTripDurationCriterion(RouteCriterion):
    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MINIMIZATION, name="Shortest-Time", *args, **kwargs,
        )

    def scoring(self, route: Route) -> float:
        if not route.feasible:
            return MAX_FLOAT

        if not any(route.planned_trips):
            return 0

        return mean(planned_trip.duration for planned_trip in route.planned_trips)


class ShortestTimeRouteCriterion(RouteCriterion):
    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MINIMIZATION, name="Shortest-Time", *args, **kwargs,
        )

    def scoring(self, route: Route) -> float:
        if not route.feasible:
            return MAX_FLOAT

        return route.duration


class LongestTimeRouteCriterion(RouteCriterion):
    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MAXIMIZATION, name="Longest-Time", *args, **kwargs,
        )

    def scoring(self, route: Route) -> float:
        if not route.feasible:
            return MIN_FLOAT

        return route.duration


class LongestUtilTimeRouteCriterion(RouteCriterion):
    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MAXIMIZATION, name="Longest-Util-Time", *args, **kwargs,
        )

    def scoring(self, route: Route) -> float:
        if not route.feasible:
            return MIN_FLOAT

        scoring = 0.0
        for trip in route.trips:
            scoring += trip.distance
        return scoring


class HashCodeRouteCriterion(RouteCriterion):
    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MAXIMIZATION, name="Longest-Time", *args, **kwargs,
        )

    def scoring(self, route: Route) -> float:
        if not route.feasible:
            return MIN_FLOAT

        scoring = 0.0
        for planned_trip in route.planned_trips:
            scoring += planned_trip.distance
            if planned_trip.pickup_time == planned_trip.trip.origin_earliest:
                scoring += planned_trip.trip.on_time_bonus
        return scoring
