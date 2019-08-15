from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .stateless import (
    StatelessCrosser,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
    )
    from ....models import (
        PlannedTrip,
    )

logger = logging.getLogger(__name__)


class BestStatelessCrosser(StatelessCrosser):

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        best = self.criterion.best(*self.iterator)
        return best
