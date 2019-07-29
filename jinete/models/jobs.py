from typing import (
    Set,
    Any,
    Dict,
    Callable, Tuple)

from .abc import (
    Model,
)
from .trips import (
    Trip,
)

OPTIMIZATION_FUNCTIONS = {
    'DIAL_A_RIDE': (
        False,
        lambda route: sum(
            planned_trip.cost for planned_trip in route.planned_trips
        )
    ),
    'TAXI_SHARING': (
        False,
        lambda route: sum(
            planned_trip.duration for planned_trip in route.planned_trips if not planned_trip.capacity
        )
    )
}


class Job(Model):
    trips: Set[Trip]
    bonus: float
    optimization_function: Callable[[Any], float]

    def __init__(self, trips: Set[Trip], bonus: float,
                 optimization_function: Tuple[bool, Callable[[Any], float]] = None,
                 *args, **kwargs):
        if optimization_function is None:
            optimization_function = OPTIMIZATION_FUNCTIONS['DIAL_A_RIDE']

        self.trips = trips
        self.bonus = bonus
        self.optimization_function = optimization_function

    def __iter__(self):
        yield from self.trips

    def as_dict(self) -> Dict[str, Any]:
        trips_str = ', '.join(str(trip) for trip in self.trips)
        dict_values = {
            'trips': f'{{{trips_str}}}',
            'bonus': self.bonus
        }
        return dict_values
