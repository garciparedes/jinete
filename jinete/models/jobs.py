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
        Callable,
    )
    from .routes import (
        Route,
    )
    from .trips import (
        Trip,
    )


class Job(Model):
    trips: Set[Trip]
    objective: Objective

    def __init__(self, trips: Set[Trip], objective: Objective = None, *args, **kwargs):
        if objective is None:
            objective = DialARideObjective()

        self.trips = trips
        self.objective = objective

    def __iter__(self):
        yield from self.trips

    def as_dict(self) -> Dict[str, Any]:
        trips_str = ', '.join(str(trip) for trip in self.trips)
        dict_values = {
            'trips': f'{{{trips_str}}}',
            'objective': self.objective,
        }
        return dict_values
