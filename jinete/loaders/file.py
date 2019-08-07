from __future__ import annotations

import logging
from pathlib import (
    Path,
)

from ..models import (
    Trip,
    Job,
    Vehicle,
    Surface,
    Fleet,
    GeometricSurface,
    METRIC,
)
from .abc import (
    Loader,
)

logger = logging.getLogger(__name__)


class FileLoader(Loader):

    def __init__(self, file_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path

        self._fleet = None
        self._job = None
        self._surface = None

    def synchronize(self):
        with self.file_path.open() as file:
            data = tuple(tuple(int(v) for v in line.split()) for line in file.readlines())
            row = data[0]
            self._surface = self._build_surface(*row[0:2])
            self._fleet = self._build_fleet(row[2], row[5])
            # TODO: Set bonus and number of steps (Config object)
            #
            self._job = self._build_job(data[1:])

    def _build_surface(self, rows: int, columns: int) -> Surface:
        surface = GeometricSurface(METRIC['MANHATTAN'])
        logger.info(f'Created surface!')
        return surface

    def _build_fleet(self, n: int, timeout: float, capacity: int = 1):
        initial = self._surface.get_or_create_position([0, 0])
        vehicles = set(Vehicle(initial, capacity=capacity, timeout=timeout) for _ in range(n))
        fleet = Fleet(vehicles)
        logger.info(f'Created fleet!')
        return fleet

    def _build_job(self, raw, *args, **kwargs):
        trips = set(self._build_trip(str(i), *row) for i, row in enumerate(raw))
        job = Job(trips, *args, **kwargs)
        logger.info(f'Created job!')
        return job

    def _build_trip(self, identifier: str, x1: float, y1: float, x2: float, y2: float, earliest: float,
                    latest: float) -> Trip:
        origin = self._surface.get_or_create_position([x1, y1])
        destination = self._surface.get_or_create_position([x2, y2])
        timeout = latest - earliest
        trip = Trip(identifier, origin, destination, earliest, timeout)
        return trip

    @property
    def fleet(self) -> Fleet:
        if self._fleet is None:
            self.synchronize()
        return self._fleet

    @property
    def job(self) -> Job:
        if self._job is None:
            self.synchronize()
        return self._job

    @property
    def surface(self) -> Surface:
        if self._surface is None:
            self.synchronize()
        return self._surface
