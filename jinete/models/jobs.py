from collections import namedtuple
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
from .routes import (
    Route,
)

OptimizationFunction = namedtuple('OptimizationFunction', {
    'direction': bool,
    'function': Callable[[Route], float],
    'description': str,
})

OPTIMIZATION_FUNCTIONS = {
    'DIAL_A_RIDE': OptimizationFunction(
        False,
        lambda route: sum(
            planned_trip.cost for planned_trip in route.planned_trips
        ),
        'Dial-a-Ride',
    ),
    'TAXI_SHARING': OptimizationFunction(
        False,
        lambda route: sum(
            planned_trip.duration for planned_trip in route.planned_trips if not planned_trip.capacity
        ),
        'Taxi-Sharing',
    )
}


class Job(Model):
    trips: Set[Trip]
    bonus: float
    optimization_function: OptimizationFunction

    def __init__(self, trips: Set[Trip], optimization_function: OptimizationFunction = None,
                 *args, **kwargs):
        if optimization_function is None:
            optimization_function = OPTIMIZATION_FUNCTIONS['DIAL_A_RIDE']

        self.trips = trips
        self.optimization_function = optimization_function

    def __iter__(self):
        yield from self.trips

    def as_dict(self) -> Dict[str, Any]:
        trips_str = ', '.join(str(trip) for trip in self.trips)
        dict_values = {
            'trips': f'{{{trips_str}}}',
            'optimization_function': self.optimization_function,
        }
        return dict_values
