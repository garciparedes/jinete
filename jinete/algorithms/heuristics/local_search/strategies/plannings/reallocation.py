import logging

import itertools as it
from ..abc import (
    LocalSearchStrategy,
)
from ......models import (
    Result,
)

logger = logging.getLogger(__name__)


class ReallocationLocalSearchStrategy(LocalSearchStrategy):

    def _improve(self) -> Result:
        from ....insertion import InsertionStrategy  # FIXME Should this import come from "insertion" module?
        strategy = InsertionStrategy()
        logger.info(f'Starting to improve "Result" with "{self.__class__.__name__}"...')
        best = None
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
                    new_destination = strategy.compute_one(destination, trip, i, j)

                    new_destination.flush()
                    if not new_destination.feasible:
                        continue

                    new_cost = partial_cost[-1] + self.objective.optimization_function(new_destination)[-1]
                    if not new_cost > cost:
                        continue

                    logger.info(f'Improved planning! "{new_cost}" < "{cost}"')
                    best = {new_origin, new_destination}
                    cost = new_cost

        if best is not None:
            assert len(best) == 2
            new_vehicles = {route.vehicle for route in best}
            routes = {route for route in self.planning.routes if route.vehicle not in new_vehicles}
            routes |= best
            self.planning.routes = routes

        return self.result
