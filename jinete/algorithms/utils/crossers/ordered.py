from __future__ import annotations

import logging
from heapq import nsmallest
from sys import maxsize
from typing import TYPE_CHECKING
from collections import OrderedDict
from uuid import UUID

from .abc import (
    Crosser,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
        Dict,
        Iterable
    )
    from ....models import (
        PlannedTrip,
        Trip,
        Route,
    )

logger = logging.getLogger(__name__)


class OrderedCrosser(Crosser):
    ranking: Dict[UUID, OrderedDict[UUID, PlannedTrip]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ranking = self.initialize_ranking()
        pass

    def initialize_ranking(self) -> Dict[UUID, OrderedDict[UUID, PlannedTrip]]:
        logger.info("Initializing ranking...")
        ranking = dict()
        for route in self.routes:
            ranking[route.uuid] = self.create_sub_ranking(route)
            logger.info(f"Added sub ranking! Currently {len(ranking)}.")

        return ranking

    def create_sub_ranking(self, route):
        logger.debug("Creating sub_ranking...")
        return self.recalcule(route, self.pending_trips)

    def update_ranking(self, planned_trip: PlannedTrip):
        logger.info("Updating ranking...")

        for route_uuid in self.ranking:
            self.ranking[route_uuid].pop(planned_trip.trip.uuid, None)

        route = planned_trip.route
        self.ranking[route.uuid] = self.update_sub_ranking(route)

    def update_sub_ranking(self, route):
        trips = (
            planned_trip.trip
            for planned_trip in self.ranking[route.uuid].values()
        )

        return self.recalcule(route, trips)

    def recalcule(self, route: Route, trips: Iterable[Trip], k: int = 500):
        raw_sub_ranking = (
            route.feasible_trip(trip)
            for trip in self.kth_smallest(trips, k)
        )
        raw_sub_ranking = (
            planned_trip
            for planned_trip in raw_sub_ranking
            if planned_trip is not None
        )
        raw_sub_ranking = (
            (planned_trip.trip_uuid, planned_trip)
            for planned_trip in self.kth_sort(raw_sub_ranking)
        )
        return OrderedDict(raw_sub_ranking)

    def kth_smallest(self, trips: Iterable[Trip], k: int):
        trips = set(nsmallest(k, trips))
        try:
            p = iter(self.pending_trips)
            while len(trips) < k:
                trips.add(next(p))
        except StopIteration:
            pass
        return trips

    def kth_sort(self, arr: Iterable[PlannedTrip], k=None) -> Iterable:
        return sorted(arr)

    def mark_planned_trip_as_done(self, planned_trip: PlannedTrip):
        super().mark_planned_trip_as_done(planned_trip)
        self.update_ranking(planned_trip)

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        if not self.ranking:
            return None
        sub_ranking = (
            sequence for sequence in self.ranking.values() if len(sequence) > 0
        )
        sub_ranking = (
            next(iter(sub_sequence.values())) for sub_sequence in sub_ranking
        )
        best_planned_trip = min(sub_ranking, default=None)
        if not sub_ranking:
            return None
        return best_planned_trip

    @staticmethod
    def ordered_route_scorer(x: OrderedDict[Trip, PlannedTrip]):
        if not x:
            return maxsize
        return next(iter(x.values())).scoring
