from __future__ import annotations

import logging
from heapq import nsmallest
from sys import maxsize
from typing import TYPE_CHECKING, Set, List
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

    def __init__(self, neighborhood_max_size: int = 500, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.neighborhood_max_size = neighborhood_max_size
        self.ranking = dict()
        self.initialize_ranking()

    def initialize_ranking(self) -> None:
        logger.info("Initializing ranking...")
        for route in self.routes:
            self.ranking[route.uuid] = self.create_sub_ranking(route)
            logger.info(f"Added sub ranking! Currently {len(self.ranking)}.")

    def create_sub_ranking(self, route):
        logger.debug("Creating sub_ranking...")
        raw_sub_ranking = (
            route.feasible_trip(trip)
            for trip in self.pending_trips
        )
        raw_sub_ranking = (
            planned_trip
            for planned_trip in raw_sub_ranking
            if planned_trip is not None
        )
        raw_sub_ranking = (
            (planned_trip.trip_uuid, planned_trip)
            for planned_trip in sorted(raw_sub_ranking)
        )
        return OrderedDict(raw_sub_ranking)

    def update_ranking(self, planned_trip: PlannedTrip):
        logger.info("Updating ranking...")
        for route_uuid in self.ranking:
            self.ranking[route_uuid].pop(planned_trip.trip_uuid, None)
        self.ranking[planned_trip.route_uuid] = self.create_sub_ranking(planned_trip.route)

    @property
    def pending_trips(self) -> Set[Trip]:
        pending_trips = super().pending_trips
        if self.neighborhood_max_size is None or len(pending_trips) < self.neighborhood_max_size:
            return pending_trips
        return set(nsmallest(self.neighborhood_max_size, pending_trips))

    def mark_planned_trip_as_done(self, planned_trip: PlannedTrip):
        super().mark_planned_trip_as_done(planned_trip)
        self.update_ranking(planned_trip)

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        if len(self.ranking) == 0:
            return None
        sub_ranking = (
            sequence for sequence in self.ranking.values() if len(sequence) > 0
        )
        sub_ranking = (
            next(iter(sub_sequence.values())) for sub_sequence in sub_ranking
        )
        best_planned_trip = min(sub_ranking, default=None)
        if best_planned_trip is None:
            return None
        return best_planned_trip
