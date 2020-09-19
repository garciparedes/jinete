import logging
from itertools import (
    chain,
    combinations,
)

from ..abc import (
    LocalSearchStrategy,
)

logger = logging.getLogger(__name__)


class TwoOPTLocalSearchStrategy(LocalSearchStrategy):
    def _improve(self) -> None:
        logger.info(f'Starting to improve "Result" with "{self.__class__.__name__}"...')

        overwritten_routes = set()
        for route in self._routes:
            logger.info(f'Improving route performed with vehicle identified by "{route.vehicle_identifier}"...')
            cost = self._objective.optimization_function(route)

            for i, k in combinations(range(1, len(route.stops) - 1), 2):
                j = k + 1
                condition = any(
                    any(
                        delivery in chain.from_iterable(b.pickup_planned_trips for b in route.stops[i : j + 1])
                        for delivery in a.delivery_planned_trips
                    )
                    for a in route.stops[i : j + 1]
                )
                if condition:
                    continue

                new_route = route.clone(i - 1)

                old_stops = [new_route.remove_stop_at(i) for _ in range(i, len(new_route.stops) - 1)]

                threshold = (j + 1) - i
                for stop in reversed(old_stops[:threshold]):
                    stop.previous = new_route.current_stop
                    new_route.insert_stop(stop)

                for stop in old_stops[threshold:]:
                    stop.previous = new_route.current_stop
                    new_route.insert_stop(stop)

                if not new_route.feasible:
                    continue

                new_cost = self._objective.optimization_function(new_route)
                if not new_cost > cost:
                    continue

                logger.info(f'Improved planning with "{self.__class__.__name__}": "{new_cost}" > "{cost}"')
                overwritten_routes.add(new_route)
                cost = new_cost

        self._update_routes(overwritten_routes)
