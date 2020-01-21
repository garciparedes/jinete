from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)

from .....models import (
    Stop,
    PlannedTrip,
    Trip,
)

if TYPE_CHECKING:
    from typing import (
        Iterable,
        List,
        Union,
    )
    from .....models import (
        Route,
    )

logger = logging.getLogger(__name__)


class InsertionStrategy(object):

    def __init__(self, *args, **kwargs):
        pass

    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], only_feasible: bool = True,
                *args, **kwargs) -> List[Route]:
        if not isinstance(trips, Trip):
            return sum((self.compute(route, trip, only_feasible=only_feasible, *args, **kwargs) for trip in trips), [])
        trip = trips

        planned_trip = self.compute_one(route, trip, *args, **kwargs)
        if only_feasible and not planned_trip.feasible:
            return []
        return [planned_trip]

    def compute_one(self, route: Route, trip: Trip, previous_idx: int = None, following_idx: int = None) -> Route:
        assert following_idx is None or (previous_idx is not None and following_idx is not None)

        if previous_idx is None:
            previous_idx = max(len(route.stops) - 2, 0)
        if following_idx is None:
            following_idx = max(len(route.stops) - 1, 0)

        route = route.clone(previous_idx + 1)

        pickup = self._build_pickup(route, trip, previous_idx)
        delivery = self._build_delivery(route, trip, previous_idx, following_idx, pickup)

        planned_trip = PlannedTrip(route.vehicle, trip, pickup, delivery)
        route.append_planned_trip(planned_trip)
        return route

    @staticmethod
    def _build_pickup(route: Route, trip: Trip, previous_idx: int) -> Stop:
        previous_pickup = route.stops[previous_idx]
        pickup = Stop(route.vehicle, trip.origin_position, previous_pickup)
        return pickup

    @staticmethod
    def _build_delivery(route: Route, trip: Trip, previous_idx: int, following_idx: int, pickup: Stop) -> Stop:
        previous_delivery = pickup if previous_idx + 1 == following_idx else route.stops[following_idx - 1]
        delivery = Stop(route.vehicle, trip.destination_position, previous_delivery)
        return delivery
