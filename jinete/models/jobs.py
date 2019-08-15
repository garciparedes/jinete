from __future__ import annotations

from typing import TYPE_CHECKING

from .abc import (
    Model,
)
from .objectives import (
    Objective,
    DialARideObjective,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Any,
        Dict,
        Type,
    )
    from .trips import (
        Trip,
    )


class Job(Model):
    trips: Set[Trip]
    objective: Objective

    def __init__(self, trips: Set[Trip], objective_cls: Type[Objective], *args, **kwargs):
        if objective_cls is None:
            objective_cls = DialARideObjective

        self.trips = trips
        self.objective_cls = objective_cls
        self._objective = None

    @property
    def objective(self) -> Objective:
        if self._objective is None:
            self._objective = self.objective_cls()
        return self._objective

    def __iter__(self):
        yield from self.trips

    def as_dict(self) -> Dict[str, Any]:
        trips_str = ', '.join(str(trip) for trip in self.trips)
        dict_values = {
            'trips': f'{{{trips_str}}}',
            'objective': self.objective,
        }
        return dict_values
