import logging

from ......models import (
    Route,
    Stop,
)
from ..abc import (
    LocalSearchStrategy,
)

logger = logging.getLogger(__name__)


class OneShiftLocalSearchStrategy(LocalSearchStrategy):
    def _improve(self) -> None:
        logger.info(f'Starting to improve "Result" with "{self.__class__.__name__}"...')
        for route in self._routes:
            cost = self._objective.optimization_function(route)

            for i in range(1, len(route.stops) - 1):
                j = i + 1
                k = i + 2
                first = route.stops[i]
                second = route.stops[j]
                third = route.stops[k] if k < len(route.stops) else None

                if not set(first.pickup_planned_trips).isdisjoint(second.delivery_planned_trips):
                    continue
                self._flip(route, first, second, third)

                if not route.feasible or cost == self._objective.best(cost, route):
                    self._flip(route, second, first, third)
                    continue

                cost = self._objective.optimization_function(route)
                logger.info(f'Flipped "{i}"-th and "{j}"-th stops from "{route}".')

    def _flip(self, route: Route, previous: Stop, other: Stop, following: Stop = None) -> None:
        assert following is None or following.previous == other
        assert other.previous == previous

        self_index = route.stops.index(other)
        other_index = route.stops.index(previous)
        route.stops[self_index], route.stops[other_index] = route.stops[other_index], route.stops[self_index]

        if following is not None:
            following.previous = previous
        other.previous = previous.previous
        previous.previous = other

        for stop in route.stops[self_index:]:
            stop.flush()
