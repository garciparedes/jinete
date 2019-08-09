import logging

from ...models import (
    Fleet,
    Job,
    Surface,
    GeometricSurface,
    METRIC,
    Vehicle,
    Trip,
)
from .abc import (
    LoaderFormatter,
)

logger = logging.getLogger(__name__)


class HashCodeLoaderFormatter(LoaderFormatter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: Set bonus and number of steps (Config object)
        #

    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        row = self.data[0]
        n, timeout, capacity = row[2], row[5], 1

        initial = surface.get_or_create_position([0, 0])
        vehicles = set(Vehicle(initial, capacity=capacity, timeout=timeout) for _ in range(n))
        fleet = Fleet(vehicles)
        logger.info(f'Created fleet!')
        return fleet

    def job(self, surface: Surface, *args, **kwargs) -> Job:
        rows = self.data[1:]
        trips = set(self._build_trip(surface, str(i), *row) for i, row in enumerate(rows))
        job = Job(trips, *args, **kwargs)
        logger.info(f'Created job!')
        return job

    def _build_trip(self, surface: Surface, identifier: str, x1: float, y1: float, x2: float, y2: float,
                    earliest: float, latest: float) -> Trip:
        origin = surface.get_or_create_position([x1, y1])
        destination = surface.get_or_create_position([x2, y2])
        timeout = latest - earliest
        trip = Trip(identifier, origin, destination, earliest, timeout)
        logger.debug(f'Created trip!')
        return trip

    def surface(self, *args, **kwargs) -> Surface:
        row = self.data[0]
        rows = row[0]
        columns = row[1]
        surface = GeometricSurface(METRIC['MANHATTAN'])
        logger.info(f'Created surface!')
        return surface
