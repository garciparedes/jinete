from __future__ import annotations

import logging
from random import Random
from typing import (
    TYPE_CHECKING,
)
from .....models import (
    Trip,
)
from .abc import (
    InsertionStrategy,
)

if TYPE_CHECKING:
    from typing import (
        Iterable,
        List,
        Union,
    )
    from .....models import (
        Route,
    )

logger = logging.getLogger(__name__)


class SamplingInsertionStrategy(InsertionStrategy):
    def __init__(self, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random = Random(seed)

    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], count: int = 25,
                *args, **kwargs) -> List[Route]:
        if not isinstance(trips, Trip):
            return super().compute(route, trips, *args, **kwargs)
        trip = trips

        indices = set()
        for _ in range(count):
            sampled_i = self.random.randint(0, len(route.stops) - 2)
            sampled_j = self.random.randint(sampled_i + 1, len(route.stops) - 1)
            pair = (sampled_i, sampled_j)
            indices.add(pair)

        planned_trips = list()
        for i, j in indices:
            planned_trip = self.compute_one(route, trip, i, j)
            planned_trips.append(planned_trip)
        return planned_trips
