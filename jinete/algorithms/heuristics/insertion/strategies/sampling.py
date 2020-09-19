from __future__ import (
    annotations,
)

import logging
from random import (
    Random,
)
from typing import (
    TYPE_CHECKING,
)

from .....models import (
    Trip,
)
from .....utils import (
    sample_index_pairs,
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
    from .....models import Route

logger = logging.getLogger(__name__)


class SamplingInsertionStrategy(InsertionStrategy):
    def __init__(self, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random = Random(seed)

    def compute(
        self, route: Route, trips: Union[Trip, Iterable[Trip]], count: int = 128, *args, **kwargs
    ) -> List[Route]:
        if not isinstance(trips, Trip):
            trips = tuple(trips)

        routes = list()
        for i, j in sample_index_pairs(len(route.stops), count, self.random):
            routes += super().compute(route, trips, i, j, *args, **kwargs)
        return routes
