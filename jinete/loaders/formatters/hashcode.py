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
    Service,
)
from .abc import (
    LoaderFormatter,
)

logger = logging.getLogger(__name__)


class HashCodeLoaderFormatter(LoaderFormatter):

    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        row = self.data[0]
        n, latest, capacity = int(row[2]), row[5], 1.0

        origin = Service(surface.get_or_create_position([0, 0]), latest=latest)
        vehicles = set(Vehicle(str(idx), origin, capacity=capacity) for idx in range(n))
        fleet = Fleet(vehicles)
        logger.info(f'Created fleet!')
        return fleet

    def job(self, surface: Surface, *args, **kwargs) -> Job:
        bonus = self.data[0][4]
        rows = self.data[1:]
        trips = set(self._build_trip(surface, str(i), bonus, *row) for i, row in enumerate(rows))

        kwargs['objective_cls'] = HashCodeObjective
        job = Job(trips, *args, **kwargs)

        logger.info(f'Created job!')
        return job

    def _build_trip(self, surface: Surface, identifier: str, bonus: float, x1: float, y1: float, x2: float, y2: float,
                    earliest: float, latest: float) -> Trip:
        origin = Service(
            position=surface.get_or_create_position([x1, y1]),
            earliest=earliest,
            latest=latest,
        )
        destination = Service(
            position=surface.get_or_create_position([x2, y2]),
        )
        trip = Trip(identifier, on_time_bonus=bonus, origin=origin, destination=destination)
        logger.debug(f'Created trip!')
        return trip

    def surface(self, *args, **kwargs) -> Surface:
        # row = self.data[0]
        # rows = row[0]
        # columns = row[1]
        surface = GeometricSurface(DistanceMetric.MANHATTAN)
        logger.info(f'Created surface!')
        return surface
