import logging

import itertools as it
from ..abc import (
    LocalSearchStrategy,
)

logger = logging.getLogger(__name__)


class ReallocationLocalSearchStrategy(LocalSearchStrategy):

    def _improve(self) -> None:
        from ....insertion import InsertionStrategy  # FIXME Should this import come from "insertion" module?
        strategy = InsertionStrategy()
        logger.info(f'Starting to improve "Result" with "{self.__class__.__name__}"...')
        overwritten_routes = set()
        cost = - float('inf')
        for origin, destination in it.permutations(self.routes, 2):
            cost = max(cost, sum([
                self.objective.optimization_function(origin)[-1],
                self.objective.optimization_function(destination)[-1],
            ]))

            for trip in origin.trips:
                new_origin = origin.clone()
                new_origin.remove_trip(trip)

                new_origin.flush()
                if not new_origin.feasible:
                    continue

                partial_cost = self.objective.optimization_function(new_origin)
                for i, j in it.combinations(range(len(destination.stops) - 1), 2):
                    destinations = strategy.compute(destination, trip, i, j)
                    if not any(destinations):
                        continue
                    new_destination = destinations[0]

                    new_cost = partial_cost[-1] + self.objective.optimization_function(new_destination)[-1]
                    if not new_cost > cost:
                        continue

                    logger.info(f'Improved planning with "{self.__class__.__name__}": "{new_cost}" > "{cost}"')
                    overwritten_routes = {new_origin, new_destination}
                    cost = new_cost

        self._update_routes(overwritten_routes)
