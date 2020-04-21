from __future__ import (
    annotations,
)

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


class TailInsertionStrategy(InsertionStrategy):
    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], *args, **kwargs) -> List[Route]:
        previous_idx = max(len(route.stops) - 2, 0)
        following_idx = max(len(route.stops) - 1, 0)
        return super().compute(route, trips, previous_idx, following_idx, *args, **kwargs)
