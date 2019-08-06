from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        Set,
    )
    from ..models import (
        Trip,
    )


class Result(object):

    def __init__(self, fleet, job, algorithm_cls, planning, computation_time):
        self.fleet = fleet
        self.job = job
        self.algorithm_cls = algorithm_cls
        self.planning = planning
        self.computation_time = computation_time

    @property
    def completed_trips(self) -> Set[Trip]:
        trips = set()
        for route in self.planning.routes:
            trips |= set(route.loaded_trips)
        return trips

    @property
    def coverage_rate(self):
        return len(self.completed_trips) / len(self.job.trips)
