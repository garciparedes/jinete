from __future__ import (
    annotations,
)

from typing import (
    TYPE_CHECKING,
)

from .abc import (
    Model,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Generator,
        Tuple,
        Any,
        Callable,
    )
    from uuid import UUID
    from .trips import Trip
    from .routes import Route
    from .jobs import Job
    from .vehicles import (
        Fleet,
        Vehicle,
    )
    from .plannings import Planning
    from .objectives import (
        Objective,
        OptimizationDirection,
        Optimizable,
    )
    from ..algorithms import Algorithm


class Result(Model):
    def __init__(self, algorithm: Algorithm, planning: Planning, computation_time: float):
        self.algorithm = algorithm
        self.planning = planning
        self.computation_time = computation_time

    @property
    def job(self) -> Job:
        return self.algorithm.job

    @property
    def fleet(self) -> Fleet:
        return self.algorithm.fleet

    @property
    def trips(self) -> Set[Trip]:
        return self.job.trips

    @property
    def vehicles(self) -> Set[Vehicle]:
        return self.fleet.vehicles

    @property
    def routes(self) -> Set[Route]:
        return self.planning.routes

    @property
    def planning_uuid(self) -> UUID:
        return self.planning.uuid

    @property
    def feasible(self) -> bool:
        return self.planning.feasible

    @property
    def completed_trips(self) -> Set[Trip]:
        trips: Set[Trip] = set()
        for route in self.routes:
            trips |= set(route.loaded_trips)
        return trips

    @property
    def coverage_rate(self):
        return len(self.completed_trips) / len(self.job.trips)

    @property
    def objective(self) -> Objective:
        return self.job.objective

    @property
    def optimization_function(self) -> Callable[[Optimizable], Tuple[float, ...]]:
        return self.objective.optimization_function

    @property
    def optimization_value(self) -> Tuple[float, ...]:
        return self.optimization_function(self)

    @property
    def direction(self) -> OptimizationDirection:
        return self.objective.direction

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ("fleet_uuid", tuple(self.fleet)),
            ("job", tuple(self.job)),
            ("algorithm_name", type(self.algorithm).__name__),
            ("planning_uuid", self.planning_uuid),
        )
