import unittest

import jinete as jit

from tests.utils import (
    generate_one_position,
)


class TestVehicles(unittest.TestCase):

    def test_construction(self):
        identifier = str(0)
        service = jit.Service(
            position=generate_one_position(),
            earliest=1800,
            latest=3600,
            duration=60,
        )
        vehicle = jit.Vehicle(identifier, service)

        self.assertEqual(identifier, vehicle.identifier)
        self.assertEqual(1, vehicle.capacity)

        self.assertEqual(service, vehicle.origin)
        self.assertEqual(service.position, vehicle.origin_position)
        self.assertEqual(service.earliest, vehicle.origin_earliest)
        self.assertEqual(service.latest, vehicle.origin_latest)
        self.assertEqual(service.duration, vehicle.origin_duration)

        self.assertEqual(service, vehicle.destination)
        self.assertEqual(service.position, vehicle.destination_position)
        self.assertEqual(service.earliest, vehicle.destination_earliest)
        self.assertEqual(service.latest, vehicle.destination_latest)
        self.assertEqual(service.duration, vehicle.destination_duration)

    def test_construction_with_capacity(self):
        capacity = 3
        service = jit.Service(
            position=generate_one_position(),
            earliest=1800,
            latest=3600,
            duration=60,
        )
        identifier = str(0)
        vehicle = jit.Vehicle(identifier, service, capacity=capacity)

        self.assertEqual(identifier, vehicle.identifier)
        self.assertEqual(capacity, vehicle.capacity)

        self.assertEqual(service, vehicle.origin)
        self.assertEqual(service.position, vehicle.origin_position)
        self.assertEqual(service.earliest, vehicle.origin_earliest)
        self.assertEqual(service.latest, vehicle.origin_latest)
        self.assertEqual(service.duration, vehicle.origin_duration)

        self.assertEqual(service, vehicle.destination)
        self.assertEqual(service.position, vehicle.destination_position)
        self.assertEqual(service.earliest, vehicle.destination_earliest)
        self.assertEqual(service.latest, vehicle.destination_latest)
        self.assertEqual(service.duration, vehicle.destination_duration)

    def test_vehicle_with_final(self):
        identifier = str(0)
        origin = jit.Service(
            position=generate_one_position(),
            earliest=100,
            latest=200,
            duration=2,
        )
        destination = jit.Service(
            position=generate_one_position(),
            earliest=1000,
            latest=2000,
            duration=20,
        )
        vehicle = jit.Vehicle(identifier, origin, destination)

        self.assertEqual(identifier, vehicle.identifier)
        self.assertEqual(1, vehicle.capacity)

        self.assertEqual(origin, vehicle.origin)
        self.assertEqual(origin.position, vehicle.origin_position)
        self.assertEqual(origin.earliest, vehicle.origin_earliest)
        self.assertEqual(origin.latest, vehicle.origin_latest)
        self.assertEqual(origin.duration, vehicle.origin_duration)

        self.assertEqual(destination, vehicle.destination)
        self.assertEqual(destination.position, vehicle.destination_position)
        self.assertEqual(destination.earliest, vehicle.destination_earliest)
        self.assertEqual(destination.latest, vehicle.destination_latest)
        self.assertEqual(destination.duration, vehicle.destination_duration)

    def test_as_tuple(self):
        identifier = str(0)
        origin = jit.Service(
            position=generate_one_position(),
            earliest=100,
            latest=200,
            duration=2,
        )
        destination = jit.Service(
            position=generate_one_position(),
            earliest=1000,
            latest=2000,
            duration=20,
        )
        capacity = 44
        vehicle = jit.Vehicle(identifier, origin, destination, capacity)

        expected = (
            ('identifier', identifier),
            ('origin', tuple(origin)),
            ('destination', tuple(destination)),
            ('capacity', capacity),
            ('timeout', vehicle.timeout),
        )

        self.assertEqual(expected, tuple(vehicle))


if __name__ == '__main__':
    unittest.main()
