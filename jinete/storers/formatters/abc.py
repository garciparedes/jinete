"""The set of abstract definitions for the formatters module."""

from __future__ import (
    annotations,
)

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Tuple,
    )
    from ...models import (
        Result,
        Planning,
        Job,
        Route,
        Objective,
        OptimizationDirection,
    )


class StorerFormatter(ABC):
    """Format a solution as a readable string."""

    def __init__(self, result: Result, remove_empty_routes: bool = False):
        """Construct a new object instance.

        :param result:
        :param remove_empty_routes:
        """
        self.result = result
        self.remove_empty_routes = remove_empty_routes

    @property
    def _job(self) -> Job:
        return self.result.job

    @property
    def _planning(self) -> Planning:
        return self.result.planning

    @property
    def _routes(self) -> Set[Route]:
        if self.remove_empty_routes:
            return self._planning.loaded_routes
        return self._planning.routes

    @property
    def _computation_time(self) -> float:
        return self.result.computation_time

    @property
    def _coverage_rate(self) -> float:
        return self.result.coverage_rate

    @property
    def _objective(self) -> Objective:
        return self.result.objective

    @property
    def _optimization_value(self) -> Tuple[float, ...]:
        return self.result.optimization_value

    @property
    def _feasible(self) -> bool:
        return self.result.feasible

    @property
    def _direction(self) -> OptimizationDirection:
        return self.result.direction

    @abstractmethod
    def format(self) -> str:
        """Perform a format process."""
        pass
