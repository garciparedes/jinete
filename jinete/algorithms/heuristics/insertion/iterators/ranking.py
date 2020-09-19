from __future__ import (
    annotations,
)

import itertools as it
import logging
from random import (
    Random,
)
from typing import (
    TYPE_CHECKING,
)

from .abc import (
    InsertionIterator,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        List,
    )
    from .....models import PlannedTrip, Route, Vehicle

logger = logging.getLogger(__name__)


class RankingInsertionIterator(InsertionIterator):
    ranking: Dict[Vehicle, List[Route]]

    def __init__(self, neighborhood_max_size: int = 24, randomized_size: int = 1, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if neighborhood_max_size is None:
            neighborhood_max_size = len(self._trips)

        self.neighborhood_max_size = min(neighborhood_max_size, len(self._trips))

        self.randomized_size = randomized_size
        self.random = Random(seed)

        self.ranking = dict()
        self._initialize_ranking()

    def _initialize_ranking(self) -> None:
        logger.info("Initializing ranking...")
        for route in self._attractive_routes:
            self.ranking[route.vehicle] = self._create_sub_ranking(route)
            logger.info(f"Added sub ranking! Currently {len(self.ranking)}.")

    def _mark_planned_trip_as_done(self, planned_trip: PlannedTrip) -> None:
        super()._mark_planned_trip_as_done(planned_trip)
        self._update_ranking(planned_trip)

    def _update_ranking(self, planned_trip: PlannedTrip) -> None:
        logger.debug(f'Updating all rankings due to planned trip with "{planned_trip.trip_identifier}" trip...')
        for route in self._attractive_routes:
            self._update_vehicle_ranking(planned_trip, route.vehicle)

    def _update_vehicle_ranking(self, planned_trip: PlannedTrip, vehicle: Vehicle):
        logger.debug(f'Updating ranking for vehicle with "{vehicle.identifier}" identifier...')
        if vehicle is planned_trip.vehicle or vehicle not in self.ranking:
            self.ranking[vehicle] = self._create_sub_ranking(self.routes_container[vehicle])
        else:
            self.ranking[vehicle] = [route for route in self.ranking[vehicle] if planned_trip.trip not in route.trips]

    def _create_sub_ranking(self, route: Route) -> List[Route]:
        logger.debug(f'Creating sub_ranking for vehicle "{route.vehicle_identifier}"...')
        pending_trips = it.islice(self.pending_trips, self.neighborhood_max_size)

        raw_sub_ranking = self._strategy.compute(route, pending_trips)

        self._criterion.sorted(raw_sub_ranking, inplace=True)

        return raw_sub_ranking

    def __next__(self) -> Route:
        if not any(self.ranking):
            raise StopIteration

        candidates = list()
        for sub_ranking in self.ranking.values():
            if not any(sub_ranking):
                continue

            for current in sub_ranking:
                if (
                    len(candidates) == self.randomized_size
                    and self._criterion.best(candidates[-1], current) == candidates[-1]
                ):
                    break

                if self.randomized_size <= len(candidates):
                    candidates.pop()

                candidates.append(current)

            self._criterion.sorted(candidates, inplace=True)

        if not any(candidates):
            raise StopIteration

        best = self.random.choice(candidates)
        return best
