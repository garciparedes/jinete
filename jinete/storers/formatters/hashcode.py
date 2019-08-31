from __future__ import annotations

from .abc import StorerFormatter


class HashCodeStorerFormatter(StorerFormatter):
    def __init__(self, remove_empty_routes: bool = True, *args, **kwargs):
        kwargs['remove_empty_routes'] = remove_empty_routes
        super().__init__(
            *args, **kwargs,
        )

    @staticmethod
    def route_to_str(route) -> str:
        trips_str = ' '.join(trip.identifier for trip in route.loaded_trips)
        return f'{route.loaded_trips_count} {trips_str}'

    def format(self) -> str:
        result = str()
        lines = sorted(self.route_to_str(route) for route in self.routes)
        result += '\n'.join(lines)
        return result
