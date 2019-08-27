from __future__ import annotations

import logging
import itertools as it
from typing import TYPE_CHECKING
from collections import OrderedDict

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
        Route,
        Trip,
    )

logger = logging.getLogger(__name__)


class OrderedCrosser(Crosser):
    ranking: Dict[Route, OrderedDict[Trip, PlannedTrip]]

    def __init__(self, neighborhood_max_size: int = 250, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if neighborhood_max_size is None:
            neighborhood_max_size = len(self.trips)
        else:
            neighborhood_max_size = min(neighborhood_max_size, len(self.trips))

        self.neighborhood_max_size = neighborhood_max_size
        self.ranking = dict()
        self.initialize_ranking()

    def initialize_ranking(self) -> None:
        logger.info("Initializing ranking...")
        for route in self.routes:
            self.ranking[route] = self.create_sub_ranking(route)
            logger.info(f"Added sub ranking! Currently {len(self.ranking)}.")

    def create_sub_ranking(self, route: Route) -> OrderedDict[Trip, PlannedTrip]:
        logger.debug("Creating sub_ranking...")
        raw_sub_ranking = route.conjecture_trip_in_batch(it.islice(self.pending_trips, self.neighborhood_max_size))

        self.criterion.sorted(raw_sub_ranking, inplace=True)
        return OrderedDict((item.trip, item) for item in raw_sub_ranking)

    def update_ranking(self, planned_trip: PlannedTrip) -> None:
        logger.info("Updating ranking...")
        for route in self.ranking:
            self.ranking[route].pop(planned_trip.trip, None)
        self.ranking[planned_trip.route] = self.create_sub_ranking(planned_trip.route)

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
            if not current.feasible:
                continue
            best = self.criterion.best(best, current)
        return best
