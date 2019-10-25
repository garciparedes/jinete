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
        Generator,
        Tuple,
        Type,
        Optional,
    )
    from .trips import (
        Trip,
    )


class Job(Model):
    trips: Set[Trip]
    objective_cls: Type[Objective]
    _objective: Optional[Objective]

    def __init__(self, trips: Set[Trip], objective_cls: Type[Objective], *args, **kwargs):
        if objective_cls is None:
            objective_cls = DialARideObjective

        self.trips = trips
        self.objective_cls = objective_cls
        self._objective = None

        self.args = args
        self.kwargs = kwargs

    @property
    def objective(self) -> Objective:
        if self._objective is None:
            self._objective = self.objective_cls(*self.args, **self.kwargs)
        return self._objective

    def __deepcopy__(self, memo) -> Job:
        return self

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('trip_identifiers', tuple(trip.identifier for trip in self.trips)),
            ('objective', self.objective),
        )
