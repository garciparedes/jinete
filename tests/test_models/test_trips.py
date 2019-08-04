import unittest
from sys import maxsize
from uuid import UUID

import jinete as jit
from .utils import (
    generate_one_position,
)


class TestTrips(unittest.TestCase):

    def test_trip(self):
        identifier = str()
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = 0

        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination, earliest=earliest)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertIsNone(trip.timeout)
        self.assertEqual(trip.latest, maxsize)
        self.assertEqual(0, trip.load_time)
        self.assertEqual(1, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)

    def test_trip_with_capacity(self):
        identifier = str()
        capacity = 3
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = 0

        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination, earliest=earliest,
                        capacity=capacity)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertIsNone(trip.timeout)
        self.assertEqual(trip.latest, maxsize)
        self.assertEqual(0, trip.load_time)
        self.assertEqual(capacity, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)

    def test_trip_with_timeout(self):
        identifier = str()
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = 0
        timeout = 3600
        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination, earliest=earliest,
                        timeout=timeout)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertEqual(timeout, trip.timeout)
        self.assertEqual(earliest + timeout, trip.latest)
        self.assertEqual(0, trip.load_time)
        self.assertEqual(1, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)

    def test_trip_with_load_time(self):
        identifier = str()
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = 0
        load_time = 1800
        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination, earliest=earliest,
                        load_time=load_time)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertIsNone(trip.timeout)
        self.assertEqual(trip.latest, maxsize)
        self.assertEqual(load_time, trip.load_time)
        self.assertEqual(1, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)


if __name__ == '__main__':
    unittest.main()
