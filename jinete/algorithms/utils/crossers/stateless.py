from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from itertools import product

from .abc import (
    Crosser,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Optional
    )
    from ....models import (
        PlannedTrip,
        Trip,
        Route,
    )

logger = logging.getLogger(__name__)


class StatelessCrosser(Crosser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iterator = self.feasible_iterator()

    def update_iterator(self):
        self.iterator = self.feasible_iterator()

    def feasible_iterator(self):
        for route, trip in product(self.attractive_routes, self.pending_trips):
            logger.debug(f'Yielding ({route}, {trip})...')
            planned_trip = route.feasible_trip(trip)
            if planned_trip is None:
                continue
            yield planned_trip

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        return next(self.iterator, None)

    @property
    def attractive_routes(self) -> Set[Route]:
        routes = set(route for route in self.routes if len(route.planned_trips) > 0)
        empty_route = next((route for route in self.routes if len(route.planned_trips) == 0), None)
        if empty_route is not None:
            routes.add(empty_route)
        return routes

    def mark_trip_as_done(self, trip: Trip):
        super().mark_trip_as_done(trip)
        self.update_iterator()
