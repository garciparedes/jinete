import logging

import itertools as it
from ..abc import (
    LocalSearchStrategy,
)

logger = logging.getLogger(__name__)


class RepositionLocalSearchStrategy(LocalSearchStrategy):

    def _improve(self) -> None:
        from ....insertion import InsertionStrategy  # FIXME Should this import come from "insertion" module?
        strategy = InsertionStrategy()
        logger.info(f'Starting to improve "Result" with "{self.__class__.__name__}"...')

        overwritten_routes = set()
        base_cost = self.objective.optimization_function(self.planning)[-1]
        best_cost = base_cost
        for route in self.routes:
            best_route = None
            partial_cost = base_cost
            partial_cost -= self.objective.optimization_function(route)[-1]

            for trip in route.trips:
                base_route = route.clone()
                base_route.remove_trip(trip)

                base_route.flush()
                if not base_route.feasible:
                    continue

                for i, j in it.combinations(range(len(base_route.stops) - 1), 2):
                    destinations = strategy.compute(base_route, trip, i, j)
                    if not any(destinations):
                        continue
                    new_cost = partial_cost + self.objective.optimization_function(destinations[0])[-1]
                    if not new_cost > best_cost:
                        continue

                    logger.info(
                        f'Improved planning cost with "{self.__class__.__name__}": "{new_cost}" > "{best_cost}"'
                    )
                    best_cost = new_cost
                    best_route = destinations[0]

            if best_route is None:
                continue

            overwritten_routes.add(best_route)

        self._update_routes(overwritten_routes)
