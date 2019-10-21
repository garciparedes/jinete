from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .constants import (
    OptimizationDirection,
    MIN_FLOAT,
    MAX_FLOAT,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
        List,
        Iterable,
    )
    from .planned_trips import (
        PlannedTrip,
    )

logger = logging.getLogger(__name__)


class PlannedTripCriterion(ABC):
    def __init__(self, name: str, direction: OptimizationDirection, *args, **kwargs):
        self.name = name
        self.direction = direction

    @abstractmethod
    def scoring(self, planned_trip: PlannedTrip) -> float:
        pass

    def best(self, *args: Optional[PlannedTrip]) -> PlannedTrip:
        return self.direction(
            (arg for arg in args if arg is not None),
            key=self.scoring,
            default=None,
        )

    def sorted(self, planned_trips: Iterable[PlannedTrip], inplace: bool = False) -> List[PlannedTrip]:
        return self.direction.sorted(planned_trips, key=self.scoring, inplace=inplace)

    def nbest(self, n: int, planned_trips: Iterable[PlannedTrip], inplace: bool = False):
        return self.direction.nbest(n, planned_trips, key=self.scoring, inplace=inplace)


class ShortestTimePlannedTripCriterion(PlannedTripCriterion):

    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MINIMIZATION,
            name='Shortest-Time',
            *args, **kwargs,
        )

    def scoring(self, planned_trip: PlannedTrip) -> float:
        if not planned_trip.feasible:
            return MAX_FLOAT

        return planned_trip.delivery_time - planned_trip.route.last_departure_time


class LongestTimePlannedTripCriterion(PlannedTripCriterion):

    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MAXIMIZATION,
            name='Longest-Time',
            *args, **kwargs,
        )

    def scoring(self, planned_trip: PlannedTrip) -> float:
        if not planned_trip.feasible:
            return MIN_FLOAT

        return planned_trip.delivery_time - planned_trip.route.last_departure_time


class LongestUtilTimePlannedTripCriterion(PlannedTripCriterion):

    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MAXIMIZATION,
            name='Longest-Time',
            *args, **kwargs,
        )

    def scoring(self, planned_trip: PlannedTrip) -> float:
        if not planned_trip.feasible:
            return MIN_FLOAT

        return planned_trip.duration - planned_trip.trip.origin_position.distance_to(planned_trip.route.last_position)


class HashCodePlannedTripCriterion(PlannedTripCriterion):

    def __init__(self, *args, **kwargs):
        super().__init__(
            direction=OptimizationDirection.MAXIMIZATION,
            name='Longest-Time',
            *args, **kwargs,
        )

    def scoring(self, planned_trip: PlannedTrip) -> float:
        if not planned_trip.feasible:
            return MIN_FLOAT

        scoring = planned_trip.distance
        if planned_trip.pickup_time == planned_trip.trip.origin_earliest:
            scoring += planned_trip.trip.on_time_bonus

        # TODO: Optimize this call
        scoring -= planned_trip.origin.distance_to(planned_trip.route.last_position)

        return scoring
