from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .constants import (
    OptimizationDirection,
)

if TYPE_CHECKING:
    from typing import (
        Iterable,
        Optional,
        List,
    )
    from .planned_trips import (
        PlannedTrip,
    )


class PlannedTripCriterion(ABC):
    def __init__(self, name: str, direction: OptimizationDirection):
        self.name = name
        self.direction = direction

    @abstractmethod
    def scoring(self, planned_trip: PlannedTrip) -> float:
        pass

    def best(self, *args: PlannedTrip) -> Optional[PlannedTrip]:
        return self.direction.fn(
            (arg for arg in args if arg is not None),
            key=self.scoring,
            default=None,
        )

    def sorted(self, arr: List[PlannedTrip], inplace: bool = False) -> List[PlannedTrip]:
        if inplace:
            arr.sort(key=self.scoring)
        else:
            arr = sorted(arr, key=self.scoring)
        return arr


class ShortestTimePlannedTripCriterion(PlannedTripCriterion):

    def __init__(self):
        super().__init__(
            direction=OptimizationDirection.MAXIMIZATION,
            name='Shortest-Time',
        )

    def scoring(self, planned_trip: PlannedTrip) -> float:
        return planned_trip.collection_time - planned_trip.route.last_time
