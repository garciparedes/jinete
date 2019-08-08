from __future__ import annotations

from .abc import StorerFormatter


class HashCodeStorerFormatter(StorerFormatter):
    def __init__(self, remove_empty_routs: bool = True, *args, **kwargs):
        super().__init__(
            remove_empty_routs=remove_empty_routs,
            *args, **kwargs,
        )

    @staticmethod
    def route_to_str(route) -> str:
        loaded_trips = route.loaded_trips
        trips_str = ' '.join(trip.identifier for trip in loaded_trips)
        return f'{len(loaded_trips)} {trips_str}'

    def format(self) -> str:
        result = str()
        result += '\n'.join(self.route_to_str(route) for route in self.routes)
        return result
