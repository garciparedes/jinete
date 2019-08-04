from .abc import StorerFormatter


class HashCodeStorerFormatter(StorerFormatter):

    @staticmethod
    def route_to_str(route) -> str:
        loaded_trips = route.loaded_trips
        trips_str = ' '.join(trip.identifier for trip in loaded_trips)
        return f'{len(loaded_trips)} {trips_str}'

    def format(self) -> str:
        result = str()
        result += '\n'.join(self.route_to_str(route) for route in self.planning.routes)
        return result
