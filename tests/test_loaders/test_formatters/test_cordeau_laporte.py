from __future__ import annotations

import unittest
from operator import attrgetter
from typing import TYPE_CHECKING
import jinete as jit

if TYPE_CHECKING:
    from typing import (
        Tuple,
    )


class TestCordeauLaporteLoaderFormatter(unittest.TestCase):
    data: Tuple[Tuple[float, ...], ...]

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = (
            (1.0, 4.0, 480, 6.0, 90.0),
            (0.0, -1.044, 2.000, 0.0, 0.0, 0.0, 1440.0),
            (1.0, -2.973, 6.414, 10.0, 1.0, 0.0, 1440.0),
            (2.0, -7.667, 9.934, 10.0, 1.0, 325.0, 358.0),
            (3.0, -5.476, 1.437, 10.0, -1.0, 258.0, 287.0),
            (4.0, 0.435, 1.469, 10.0, -1.0, 0.0, 1440.0),
        )

    def test_creation(self):
        formatter = jit.CordeauLaporteLoaderFormatter(self.data)
        self.assertEqual(formatter.data, self.data)

    def test_format_surface(self):
        formatter = jit.CordeauLaporteLoaderFormatter(self.data)

        surface = formatter.surface()
        self.assertIsInstance(surface, jit.GeometricSurface)
        self.assertEqual(0, len(surface.positions))

    def test_format_fleet(self):
        formatter = jit.CordeauLaporteLoaderFormatter(self.data)

        surface = formatter.surface()
        fleet = formatter.fleet(surface)
        self.assertIsInstance(fleet, jit.Fleet)
        self.assertEqual(int(self.data[0][0]), len(fleet.vehicles))

        for idx, vehicle in enumerate(fleet.vehicles):
            self.assertEqual(str(idx), vehicle.identifier)
            self.assertIsInstance(vehicle, jit.Vehicle)
            self.assertEqual(self.data[0][2], vehicle.timeout)
            self.assertEqual(self.data[0][3], vehicle.capacity)

            position = vehicle.origin_position
            self.assertEqual(vehicle.origin_position, vehicle.destination_position)
            self.assertIsInstance(position, jit.GeometricPosition)
            self.assertEqual(self.data[1][1:3], position.coordinates)

    def test_format_job(self):
        n = int(self.data[0][1] // 2)
        formatter = jit.CordeauLaporteLoaderFormatter(self.data)

        surface = formatter.surface()
        job = formatter.job(surface)
        self.assertIsInstance(job, jit.Job)
        self.assertEqual(n, len(job.trips))

        for idx, trip in enumerate(sorted(job.trips, key=attrgetter('identifier'))):
            origin_row = self.data[2 + idx]
            destination_row = self.data[2 + idx + n]

            origin_earliest, origin_latest = origin_row[-2:]
            destination_earliest, destination_latest = destination_row[-2:]

            self.assertEqual(str(idx + 1), trip.identifier)
            self.assertEqual(self.data[0][4], trip.timeout)
            self.assertIsInstance(trip, jit.Trip)
            self.assertEqual(1.0, trip.capacity)
            self.assertEqual(0.0, trip.on_time_bonus)

            self.assertEqual(origin_earliest, trip.origin_earliest)
            self.assertEqual(origin_latest, trip.origin_latest)

            self.assertEqual(destination_earliest, trip.destination_earliest)
            self.assertEqual(destination_latest, trip.destination_latest)

            self.assertIsInstance(trip.origin_position, jit.GeometricPosition)
            self.assertEqual(origin_row[1:3], trip.origin_position.coordinates)
            self.assertIsInstance(trip.destination_position, jit.GeometricPosition)
            self.assertEqual(destination_row[1:3], trip.destination_position.coordinates)


if __name__ == '__main__':
    unittest.main()
