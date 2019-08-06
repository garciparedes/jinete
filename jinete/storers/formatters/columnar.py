from .abc import StorerFormatter

from ...models import (
    Route,
)


class ColumnarStorerFormatter(StorerFormatter):

    @staticmethod
    def route_to_str(route: Route) -> str:
        loaded_trips = route.loaded_trips
        trips_str = ' '.join(trip.identifier for trip in loaded_trips)
        return f'Vehicle: {route.vehicle_uuid} Trips: "{len(loaded_trips)}" Identifiers: "{trips_str}"'

    def format(self) -> str:
        return '\n'.join((
            f'Planning UUID: "{self.planning.uuid}"',
            f'Routes count: "{len(self.planning.routes)}"',
            f'Routes: ',
            '\n'.join(f'\t{self.route_to_str(route)}' for route in self.planning.routes),
            f'Computation time: "{self.result.computation_time:0.4f}" seconds',
            f'Coverage Rate: "{self.result.coverage_rate}"',
        ))
