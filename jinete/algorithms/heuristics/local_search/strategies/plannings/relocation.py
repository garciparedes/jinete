import logging

import itertools as it
from ..abc import (
    LocalSearchStrategy,
)
from ......models import (
    Result,
)

logger = logging.getLogger(__name__)


class RelocationLocalSearchStrategy(LocalSearchStrategy):

    def _improve(self) -> Result:
        from ....insertion import InsertionStrategy
        strategy = InsertionStrategy()
        logger.info(f'Starting to improve "Result" with "{self.__class__.__name__}"...')
        best = None
        cost = - float('inf')
        for origin, destination in it.permutations(self.routes, 2):
            cost = max(sum([
                self.objective.optimization_function(origin)[-1],
                self.objective.optimization_function(origin)[-1],
            ]), cost)

            for trip in origin.trips:
                new_origin = origin.clone()
                new_origin.remove_trip(trip)

                new_origin.flush()
                if not new_origin.feasible:
                    continue

                partial_cost = self.objective.optimization_function(new_origin)
                for i, j in it.combinations(range(len(destination.stops) - 1), 2):
                    new_destination = strategy.compute_one(destination, trip, i, j)

                    new_destination.flush()
                    if not new_destination.feasible:
                        continue

                    new_cost = partial_cost[-1] + self.objective.optimization_function(new_destination)[-1]
                    if new_cost > cost:
                        print(f'Improved! {new_cost} < {cost}')
                        if new_cost > -294:
                            new_origin.flush()
                            new_destination.flush()
                            new_origin.feasible
                            new_destination.feasible

                        best = {new_origin, new_destination}
                        cost = new_cost
        if best:
            self.planning.routes = best
        return self.result
