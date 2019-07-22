import unittest
from datetime import datetime, timedelta
from uuid import UUID

from ride import (
    Vehicle,
    Trip)
from .utils import (
    generate_one_position,
)


class TestTrips(unittest.TestCase):

    def test_trip(self):
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = datetime.now()

        trip = Trip(origin=origin, destination=destination, earliest=earliest)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertIsNone(trip.timeout)
        self.assertIsNone(trip.latest)
        self.assertEqual(timedelta(0), trip.load_time)
        self.assertEqual(1, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)

    def test_trip_with_capacity(self):
        capacity = 3
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = datetime.now()

        trip = Trip(origin=origin, destination=destination, earliest=earliest, capacity=capacity)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertIsNone(trip.timeout)
        self.assertIsNone(trip.latest)
        self.assertEqual(timedelta(0), trip.load_time)
        self.assertEqual(capacity, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)

    def test_trip_with_timeout(self):
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = datetime.now()
        timeout = timedelta(hours=1)
        trip = Trip(origin=origin, destination=destination, earliest=earliest, timeout=timeout)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertEqual(timeout, trip.timeout)
        self.assertEqual(earliest + timeout, trip.latest)
        self.assertEqual(timedelta(0), trip.load_time)
        self.assertEqual(1, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)

    def test_trip_with_load_time(self):
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = datetime.now()
        load_time = timedelta(minutes=30)
        trip = Trip(origin=origin, destination=destination, earliest=earliest, load_time=load_time)

        self.assertEqual(origin, trip.origin)
        self.assertEqual(destination, trip.destination)
        self.assertEqual(earliest, trip.earliest)
        self.assertIsNone(trip.timeout)
        self.assertIsNone(trip.latest)
        self.assertEqual(load_time, trip.load_time)
        self.assertEqual(1, trip.capacity)
        self.assertIsInstance(trip.uuid, UUID)


if __name__ == '__main__':
    unittest.main()
