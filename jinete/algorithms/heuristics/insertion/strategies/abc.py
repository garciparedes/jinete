from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)

from .....models import (
    Stop,
    PlannedTrip,
    Trip,
    RouteCloner,
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

        i = max(idx, 1)
        while i < len(route.stops):
            stop = route.stops[i]
            planned_trip = max(
                (pt for pt in stop.pickups if pt.duration > pt.timeout),
                default=None,
                key=lambda pt: (pt.delivery_time - pt.timeout)
            )
            if planned_trip is None:
                i += 1
                continue

            value = planned_trip.delivery_time - planned_trip.timeout

            if stop.starting_time >= value:
                i += 1
                continue

            stop.starting_time = value

            for s in route.stops[i:]:
                s.flush()

            route.flush()
            if route.feasible:
                return

            max_idx = route.stops.index(planned_trip.delivery)

            stops = route.stops[i + 1:max_idx - 1]
            iterable = (min((route.stops.index(s2.pickup) for s2 in s.deliveries), default=9999) for s in stops)
            i_candidate = min(iterable, default=9999)
            if i_candidate == 9999 or i_candidate <= i:
                i += 1
                continue
            i = i_candidate

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
