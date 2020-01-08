from __future__ import annotations

import logging
import itertools as it
from typing import TYPE_CHECKING

from .abc import (
    Crosser,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
        Dict,
        List,
    )
    from ....models import (
        PlannedTrip,
        Route,
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
        for route in self.attractive_routes:
            self.ranking[route.vehicle] = self.create_sub_ranking(route)
            logger.info(f"Added sub ranking! Currently {len(self.ranking)}.")

    def mark_planned_trip_as_done(self, planned_trip: PlannedTrip) -> None:
        super().mark_planned_trip_as_done(planned_trip)
        self.update_ranking(planned_trip)

    def update_ranking(self, planned_trip: PlannedTrip) -> None:
        logger.debug(f'Updating all rankings due to planned trip with "{planned_trip.trip_identifier}" trip...')
        for route in self.attractive_routes:
            self._update_vehicle_ranking(planned_trip, route.vehicle)

    def _update_vehicle_ranking(self, planned_trip: PlannedTrip, vehicle: Vehicle):
        logger.debug(f'Updating ranking for vehicle with "{vehicle.identifier}" identifier...')
        if vehicle is planned_trip.vehicle or vehicle not in self.ranking:
            self.ranking[vehicle] = self.create_sub_ranking(self.routes_container[vehicle])
        else:
            self.ranking[vehicle] = [route for route in self.ranking[vehicle] if planned_trip.trip not in route.trips]

    def create_sub_ranking(self, route: Route) -> List[Route]:
        logger.debug(f'Creating sub_ranking for vehicle "{route.vehicle_identifier}"...')
        pending_trips = it.islice(self.pending_trips, self.neighborhood_max_size)

        raw_sub_ranking = self.conjecturer.compute(route, pending_trips)

        self.criterion.sorted(raw_sub_ranking, inplace=True)
        return raw_sub_ranking

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        if len(self.ranking) == 0:
            return None

        best = None
        for sub_ranking in self.ranking.values():
            if len(sub_ranking) == 0:
                continue
            current = sub_ranking[0]
            if not current.feasible:
                continue
            best = self.criterion.best(best, current)
        return best
