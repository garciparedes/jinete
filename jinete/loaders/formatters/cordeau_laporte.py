"""Formatting modules from raw objects containing Cordeau-Laporte problem instances to ``jinete```s class hierarchy."""

from __future__ import (
    annotations,
)

import logging
from typing import (
    TYPE_CHECKING,
)

from ...models import (
    DialARideObjective,
    DistanceMetric,
    Fleet,
    GeometricSurface,
    Job,
    Service,
    Trip,
    Vehicle,
)
from .abc import (
    LoaderFormatter,
)

if TYPE_CHECKING:
    from ...models import Surface

logger = logging.getLogger(__name__)


class CordeauLaporteLoaderFormatter(LoaderFormatter):
    """Format a HashCode problem instance from a raw object to build ``jinete``'s set of objects."""

    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        """Retrieve the fleet object for the current on load instance.

        :param surface: The surface surface object for the current on load instance.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        row = self.data[0]
        m = int(row[0])

        depot_row = self.data[1]
        depot_position = surface.get_or_create_position(depot_row[1:3])

        origin = Service(depot_position)

        capacity = row[3]
        timeout = row[2]

        vehicles = set()
        for idx in range(m):
            vehicle = Vehicle(str(idx), origin, capacity=capacity, timeout=timeout,)

            vehicles.add(vehicle)
        fleet = Fleet(vehicles)
        logger.info(f"Created {fleet}!")
        return fleet

    def job(self, surface: Surface, *args, **kwargs) -> Job:
        """Retrieve the job object for the current on load instance.

        :param surface: The surface object for the current on load instance.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        row = self.data[0]
        n = int(row[1] // 2)

        trips = set()
        for idx in range(n):
            trip = self._build_trip(surface, idx, n)
            trips.add(trip)
        job = Job(trips, objective_cls=DialARideObjective)
        logger.info(f'Created "{job}"!')
        return job

    def _build_trip(self, surface: Surface, idx: int, n: int) -> Trip:
        origin_idx = idx + 2
        origin_row = self.data[origin_idx]
        origin = Service(
            position=surface.get_or_create_position(origin_row[1:3]),
            earliest=origin_row[5],
            latest=origin_row[6],
            duration=origin_row[3],
        )

        destination_row = self.data[origin_idx + n]
        destination = Service(
            position=surface.get_or_create_position(destination_row[1:3]),
            earliest=destination_row[5],
            latest=destination_row[6],
            duration=destination_row[3],
        )

        identifier = f"{idx + 1:.0f}"

        assert origin_row[4] == -destination_row[4]
        capacity = origin_row[4]

        timeout = self.data[0][4]

        trip = Trip(identifier=identifier, origin=origin, destination=destination, capacity=capacity, timeout=timeout,)
        return trip

    def surface(self, *args, **kwargs) -> Surface:
        """Retrieve the surface object for the current on load instance.

        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        surface = GeometricSurface(DistanceMetric.EUCLIDEAN)
        logger.info("Created surface!")
        return surface
