import unittest
from sys import maxsize
from uuid import UUID

import jinete as jit
from .utils import (
    generate_one_position,
)


class TestVehicles(unittest.TestCase):

    def test_vehicle(self):
        initial = generate_one_position()
        vehicle = jit.Vehicle(initial)

        self.assertEqual(1, vehicle.capacity)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, 0)
        self.assertEqual(vehicle.latest, maxsize)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_capacity(self):
        capacity = 3
        initial = generate_one_position()
        vehicle = jit.Vehicle(initial, capacity=capacity)

        self.assertEqual(vehicle.capacity, capacity)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, 0)
        self.assertEqual(vehicle.latest, maxsize)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_final(self):
        capacity = 3
        initial = generate_one_position()
        final = generate_one_position()
        vehicle = jit.Vehicle(initial, capacity=capacity, final=final)

        self.assertEqual(vehicle.capacity, capacity)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, final)
        self.assertEqual(vehicle.earliest, 0)
        self.assertEqual(vehicle.latest, maxsize)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_earliest(self):
        initial = generate_one_position()
        earliest = 3600

        vehicle = jit.Vehicle(initial, earliest=earliest)

        self.assertEqual(vehicle.capacity, 1, )
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, earliest)
        self.assertEqual(vehicle.latest, maxsize)
        self.assertIsNone(vehicle.timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_timeout(self):
        initial = generate_one_position()
        earliest = 1800
        timeout = 3600

        vehicle = jit.Vehicle(initial, earliest=earliest, timeout=timeout)

        self.assertEqual(vehicle.capacity, 1)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, earliest)
        self.assertEqual(vehicle.latest, earliest + timeout)
        self.assertEqual(vehicle.timeout, timeout)
        self.assertIsInstance(vehicle.uuid, UUID)


if __name__ == '__main__':
    unittest.main()
