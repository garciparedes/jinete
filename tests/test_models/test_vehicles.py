import unittest
from uuid import UUID

import jinete as jit

from tests.utils import (
    generate_one_position,
)


class TestVehicles(unittest.TestCase):

    def test_vehicle(self):
        initial = generate_one_position()
        identifier = str(0)
        vehicle = jit.Vehicle(identifier, initial)

        self.assertEqual(identifier, vehicle.identifier)
        self.assertEqual(1, vehicle.capacity)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, 0)
        self.assertEqual(vehicle.latest, jit.MAX_FLOAT)
        self.assertEqual(vehicle.timeout, jit.MAX_FLOAT)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_capacity(self):
        capacity = 3
        initial = generate_one_position()
        identifier = str(0)
        vehicle = jit.Vehicle(identifier, initial, capacity=capacity)

        self.assertEqual(vehicle.capacity, capacity)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, 0)
        self.assertEqual(vehicle.latest, jit.MAX_FLOAT)
        self.assertEqual(vehicle.timeout, jit.MAX_FLOAT)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_final(self):
        capacity = 3
        initial = generate_one_position()
        final = generate_one_position()
        identifier = str(0)
        vehicle = jit.Vehicle(identifier, initial, capacity=capacity, final=final)

        self.assertEqual(identifier, vehicle.identifier)
        self.assertEqual(vehicle.capacity, capacity)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, final)
        self.assertEqual(vehicle.earliest, 0)
        self.assertEqual(vehicle.latest, jit.MAX_FLOAT)
        self.assertEqual(vehicle.timeout, jit.MAX_FLOAT)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_earliest(self):
        initial = generate_one_position()
        earliest = 3600
        identifier = str(0)
        vehicle = jit.Vehicle(identifier, initial, earliest=earliest)

        self.assertEqual(identifier, vehicle.identifier)
        self.assertEqual(vehicle.capacity, 1, )
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, earliest)
        self.assertEqual(vehicle.latest, jit.MAX_FLOAT)
        self.assertEqual(vehicle.timeout, jit.MAX_FLOAT)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_vehicle_with_timeout(self):
        initial = generate_one_position()
        earliest = 1800
        timeout = 3600
        identifier = str(0)
        vehicle = jit.Vehicle(identifier, initial, earliest=earliest, timeout=timeout)

        self.assertEqual(identifier, vehicle.identifier)
        self.assertEqual(vehicle.capacity, 1)
        self.assertEqual(vehicle.initial, initial)
        self.assertEqual(vehicle.final, vehicle.initial)
        self.assertEqual(vehicle.earliest, earliest)
        self.assertEqual(vehicle.latest, earliest + timeout)
        self.assertEqual(vehicle.timeout, timeout)
        self.assertIsInstance(vehicle.uuid, UUID)

    def test_as_dict(self):
        initial = generate_one_position()
        identifier = str(0)
        vehicle = jit.Vehicle(identifier, initial)

        expected = {
            'initial': vehicle.initial,
            'final': vehicle.final,
            'capacity': vehicle.capacity,
            'earliest': vehicle.earliest,
            'timeout': vehicle.timeout,
            'route_timeout': vehicle.route_timeout,
            'trip_timeout': vehicle.trip_timeout,
            'latest': vehicle.latest,
            'uuid': vehicle.uuid,
        }

        self.assertEqual(expected, vehicle.as_dict())

if __name__ == '__main__':
    unittest.main()
