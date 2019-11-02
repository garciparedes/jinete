from __future__ import annotations

import logging
import itertools as it
from typing import TYPE_CHECKING, List
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
        Vehicle
    )

logger = logging.getLogger(__name__)


class OrderedCrosser(Crosser):
    ranking: Dict[Vehicle, List[Route]]

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
            self.ranking[route.vehicle] = self.create_sub_ranking(route)
            logger.info(f"Added sub ranking! Currently {len(self.ranking)}.")

    def create_sub_ranking(self, route: Route) -> List[Route]:
        logger.debug("Creating sub_ranking...")
        pending_trips = it.islice(self.pending_trips, self.neighborhood_max_size)
        raw_sub_ranking = route.conjecture_trip_in_batch(pending_trips)

        self.criterion.sorted(raw_sub_ranking, inplace=True)
        return raw_sub_ranking
        # return OrderedDict((item.trip, item) for item in raw_sub_ranking)

    def update_ranking(self, trip: Trip) -> None:
        logger.info("Updating ranking...")
        # for route in self.ranking:
        #     if route == planned_trip.route:
        #         continue
        #     self.ranking[route] = list(pt for pt in self.ranking[route] if not pt.trip == planned_trip.trip)
        # self.ranking[planned_trip.route] = self.create_sub_ranking(planned_trip.route)
        for route in self.routes:
            self.ranking[route.vehicle] = self.create_sub_ranking(route)

    def mark_trip_as_done(self, trip: Trip) -> None:
        super().mark_trip_as_done(trip)
        self.update_ranking(trip)

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        if len(self.ranking) == 0:
            return None

        best = None
        for sub_ranking in self.ranking.values():
            if len(sub_ranking) == 0:
                continue
            current = sub_ranking.pop(0)
            if not current.feasible:
                continue
            best = self.criterion.best(best, current)
        return best
