import unittest

import jinete as jit

from tests.utils import (
    generate_one_position,
)


class TestTrips(unittest.TestCase):

    def test_trip(self):
        identifier = str()
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = 0
        distance = origin.distance_to(destination)
        duration = origin.time_to(destination, earliest)

        trip = jit.Trip(identifier=identifier, origin_position=origin, destination_position=destination, origin_earliest=earliest)

        self.assertEqual(origin, trip.origin_position)
        self.assertEqual(destination, trip.destination_position)
        self.assertEqual(earliest, trip.origin_earliest)
        self.assertEqual(trip.origin_latest, jit.MAX_FLOAT)
        self.assertEqual(0, trip.origin_duration)
        self.assertEqual(1, trip.capacity)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))

    def test_trip_with_capacity(self):
        identifier = str()
        capacity = 3
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = 0
        distance = origin.distance_to(destination)
        duration = origin.time_to(destination, earliest)

        trip = jit.Trip(identifier=identifier, origin_position=origin, destination_position=destination, origin_earliest=earliest,
                        capacity=capacity)

        self.assertEqual(origin, trip.origin_position)
        self.assertEqual(destination, trip.destination_position)
        self.assertEqual(earliest, trip.origin_earliest)
        self.assertEqual(trip.origin_latest, jit.MAX_FLOAT)
        self.assertEqual(0, trip.origin_duration)
        self.assertEqual(capacity, trip.capacity)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))

    def test_trip_with_timeout(self):
        identifier = str()
        origin = generate_one_position()
        destination = generate_one_position()
        earliest = 0
        timeout = 3600
        distance = origin.distance_to(destination)
        duration = origin.time_to(destination, earliest)

        trip = jit.Trip(identifier=identifier, origin_position=origin, destination_position=destination, origin_earliest=earliest,
                        origin_latest=earliest + timeout)

        self.assertEqual(origin, trip.origin_position)
        self.assertEqual(destination, trip.destination_position)
        self.assertEqual(earliest, trip.origin_earliest)
        self.assertEqual(earliest + timeout, trip.origin_latest)
        self.assertEqual(0, trip.origin_duration)
        self.assertEqual(1, trip.capacity)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))

    def test_trip_with_load_time(self):
        identifier = str()
        origin = generate_one_position()
        earliest = 0
        load_time = 1800
        destination = generate_one_position()
        distance = origin.distance_to(destination)
        duration = origin.time_to(destination, earliest)

        trip = jit.Trip(identifier=identifier, origin_position=origin, destination_position=destination, origin_earliest=earliest,
                        origin_duration=load_time)

        self.assertEqual(origin, trip.origin_position)
        self.assertEqual(destination, trip.destination_position)
        self.assertEqual(trip.origin_latest, jit.MAX_FLOAT)
        self.assertEqual(load_time, trip.origin_duration)
        self.assertEqual(1, trip.capacity)
        self.assertEqual(earliest, trip.origin_earliest)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))


if __name__ == '__main__':
    unittest.main()
