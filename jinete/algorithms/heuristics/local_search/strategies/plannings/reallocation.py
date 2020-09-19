import itertools as it
import logging

from jinete.utils import (
    sample_index_pairs,
)

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
        base_cost = self._objective.optimization_function(self._planning)[-1]
        best_cost = base_cost
        for origin, destination in it.permutations(self._routes, 2):

            partial_cost = base_cost
            partial_cost -= self._objective.optimization_function(origin)[-1]
            partial_cost -= self._objective.optimization_function(destination)[-1]

            for trip in origin.trips:
                new_origin = origin.clone()
                new_origin.remove_trip(trip)

                new_origin.flush()
                if not new_origin.feasible:
                    continue

                partial_cost_origin = partial_cost + self._objective.optimization_function(new_origin)[-1]

                for i, j in sample_index_pairs(len(destination.stops), 128):
                    destinations = strategy.compute(destination, trip, i, j)
                    if not any(destinations):
                        continue
                    new_destination = destinations[0]

                    new_cost = partial_cost_origin + self._objective.optimization_function(new_destination)[-1]
                    if not new_cost > best_cost:
                        continue

                    logger.info(f'Improved planning with "{self.__class__.__name__}": "{new_cost}" > "{best_cost}"')
                    overwritten_routes = {new_origin, new_destination}
                    best_cost = new_cost

        self._update_routes(overwritten_routes)
