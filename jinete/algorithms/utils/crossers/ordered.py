from __future__ import annotations

import logging
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
    )
    from ....models import (
        PlannedTrip,
        Trip,
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
        return ranking

    def create_sub_ranking(self, route):
        logger.info("Creating sub_ranking...")
        sub_ranking = list()
        for trip in self.pending_trips:
            planned_trip = route.feasible_trip(trip)
            if planned_trip is None:
                continue
            sub_ranking.append((trip.uuid, planned_trip))
        return OrderedDict(sorted(sub_ranking, key=lambda x: x[1].scoring))

    def update_ranking(self, planned_trip: PlannedTrip):
        logger.info("Updating ranking...")

        for route_uuid in self.ranking:
            self.ranking[route_uuid].pop(planned_trip.trip.uuid, None)

        route = planned_trip.route
        self.ranking[route.uuid] = self.update_sub_ranking(route)

    def update_sub_ranking(self, route):
        sub_ranking = self.ranking[route.uuid]
        raw_sub_ranking = (
            (trip_uuid, route.feasible_trip(planned_trip.trip))
            for trip_uuid, planned_trip in sub_ranking.items()
            if route.feasible_trip(planned_trip.trip) is not None
        )
        return OrderedDict(sorted(raw_sub_ranking, key=lambda x: x[1].scoring))

    def mark_planned_trip_as_done(self, planned_trip: PlannedTrip):
        super().mark_planned_trip_as_done(planned_trip)
        self.update_ranking(planned_trip)

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        if not self.ranking:
            return None

        sub_ranking = min(self.ranking.values(), key=lambda x: self.ordered_route_scorer(x))
        if not sub_ranking:
            return None
        best_planned_trip = next(iter(sub_ranking.values()))

        return best_planned_trip

    @staticmethod
    def ordered_route_scorer(x: OrderedDict[Trip, PlannedTrip]):
        if not x:
            return maxsize
        return next(iter(x.values())).scoring
