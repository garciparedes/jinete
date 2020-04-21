"""The set of definitions to format the artifact to be stored following the HashCode style."""

from __future__ import (
    annotations,
)

from .abc import (
    StorerFormatter,
)


class HashCodeStorerFormatter(StorerFormatter):
    """Format a solution as a readable string following the HashCode style."""

    def __init__(self, remove_empty_routes: bool = True, *args, **kwargs):
        """Construct a new instance.

        :param remove_empty_routes: Flag to manage if empty routes should be removed.
        :param args: Additional positional parameters.
        :param kwargs: Additional named parameters.
        """
        kwargs["remove_empty_routes"] = remove_empty_routes
        super().__init__(
            *args, **kwargs,
        )

    @staticmethod
    def _route_to_str(route) -> str:
        trips_str = " ".join(trip.identifier for trip in route.loaded_trips)
        return f"{route.loaded_trips_count} {trips_str}"

    def format(self) -> str:
        """Perform a format process."""
        result = str()
        lines = sorted(self._route_to_str(route) for route in self._routes)
        result += "\n".join(lines)
        return result
