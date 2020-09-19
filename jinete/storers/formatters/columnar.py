"""The set of definitions to format the artifact to be stored following a columnar style."""

import itertools as it
from typing import (
    List,
)

from ...models import (
    PlannedTrip,
    Route,
    Stop,
    Vehicle,
)
from .abc import (
    StorerFormatter,
)


class ColumnarStorerFormatter(StorerFormatter):
    """Format a solution as a readable string following a columnar style."""

    def __init__(self, tab_character: str = "  ", *args, **kwargs):
        """Construct a new instance.

        :param tab_character: The tabulation character to use during the formatting process.
        :param args: Additional positional parameters.
        :param kwargs: Additional named parameters.
        """
        super().__init__(*args, **kwargs)
        self.tab_character = tab_character

    def format(self) -> str:
        """Perform a format process."""
        rows = it.chain.from_iterable(self._route_to_str(route) for route in self._routes)
        return "\n".join(
            (
                f'Planning UUID: "{self._planning.uuid}"',
                f'Routes count: "{len(self._routes)}"',
                "Routes: ",
                "\n".join(f"{self.tab_character}{row}" for row in rows),
                f'Computation time: "{self._computation_time:0.4f}" seconds',
                f'Coverage Rate: "{self._coverage_rate}"',
                f'Objective: "{self._objective.__class__.__name__}"',
                f'Optimization Value: "{self._optimization_value}"',
                f'Feasible: "{self._feasible}"',
                f'Direction: "{self._direction}"',
            )
        )

    def _route_to_str(self, route: Route) -> List[str]:
        planned_trip_rows = [self._planned_trip_to_str(planned_trip) for planned_trip in route.planned_trips]
        stop_rows = [self._stop_to_str(stop) for stop in route.stops]
        return [
            "Vehicle: ",
            *(f"{self.tab_character}{row}" for row in self._vehicle_to_str(route.vehicle)),
            f'Planned Trips: "{sum(1 for _ in route.planned_trips)}"',
            *(f"{self.tab_character}{row}" for row in planned_trip_rows),
            f'Stops: "{len(route.stops)}"',
            *(f"{self.tab_character}{row}" for row in stop_rows),
        ]

    @staticmethod
    def _vehicle_to_str(vehicle: Vehicle) -> List[str]:
        return [
            f'ID: "{vehicle.identifier}"',
            f"Initial:  {vehicle.origin_position}",
            f"Final:    {vehicle.destination_position}",
            f"Earliest: {vehicle.origin_earliest:7.2f}",
            f"Latest:   {vehicle.origin_latest:7.2f}",
            f"Capacity: {vehicle.capacity:7.2f}",
        ]

    def _planned_trip_to_str(self, planned_trip: PlannedTrip) -> str:
        return self.tab_character.join(
            (
                f"ID: {planned_trip.trip.identifier:5}",
                f"P: {planned_trip.origin} to {planned_trip.destination}",
                f"TW: {planned_trip.trip.origin_earliest:7.01f} to {planned_trip.trip.destination_latest:7.01f}",
                f"WT: {planned_trip.waiting_time:7.01f}",
                f"NT: {planned_trip.transit_time:7.01f}",
                f"LT: {planned_trip.load_time:4.01f}",
                f"TT: {planned_trip.duration:6.01f}",
                f"T: {planned_trip.pickup_time:7.01f} to {planned_trip.delivery_time:7.01f}",
                f"L: {planned_trip.capacity}",
            )
        )

    def _stop_to_str(self, stop: Stop) -> str:
        return self.tab_character.join(
            (
                f"ID: {stop.identifier:5}",
                f"P: {stop.position}",
                f"TW: {stop.earliest:7.01f} to {stop.latest:7.01f}",
                f"WT: {stop.waiting_time:7.01f}",
                f"NT: {stop.transit_time:7.01f}",
                f"LT: {stop.load_time:5.01f}",
                f"DT: {stop.departure_time:7.01f}",
                f"L: {stop.capacity}",
            )
        )
