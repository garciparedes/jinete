from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from itertools import product

from ...models import (
    Fleet,
    Job,
    Route,
    Trip,
)

if TYPE_CHECKING:
    from typing import (
        Set,
    )

logger = logging.getLogger(__name__)


class Crosser(object):

    def __init__(self, fleet: Fleet, job: Job):
        self.routes = set(Route(vehicle) for vehicle in fleet.vehicles)
        self.trips = job.trips
        self.done_trips = set()

    def __iter__(self):
        for route, trip in (product(self.attractive_routes, self.pending_trips)):
            if self.completed:
                break
            logger.debug(f'Yielding ({route}, {trip})...')
            yield route, trip
        return None

    @property
    def attractive_routes(self) -> Set[Route]:
        routes = set(route for route in self.routes if len(route.planned_trips) > 0)
        empty_route = next((route for route in self.routes if len(route.planned_trips) == 0), None)
        if empty_route is not None:
            routes.add(empty_route)
        return routes

    def mark_as_done(self, trip: Trip):
        self.done_trips.add(trip)

    def mark_as_undone(self, trip: Trip):
        self.done_trips.remove(trip)

    @property
    def pending_trips(self):
        return self.trips - self.done_trips

    @property
    def completed(self) -> bool:
        return len(self.pending_trips) == 0

    def update_ranking(self):
        ranking = list()
        for route, trip in self:
            planned_trip = route.feasible_trip(trip)
            if planned_trip is None:
                continue
            ranking.append(planned_trip)
        ranking.sort(key=lambda pt: pt.scoring)

    def get_best(self):
        best_planned_trip = None
        for route, trip in self:
            planned_trip = route.feasible_trip(trip)
            if planned_trip is None:
                continue

            if best_planned_trip is None or planned_trip.scoring < best_planned_trip.scoring:
                best_planned_trip = planned_trip

        return best_planned_trip
