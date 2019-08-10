from __future__ import annotations

import logging
from itertools import islice
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
        Iterable,
        Set,
    )
    from ....models import (
        PlannedTrip,
        Trip,
        Route,
    )

logger = logging.getLogger(__name__)


class OrderedCrosser(Crosser):
    ranking: Dict[UUID, OrderedDict[UUID, PlannedTrip]]

    def __init__(self, neighborhood_max_size: int = 250, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.neighborhood_max_size = min(neighborhood_max_size, len(self.trips))
        self.ranking = dict()
        self.initialize_ranking()

    def initialize_ranking(self) -> None:
        logger.info("Initializing ranking...")
        for route in self.routes:
            self.ranking[route.uuid] = self.create_sub_ranking(route)
            logger.info(f"Added sub ranking! Currently {len(self.ranking)}.")

    def create_sub_ranking(self, route: Route) -> OrderedDict[UUID, PlannedTrip]:
        logger.debug("Creating sub_ranking...")
        raw_sub_ranking = list()
        for trip in islice(self.pending_trips, self.neighborhood_max_size):
            planned_trip = route.feasible_trip(trip)
            if planned_trip is None:
                continue
            raw_sub_ranking.append((trip.uuid, planned_trip))
        raw_sub_ranking.sort(key=lambda x: x[1])
        return OrderedDict(raw_sub_ranking)

    def update_ranking(self, planned_trip: PlannedTrip) -> None:
        logger.info("Updating ranking...")
        for route_uuid in self.ranking:
            self.ranking[route_uuid].pop(planned_trip.trip_uuid, None)
        self.ranking[planned_trip.route_uuid] = self.create_sub_ranking(planned_trip.route)

    def mark_planned_trip_as_done(self, planned_trip: PlannedTrip):
        super().mark_planned_trip_as_done(planned_trip)
        self.update_ranking(planned_trip)

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        if len(self.ranking) == 0:
            return None

        best = None
        for sub_ranking in self.ranking.values():
            if len(sub_ranking) == 0:
                continue
            current = next(iter(sub_ranking.values()))
            if best is None or current < best:
                best = current
        return best
