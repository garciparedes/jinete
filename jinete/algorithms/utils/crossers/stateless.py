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
        Route,
        Trip,
    )

logger = logging.getLogger(__name__)


class StatelessCrosser(Crosser):

    def __next__(self) -> Optional[Route]:
        return next(self.iterator)

    @cached_property
    def iterator(self) -> Iterator[Route]:
        for route, trip in it.product(self.attractive_routes, self.pending_trips):
            logger.debug(f'Yielding ({route}, {trip})...')
            planned_trip = self.conjecturer.compute_one(route, trip)
            yield planned_trip

    def mark_trip_as_done(self, trip: Trip):
        super().mark_trip_as_done(trip)
        self.flush()

    def flush(self):
        for key in ('iterator',):
            self.__dict__.pop(key, None)


class BestStatelessCrosser(StatelessCrosser):

    def __next__(self) -> Optional[Route]:
        best = self.criterion.best(*self.iterator)
        if best is None:
            raise StopIteration
        return best
