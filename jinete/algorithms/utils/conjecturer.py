from __future__ import annotations

import logging
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
)

from ...models import (
    Route,
    Stop,
    PlannedTrip,
)

if TYPE_CHECKING:
    from typing import (
        Iterable,
        List,
    )
    from ...models import (
        Trip,
    )

logger = logging.getLogger(__name__)


class Conjecturer(object):

    @staticmethod
    def conjecture_trip(route: Route, trip: Trip, previous_idx: int = None, following_idx: int = None) -> Route:
        assert following_idx is None or (previous_idx is not None and following_idx is not None)

        if previous_idx is None:
            previous_idx = - 2
        if following_idx is None:
            following_idx = - 1

        vehicle = route.vehicle
        route = deepcopy(route)

        previous_pickup = route.stops[previous_idx]
        pickup = Stop(vehicle, trip.origin_position, previous_pickup)
        if previous_idx + 1 == following_idx:
            previous_delivery = pickup
        else:
            previous_delivery = route.stops[following_idx - 1]

        delivery = Stop(vehicle, trip.destination_position, previous_delivery)
        planned_trip = PlannedTrip(vehicle=vehicle, trip=trip, pickup=pickup, delivery=delivery)
        route.append_planned_trip(planned_trip)
        return route

    def intensive_conjecture_trip(self, route: Route, trip: Trip) -> List[Route]:
        routes = list()
        for i in range(len(route.stops) - 1):
            for j in range(i + 1, len(route.stops)):
                conjectured_route = self.conjecture_trip(route, trip, i, j)
                routes.append(conjectured_route)
        return routes

    def sampling_conjecture_trip(self, route: Route, trip: Trip, count: int = 25) -> List[Route]:
        from random import randint

        indices = set()
        for _ in range(count):
            sampled_i = randint(0, len(route.stops) - 2)
            sampled_j = randint(sampled_i + 1, len(route.stops) - 1)
            pair = (sampled_i, sampled_j)
            indices.add(pair)

        planned_trips = list()
        for i, j in indices:
            planned_trip = self.conjecture_trip(route, trip, i, j)
            planned_trips.append(planned_trip)
        return planned_trips

    def conjecture_trip_in_batch(self, route: Route, iterable: Iterable[Trip], *args, **kwargs) -> List[Route]:
        # return sum((self.sampling_conjecture_trip(route, trip) for trip in iterable), [])
        return sum((self.intensive_conjecture_trip(route, trip) for trip in iterable), [])
        # return [self.conjecture_trip(route, trip) for trip in iterable]
