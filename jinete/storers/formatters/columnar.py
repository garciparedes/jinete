from itertools import chain
from typing import List

from .abc import StorerFormatter

from ...models import (
    Route,
    Vehicle,
    PlannedTrip,
)


class ColumnarStorerFormatter(StorerFormatter):

    def vehicle_to_str(self, vehicle: Vehicle) -> List[str]:
        return [
            f'ID: "{vehicle.uuid}"',
            f'Initial:  {vehicle.initial}',
            f'Final:    {vehicle.final}',
            f'Earliest: {vehicle.earliest:7.2f}',
            f'Latest:   {vehicle.latest:7.2f}',
            f'Capacity: {vehicle.capacity:7.2f}',
        ]

    def planned_trip_to_str(self, planned_trip: PlannedTrip) -> List[str]:
        return [
            '\t'.join((
                f'ID: {planned_trip.trip.identifier:6}',
                f'Position: {planned_trip.origin} to {planned_trip.destination}',
                f'Duration: {planned_trip.duration:7.02f}',
                f'Time: {planned_trip.collection_time:8.02f} to {planned_trip.delivery_time:8.02f}',
                f'Load: {planned_trip.capacity}',
            )),
        ]

    def route_to_str(self, route: Route) -> List[str]:
        rows = chain.from_iterable(self.planned_trip_to_str(planned_trip) for planned_trip in route.planned_trips)
        return [
            f'Vehicle: ',
            *(f'\t{row}' for row in self.vehicle_to_str(route.vehicle)),
            f'Planned Trips: "{len(route.planned_trips)}"',
            *(f'\t{row}' for row in rows)
        ]

    def format(self) -> str:
        rows = chain.from_iterable(self.route_to_str(route) for route in self.planning.routes)
        return '\n'.join((
            f'Planning UUID: "{self.planning.uuid}"',
            f'Routes count: "{len(self.planning.routes)}"',
            f'Routes: ',
            '\n'.join(f'\t{row}' for row in rows),
            f'Computation time: "{self.result.computation_time:0.4f}" seconds',
            f'Coverage Rate: "{self.result.coverage_rate}"',
        ))
