from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...models import (
    GeometricSurface,
    DistanceMetric,
    Fleet,
    Vehicle,
    Job,
    Trip,
    DialARideObjective,
)
from .abc import (
    LoaderFormatter,
)

if TYPE_CHECKING:
    from ...models import (
        Surface,
    )

logger = logging.getLogger(__name__)


class CordeauLaporteLoaderFormatter(LoaderFormatter):

    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        row = self.data[0]
        m = int(row[0])

        depot_row = self.data[1]
        initial = surface.get_or_create_position(depot_row[1:3])
        final = None

        capacity = row[3]
        route_timeout = row[2]
        trip_timeout = row[4]

        vehicles = set()
        for idx in range(m):
            vehicle = Vehicle(
                str(idx),
                initial,
                final,
                capacity=capacity,
                route_timeout=route_timeout,
                trip_timeout=trip_timeout,
            )

            vehicles.add(vehicle)
        fleet = Fleet(vehicles)
        logger.info(f'Created fleet!')
        return fleet

    def job(self, surface: Surface, *args, **kwargs) -> Job:
        row = self.data[0]
        n = int(row[1] // 2)

        trips = set()
        for idx in range(n):
            trip = self.build_trip(surface, idx, n)
            trips.add(trip)
        job = Job(trips, objective_cls=DialARideObjective)
        logger.info(f'Created job!')
        return job

    def build_trip(self, surface: Surface, idx: int, n: int) -> Trip:
        origin_idx = idx + 2
        origin_row = self.data[origin_idx]
        origin = surface.get_or_create_position(origin_row[1:3])
        origin_earliest, origin_latest = origin_row[5:7]
        origin_duration = origin_row[3]

        destination_idx = origin_idx + n
        destination_row = self.data[destination_idx]
        destination = surface.get_or_create_position(destination_row[1:3])
        destination_earliest, destination_latest = destination_row[5:7]
        destination_duration = destination_row[3]

        identifier = f'{origin_row[0]:.0f}'

        assert origin_row[4] == -destination_row[4]
        capacity = origin_row[4]

        trip = Trip(
            identifier=identifier,
            origin=origin,
            origin_earliest=origin_earliest,
            origin_latest=origin_latest,
            origin_duration=origin_duration,
            destination=destination,
            destination_earliest=destination_earliest,
            destination_latest=destination_latest,
            destination_duration=destination_duration,
            capacity=capacity,
        )
        return trip

    def surface(self, *args, **kwargs) -> Surface:
        surface = GeometricSurface(DistanceMetric.EUCLIDEAN)
        logger.info(f'Created surface!')
        return surface
