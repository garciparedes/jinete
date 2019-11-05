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
        logger.info(f'Starting to improve "Result" with "{self.__class__.__name__}"...')
        for idx, route in enumerate(self.routes):
            cost = self.objective.optimization_function(route)

            for i in range(1, len(route.stops) - 1):
                j = i + 1
                k = i + 2
                first = route.stops[i]
                second = route.stops[j]
                third = route.stops[k] if k < len(route.stops) else None

                if not set(first.pickups).isdisjoint(second.deliveries):
                    continue
                first.flip(second, third)

                if not route.feasible or cost == self.objective.best(cost, route):
                    second.flip(first, third)
                    continue

                cost = self.objective.optimization_function(route)
                logger.info(f'Flipped "{i}"-th and "{j}"-th stops from "{route}".')
        return self.result
