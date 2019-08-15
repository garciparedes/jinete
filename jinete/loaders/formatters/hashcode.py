import logging

from ...models import (
    Fleet,
    Job,
    Surface,
    GeometricSurface,
    DistanceMetric,
    Vehicle,
    Trip,
    HashCodeObjective,
)
from .abc import (
    LoaderFormatter,
)

logger = logging.getLogger(__name__)


class HashCodeLoaderFormatter(LoaderFormatter):

    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        row = self.data[0]
        n, timeout, capacity = int(row[2]), row[5], 1.0

        initial = surface.get_or_create_position([0, 0])
        vehicles = set(Vehicle(str(idx), initial, capacity=capacity, timeout=timeout) for idx in range(n))
        fleet = Fleet(vehicles)
        logger.info(f'Created fleet!')
        return fleet

    def job(self, surface: Surface, *args, **kwargs) -> Job:
        bonus = self.data[0][4]
        rows = self.data[1:]
        trips = set(self._build_trip(surface, str(i), bonus, *row) for i, row in enumerate(rows))
        objective_cls = HashCodeObjective
        job = Job(trips, objective_cls=objective_cls, *args, **kwargs)
        logger.info(f'Created job!')
        return job

    def _build_trip(self, surface: Surface, identifier: str, bonus: float, x1: float, y1: float, x2: float, y2: float,
                    earliest: float, latest: float) -> Trip:
        origin = surface.get_or_create_position([x1, y1])
        destination = surface.get_or_create_position([x2, y2])
        timeout = latest - earliest
        trip = Trip(identifier, origin, destination, earliest, timeout, bonus)
        logger.debug(f'Created trip!')
        return trip

    def surface(self, *args, **kwargs) -> Surface:
        row = self.data[0]
        rows = row[0]
        columns = row[1]
        surface = GeometricSurface(DistanceMetric.MANHATTAN)
        logger.info(f'Created surface!')
        return surface
