from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import itertools as it

from cached_property import (
    cached_property,
)

from .abc import (
    Crosser,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
        Iterator,
    )
    from ....models import (
        PlannedTrip,
        Trip,
    )

logger = logging.getLogger(__name__)


class StatelessCrosser(Crosser):

    def flush(self):
        for key in ('iterator',):
            self.__dict__.pop(key, None)

    @cached_property
    def iterator(self) -> Iterator[PlannedTrip]:
        for route, trip in it.product(self.attractive_routes, self.pending_trips):
            logger.debug(f'Yielding ({route}, {trip})...')
            planned_trip = self.conjecturer.compute_one(route, trip)
            yield planned_trip

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        return next(self.iterator, None)

    def mark_trip_as_done(self, trip: Trip):
        super().mark_trip_as_done(trip)
        self.flush()
