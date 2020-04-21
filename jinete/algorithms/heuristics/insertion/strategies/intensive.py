from __future__ import (
    annotations,
)

import itertools as it
import logging
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
    from .....models import Route

logger = logging.getLogger(__name__)


class IntensiveInsertionStrategy(InsertionStrategy):
    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], *args, **kwargs) -> List[Route]:
        if not isinstance(trips, Trip):
            trips = tuple(trips)
        routes = list()
        for i, j in it.combinations(range(len(route.stops)), 2):
            routes += super().compute(route, trips, i, j, *args, **kwargs)
        return routes
