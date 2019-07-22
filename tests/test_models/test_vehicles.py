import unittest
from datetime import datetime, timedelta
from uuid import UUID

from rider import (
    Vehicle,
)
from .utils import (
    generate_one_position,
)


class TestVehicles(unittest.TestCase):

    def test_vehicle(self):
        initial = generate_one_position()
        vehicle = Vehicle(initial=initial)

        self.assertEqual(1, vehicle.capacity)
        self.assertEqual(initial, vehicle.initial)
        self.assertIsNone(vehicle.final)
        self.assertIsNone(vehicle.earliest)
        self.assertIsNone(vehicle.latest)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_capacity(self):
        capacity = 3
        initial = generate_one_position()
        vehicle = Vehicle(capacity=capacity, initial=initial)

        self.assertEqual(capacity, vehicle.capacity)
        self.assertEqual(initial, vehicle.initial)
        self.assertIsNone(vehicle.final)
        self.assertIsNone(vehicle.earliest)
        self.assertIsNone(vehicle.latest)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_final(self):
        capacity = 3
        initial = generate_one_position()
        final = generate_one_position()
        vehicle = Vehicle(capacity=capacity, initial=initial, final=final)

        self.assertEqual(capacity, vehicle.capacity)
        self.assertEqual(initial, vehicle.initial)
        self.assertEqual(final, vehicle.final)
        self.assertIsNone(vehicle.earliest)
        self.assertIsNone(vehicle.latest)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_earliest(self):
        initial = generate_one_position()
        earliest = datetime.now()

        vehicle = Vehicle(initial=initial, earliest=earliest)

        self.assertEqual(1, vehicle.capacity)
        self.assertEqual(initial, vehicle.initial)
        self.assertIsNone(vehicle.final)
        self.assertEqual(earliest, vehicle.earliest)
        self.assertIsNone(vehicle.latest)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_latest(self):
        initial = generate_one_position()
        latest = datetime.now()

        vehicle = Vehicle(initial=initial, latest=latest)

        self.assertEqual(1, vehicle.capacity)
        self.assertEqual(initial, vehicle.initial)
        self.assertIsNone(vehicle.final)
        self.assertIsNone(vehicle.earliest)
        self.assertEqual(latest, vehicle.latest)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_timeout(self):
        initial = generate_one_position()
        timeout = timedelta(hours=8)

        vehicle = Vehicle(initial=initial, timeout=timeout)

        self.assertEqual(1, vehicle.capacity)
        self.assertEqual(initial, vehicle.initial)
        self.assertIsNone(vehicle.final)
        self.assertIsNone(vehicle.earliest)
        self.assertIsNone(vehicle.latest)
        self.assertEqual(timeout, vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)


if __name__ == '__main__':
    unittest.main()
