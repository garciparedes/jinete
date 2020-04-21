from __future__ import (
    annotations,
)

from abc import (
    ABC,
    abstractmethod,
)
from copy import (
    deepcopy,
)
from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from typing import Set
    from .....models import Planning, Result, Objective, Route


class LocalSearchStrategy(ABC):
    def __init__(self, result: Result, with_copy: bool = True):
        if with_copy:
            result = deepcopy(result)

        self.result = result

    @property
    def _objective(self) -> Objective:
        return self.result.objective

    @property
    def _planning(self) -> Planning:
        return self.result.planning

    @property
    def _routes(self) -> Set[Route]:
        return self._planning.routes

    def improve(self) -> Result:

        if __debug__:
            for route in self._routes:
                assert all(s1 == s2.previous for s1, s2 in zip(route.stops[:-1], route.stops[1:]))
                assert all(s1.departure_time <= s2.arrival_time for s1, s2 in zip(route.stops[:-1], route.stops[1:]))

        self._improve()

        if __debug__:
            for route in self._routes:
                assert all(s1 == s2.previous for s1, s2 in zip(route.stops[:-1], route.stops[1:]))
                if not all(s1.departure_time <= s2.arrival_time for s1, s2 in zip(route.stops[:-1], route.stops[1:])):
                    assert False

        return self.result

    @abstractmethod
    def _improve(self) -> None:
        pass

    def _update_routes(self, overwritten_routes: Set[Route]):
        if any(overwritten_routes):
            overwritten_vehicles = {route.vehicle for route in overwritten_routes}
            routes = {route for route in self._planning.routes if route.vehicle not in overwritten_vehicles}
            routes |= overwritten_routes
            self._planning.routes = routes
