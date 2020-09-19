"""Formatting modules from raw objects containing HashCode problem instances to ``jinete```s class hierarchy."""

import logging

from ...models import (
    DistanceMetric,
    Fleet,
    GeometricSurface,
    HashCodeObjective,
    Job,
    Service,
    Surface,
    Trip,
    Vehicle,
)
from .abc import (
    LoaderFormatter,
)

logger = logging.getLogger(__name__)


class HashCodeLoaderFormatter(LoaderFormatter):
    """Format a HashCode problem instance from a raw object to build ``jinete``'s set of objects."""

    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        """Retrieve the fleet object for the current on load instance.

        :param surface: The surface surface object for the current on load instance.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        row = self.data[0]
        n, latest, capacity = int(row[2]), row[5], 1.0

        origin = Service(surface.get_or_create_position([0, 0]), latest=latest)
        vehicles = set(Vehicle(str(idx), origin, capacity=capacity) for idx in range(n))
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
        bonus = self.data[0][4]
        rows = self.data[1:]
        trips = set(self._build_trip(surface, str(i), bonus, *row) for i, row in enumerate(rows))

        kwargs["objective_cls"] = HashCodeObjective
        job = Job(trips, *args, **kwargs)

        logger.info(f'Created "{job}"!')
        return job

    @staticmethod
    def _build_trip(
        surface: Surface,
        identifier: str,
        bonus: float,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        earliest: float,
        latest: float,
    ) -> Trip:
        origin = Service(position=surface.get_or_create_position([x1, y1]), earliest=earliest, latest=latest,)
        destination = Service(position=surface.get_or_create_position([x2, y2]),)
        trip = Trip(identifier, on_time_bonus=bonus, origin=origin, destination=destination)
        logger.debug("Created trip!")
        return trip

    def surface(self, *args, **kwargs) -> Surface:
        """Retrieve the surface object for the current on load instance.

        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        surface = GeometricSurface(DistanceMetric.MANHATTAN)
        logger.info("Created surface!")
        return surface
