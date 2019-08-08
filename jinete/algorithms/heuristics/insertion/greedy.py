from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ....models import (
    Planning,
)
from ...abc import (
    Algorithm,
)
from ...utils import (
    Crosser,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class GreedyAlgorithm(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crosser_cls = Crosser

    def build_crosser(self) -> Crosser:
        return self.crosser_cls(self.fleet, self.job)

    def optimize(self) -> Planning:
        logger.info('Optimizing...')
        crosser = self.build_crosser()

        while not crosser.completed:
            planned_trip = crosser.get_best()
            if not planned_trip:
                break
            route = planned_trip.route
            route.append_planned_trip(planned_trip)
            crosser.mark_planned_trip_as_done(planned_trip.trip)

        for route in crosser.routes:
            route.finish()
        planning = Planning(crosser.routes)
        logger.info('Optimized!')
        return planning
