from .abc import StorerFormatter


class ColumnarStorerFormatter(StorerFormatter):

    @staticmethod
    def route_to_str(route) -> str:
        loaded_trips = route.loaded_trips
        trips_str = ' '.join(trip.identifier for trip in loaded_trips)
        return f'{len(loaded_trips)} {trips_str}'

    def format(self) -> str:
        return '\n'.join((
            f'Planning UUID: "{self.planning.uuid}"',
            f'Routes count: "{len(self.planning.routes)}"',
            f'Routes: '
            '\n'.join(f'\t{self.route_to_str(route)}' for route in self.planning.routes),
            f'Computation time: "{self.planning.computation_time}" seconds',
        ))
