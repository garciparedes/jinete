from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...models import (
    Planning,
)
from ...exceptions import (
    StopPlannedTripIterationException,
)
from ..abc import (
    Algorithm,
)
from ..utils import (
    OrderedCrosser,
)

if TYPE_CHECKING:
    from typing import (
        Type,
    )
    from ..utils import (
        Crosser,
    )

logger = logging.getLogger(__name__)


class InsertionAlgorithm(Algorithm):

    def __init__(self, crosser_cls: Type[Crosser] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if crosser_cls is None:
            crosser_cls = OrderedCrosser
        self.crosser_cls = crosser_cls
        self.args = args
        self.kwargs = kwargs

    def build_crosser(self) -> Crosser:
        return self.crosser_cls(*self.args, **self.kwargs)

    def _optimize(self) -> Planning:
        crosser = self.build_crosser()

        while not crosser.completed:
            try:
                planned_trip = next(crosser)
            except StopPlannedTripIterationException:
                break
            route = planned_trip.route
            route.append_planned_trip(planned_trip)
            crosser.mark_planned_trip_as_done(planned_trip)

        for route in crosser.routes:
            route.finish()
        planning = Planning(crosser.routes)
        return planning
