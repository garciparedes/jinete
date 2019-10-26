from __future__ import annotations

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
        Type,
    )
    from uuid import (
        UUID,
    )
    from .trips import (
        Trip,
    )
    from .routes import (
        Route,
    )
    from .jobs import (
        Job,
    )
    from .vehicles import (
        Fleet,
        Vehicle,
    )
    from .plannings import (
        Planning,
    )
    from .objectives import (
        Objective,
        OptimizationDirection,
    )
    from ..algorithms import (
        Algorithm,
    )


class Result(Model):

    def __init__(self, fleet: Fleet, job: Job, algorithm_cls: Type[Algorithm], planning: Planning,
                 computation_time: float):
        self.fleet = fleet
        self.job = job
        self.algorithm_cls = algorithm_cls
        self.planning = planning
        self.computation_time = computation_time

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
    def optimization_function(self) -> float:
        return self.objective.optimization_function(self)

    @property
    def direction(self) -> OptimizationDirection:
        return self.objective.direction

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('fleet_uuid', tuple(self.fleet)),
            ('job', tuple(self.job)),
            ('algorithm_name', self.algorithm_cls.__name__),
            ('planning_uuid', self.planning_uuid)
        )
