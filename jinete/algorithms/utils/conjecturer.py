from __future__ import annotations

import logging
from copy import deepcopy
from random import Random
from typing import (
    TYPE_CHECKING,
    Union)

from ...models import (
    Route,
    Stop,
    PlannedTrip,
    Trip,
)

if TYPE_CHECKING:
    from typing import (
        Iterable,
        List,
    )

logger = logging.getLogger(__name__)


class Conjecturer(object):

    def __init__(self, *args, **kwargs):
        pass

    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], *args, **kwargs) -> List[Route]:
        if not isinstance(trips, Trip):
            return sum((self.compute(route, trip, *args, **kwargs) for trip in trips), [])
        trip = trips

        return [self.compute_one(route, trip, *args, **kwargs)]

    @staticmethod
    def compute_one(route: Route, trip: Trip, previous_idx: int = None, following_idx: int = None) -> Route:
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


class IntensiveConjecturer(Conjecturer):

    def compute(self, route: Route, trips: Trip, *args, **kwargs) -> List[Route]:
        if not isinstance(trips, Trip):
            return super().compute(route, trips, *args, **kwargs)
        trip = trips

        routes = list()
        for i in range(len(route.stops) - 1):
            for j in range(i + 1, len(route.stops)):
                conjectured_route = self.compute_one(route, trip, i, j)
                routes.append(conjectured_route)
        return routes


class SamplingConjecturer(Conjecturer):
    def __init__(self, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random = Random(seed)

    def compute(self, route: Route, trips: Trip, count: int = 25, *args, **kwargs) -> List[Route]:
        if not isinstance(trips, Trip):
            return super().compute(route, trips, *args, **kwargs)
        trip = trips

        indices = set()
        for _ in range(count):
            sampled_i = self.random.randint(0, len(route.stops) - 2)
            sampled_j = self.random.randint(sampled_i + 1, len(route.stops) - 1)
            pair = (sampled_i, sampled_j)
            indices.add(pair)

        planned_trips = list()
        for i, j in indices:
            planned_trip = self.compute_one(route, trip, i, j)
            planned_trips.append(planned_trip)
        return planned_trips