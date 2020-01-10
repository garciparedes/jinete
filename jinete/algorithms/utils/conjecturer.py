from __future__ import annotations

import logging
from random import Random
from typing import (
    TYPE_CHECKING,
)

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
        Union,
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


class IntensiveConjecturer(Conjecturer):

    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], *args, **kwargs) -> List[Route]:
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

    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], count: int = 25,
                *args, **kwargs) -> List[Route]:
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
