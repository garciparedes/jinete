from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from jinete.models import (
    Planning,
)
from jinete.algorithms.abc import (
    Algorithm,
)
from jinete.algorithms.utils import (
    BestStatelessCrosser,
)
from jinete.exceptions import (
    NonFeasiblePlannedTripFoundException,
)

if TYPE_CHECKING:
    from typing import (
        Type,
    )
    from jinete.algorithms.utils import (
        Crosser,
    )

logger = logging.getLogger(__name__)


class InsertionAlgorithm(Algorithm):

    def __init__(self, crosser_cls: Type[Crosser] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if crosser_cls is None:
            crosser_cls = BestStatelessCrosser
        self.crosser_cls = crosser_cls

    def build_crosser(self) -> Crosser:
        return self.crosser_cls(self.fleet, self.job)

    def optimize(self) -> Planning:
        logger.info('Optimizing...')
        crosser = self.build_crosser()

        while not crosser.completed:
            try:
                planned_trip = next(crosser)
            except NonFeasiblePlannedTripFoundException:
                break
            route = planned_trip.route
            route.append_planned_trip(planned_trip)
            crosser.mark_planned_trip_as_done(planned_trip)

        for route in crosser.routes:
            route.finish()
        planning = Planning(crosser.routes)
        logger.info('Optimized!')
        return planning
