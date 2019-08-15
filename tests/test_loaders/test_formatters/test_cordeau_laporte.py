import unittest

import jinete as jit


class TestCordeauLaporteLoaderFormatter(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = (
            (1.0, 2.0, 480, 6.0, 90.0),
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
            self.assertEqual(self.data[0][2], vehicle.vehicle_timeout)
            self.assertEqual(self.data[0][3], vehicle.capacity)
            self.assertEqual(self.data[0][4], vehicle.trip_timeout)

            position = vehicle.initial
            self.assertEqual(vehicle.initial, vehicle.final)
            self.assertIsInstance(position, jit.GeometricPosition)
            self.assertEqual(self.data[1][1:3], position.coordinates)

    def test_format_job(self):
        n = int(self.data[0][1] // 2)
        formatter = jit.CordeauLaporteLoaderFormatter(self.data)

        surface = formatter.surface()
        job = formatter.job(surface)
        self.assertIsInstance(job, jit.Job)
        self.assertEqual(n, len(job.trips))

        for idx, trip in enumerate(job.trips):
            origin_row = self.data[2 + idx]
            destination_row = self.data[2 + idx + n]

            if origin_row[-2] == 0.0 and origin_row[-1] == 1440.0:
                earliest, latest = destination_row[-2:]
                inbound = True
            else:
                earliest, latest = origin_row[-2:]
                inbound = False

            self.assertEqual(str(idx), trip.identifier)
            self.assertIsInstance(trip, jit.Trip)
            self.assertEqual(1.0, trip.capacity)
            self.assertEqual(0.0, trip.on_time_bonus)

            self.assertEqual(inbound, trip.inbound)
            self.assertEqual(earliest, trip.earliest)
            self.assertEqual(latest, trip.latest)

            self.assertIsInstance(trip.origin, jit.GeometricPosition)
            self.assertEqual(origin_row[1:3], trip.origin.coordinates)
            self.assertIsInstance(trip.destination, jit.GeometricPosition)
            self.assertEqual(destination_row[1:3], trip.destination.coordinates)


if __name__ == '__main__':
    unittest.main()
