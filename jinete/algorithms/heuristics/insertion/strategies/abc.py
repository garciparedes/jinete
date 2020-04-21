from __future__ import (
    annotations,
)

import logging
from operator import (
    attrgetter,
)
from typing import (
    TYPE_CHECKING,
)

from .....models import (
    PlannedTrip,
    RouteCloner,
    Stop,
    Trip,
)

if TYPE_CHECKING:
    from typing import (
        Iterable,
        List,
        Union,
    )
    from .....models import Route

logger = logging.getLogger(__name__)


class InsertionStrategy(object):
    def __init__(self, only_feasible: bool = True, *args, **kwargs):
        self.only_feasible = only_feasible

    def compute(
        self,
        route: Route,
        trips: Union[Trip, Iterable[Trip]],
        previous_idx: int = None,
        following_idx: int = None,
        only_feasible: bool = None,
        *args,
        **kwargs
    ) -> List[Route]:
        assert previous_idx < following_idx

        if only_feasible is None:
            only_feasible = self.only_feasible

        if isinstance(trips, Trip):
            trips = [trips]

        routes = (self._compute_one(route, trip, previous_idx, following_idx, *args, **kwargs) for trip in trips)
        routes = [r for r in routes if not only_feasible or r.feasible]
        return routes

    def _compute_one(self, route: Route, trip: Trip, previous_idx: int, following_idx: int, *args, **kwargs) -> Route:
        cloner = RouteCloner(route, previous_idx + 1)
        route = cloner.clone()

        pickup = self._build_pickup(route, trip, previous_idx)
        delivery = self._build_delivery(route, trip, previous_idx, following_idx, pickup)

        planned_trip = PlannedTrip(route.vehicle, trip, pickup, delivery)
        route.append_planned_trip(planned_trip)

        self._improve_ride_times(route, cloner.idx)
        return route

    def _improve_ride_times(self, route: Route, idx: int) -> None:
        if route.stops[1].waiting_time != 0:
            route.stops[0].starting_time = route.stops[1].waiting_time
            route.stops[0].flush(), route.stops[1].flush()

        if route.feasible:
            return

        for i in reversed(range(max(idx, 1), len(route.stops))):
            stop = route.stops[i]
            planned_trip = max(stop.pickup_planned_trips, default=None, key=attrgetter("duration"))
            if planned_trip is None:
                continue

            stop.starting_time += max(planned_trip.duration - planned_trip.timeout, 0)

            for s in route.stops[i:]:
                s.flush()

        route.flush()
        if route.feasible:
            # print(f'feasible!')
            pass

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
