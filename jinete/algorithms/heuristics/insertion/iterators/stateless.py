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

from cached_property import (
    cached_property,
)

from .abc import (
    InsertionIterator,
)

if TYPE_CHECKING:
    from typing import Iterator
    from .....models import (
        Route,
        Trip,
    )

logger = logging.getLogger(__name__)


class StatelessInsertionIterator(InsertionIterator):
    @cached_property
    def iterator(self) -> Iterator[Route]:
        for route, trip in it.product(self._attractive_routes, self.pending_trips):
            logger.debug(f"Yielding ({route}, {trip})...")
            yield from self._strategy.compute(route, trip)

    def __next__(self) -> Route:
        return next(self.iterator)

    def _mark_trip_as_done(self, trip: Trip):
        super()._mark_trip_as_done(trip)
        self.flush()

    def flush(self):
        for key in ("iterator",):
            self.__dict__.pop(key, None)


class BestStatelessInsertionIterator(StatelessInsertionIterator):
    def __init__(self, randomized_size: int = 1, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.randomized_size = randomized_size
        self.random = Random(seed)

    def __next__(self) -> Route:
        candidates = self._criterion.nbest(self.randomized_size, *self.iterator)

        if not any(candidates):
            raise StopIteration

        best = self.random.choice(candidates)
        return best
