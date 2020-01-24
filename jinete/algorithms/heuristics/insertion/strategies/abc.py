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

    def __init__(self, only_feasible: bool = True, *args, **kwargs):
        self.only_feasible = only_feasible

    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], previous_idx: int = None,
                following_idx: int = None, only_feasible: bool = None, *args, **kwargs) -> List[Route]:
        assert (previous_idx is not None and following_idx is not None)

        if only_feasible is None:
            only_feasible = self.only_feasible

        if isinstance(trips, Trip):
            trips = [trips]

        routes = (self._compute_one(route, trip, previous_idx, following_idx, *args, **kwargs) for trip in trips)
        routes = [r for r in routes if not only_feasible or r.feasible]
        return routes

    def _compute_one(self, route: Route, trip: Trip, previous_idx: int, following_idx: int, *args, **kwargs) -> Route:

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
