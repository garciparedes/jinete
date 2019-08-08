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
    from jinete.models import (
        PlannedTrip,
    )

logger = logging.getLogger(__name__)


class BestStatelessCrosser(StatelessCrosser):

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        best_planned_trip = None
        for planned_trip in self.iterator:
            if best_planned_trip is None or planned_trip.scoring < best_planned_trip.scoring:
                best_planned_trip = planned_trip
        return best_planned_trip
