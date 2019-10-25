import logging

from .abc import (
    Breeder,
)
from ....models import (
    Result
)

logger = logging.getLogger(__name__)


class FlipBreeder(Breeder):

    def improve(self) -> Result:
        for route in self.planning.routes:
            cost = self.objective.optimization_function(route)

            for i in range(1, len(route.stops) - 1):
                j = i + 1
                first = route.stops[i]
                second = route.stops[j]

                if not set(first.pickups).isdisjoint(second.deliveries):
                    continue
                first.flip(second)

                if not route.feasible or cost < self.objective.optimization_function(route):
                    second.flip(first)
                    continue

                cost = self.objective.optimization_function(route)
                logger.info(f'Flipped "{i}"-th and "{j}"-th stops from "{route}".')
        return self.result
