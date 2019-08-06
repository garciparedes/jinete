from __future__ import annotations

import logging
from itertools import product
from typing import Set, TYPE_CHECKING

from .abc import Algorithm
from ..models import (
    Route,
    Fleet,
    Job,
    Planning,
)

if TYPE_CHECKING:
    from ..models import (
        Trip,
    )

logger = logging.getLogger(__name__)


class Crosser(object):

    def __init__(self, fleet: Fleet, job: Job):
        self.routes = set(Route(vehicle) for vehicle in fleet.vehicles)
        self.trips = job.trips
        self.done_trips = set()

    def __iter__(self):
        for route, trip in (product(self.atractive_routes, self.pending_trips)):
            if self.completed:
                break
            logger.debug(f'Yielding ({route}, {trip})...')
            yield route, trip
        return None

    @property
    def atractive_routes(self) -> Set[Route]:
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


class GreedyAlgorithm(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crosser_cls = Crosser

    def build_crosser(self) -> Crosser:
        return self.crosser_cls(self.fleet, self.job)

    def optimize(self) -> Planning:
        logger.info('Optimizing...')
        crosser = self.build_crosser()

        while not crosser.completed:
            planned_trip = crosser.get_best()
            if not planned_trip:
                break
            route = planned_trip.route
            route.append_planned_trip(planned_trip)
            crosser.mark_as_done(planned_trip.trip)

        for route in crosser.routes:
            route.finish()
        planning = Planning(crosser.routes)
        logger.info('Optimized!')
        return planning
