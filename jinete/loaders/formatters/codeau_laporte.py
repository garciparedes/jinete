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
from .exceptions import (
    LoaderFormatterException,
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
        destination_idx = origin_idx + n

        origin_row = self.data[origin_idx]
        destination_row = self.data[destination_idx]

        origin = surface.get_or_create_position(origin_row[1:3])
        destination = surface.get_or_create_position(destination_row[1:3])

        e1, l1 = origin_row[5:7]
        e2, l2 = destination_row[5:7]

        if e1 == 0 and l1 == 1440:
            earliest, latest = e2, l2
            inbound = True
        elif e2 == 0 and l2 == 1440:
            earliest, latest = e1, l1
            inbound = False
        else:
            raise LoaderFormatterException('It is not possible to distinguish between inbound and outbound task.')

        identifier = str(idx)
        timeout = latest - earliest

        trip = Trip(
            identifier=identifier,
            origin=origin,
            destination=destination,
            inbound=inbound,
            earliest=earliest,
            timeout=timeout,
            load_time=10.0,
        )
        return trip

    def surface(self, *args, **kwargs) -> Surface:
        surface = GeometricSurface(DistanceMetric.EUCLIDEAN)
        logger.info(f'Created surface!')
        return surface
