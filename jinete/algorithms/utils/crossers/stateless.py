from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import itertools as it

from cached_property import (
    cached_property,
)

from ..conjecturer import (
    Conjecturer,
)
from .abc import (
    Crosser,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Optional,
        Iterator,
    )
    from ....models import (
        PlannedTrip,
        Trip,
        Route,
    )

logger = logging.getLogger(__name__)


class StatelessCrosser(Crosser):

    def flush(self):
        for key in ('iterator',):
            self.__dict__.pop(key, None)

    @cached_property
    def iterator(self) -> Iterator[PlannedTrip]:
        conjecturer = Conjecturer()
        for route, trip in it.product(self.attractive_routes, self.pending_trips):
            logger.debug(f'Yielding ({route}, {trip})...')
            planned_trip = conjecturer.conjecture_trip(route, trip)
            yield planned_trip

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        return next(self.iterator, None)

    @property
    def attractive_routes(self) -> Set[Route]:
        routes = set(route for route in self.routes if any(route.planned_trips))
        empty_route = next((route for route in self.routes if not any(route.planned_trips)), None)
        if empty_route is not None:
            routes.add(empty_route)
        return routes

    def mark_trip_as_done(self, trip: Trip):
        super().mark_trip_as_done(trip)
        self.flush()
