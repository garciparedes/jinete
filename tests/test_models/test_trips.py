import unittest

import jinete as jit

from tests.utils import (
    generate_one_position,
)


class TestTrips(unittest.TestCase):

    def test_trip(self):
        identifier = str()
        origin = jit.Service(
            position=generate_one_position(),
            earliest=0.0,
        )
        destination = jit.Service(
            position=generate_one_position()
        )

        distance = origin.distance_to(destination)
        duration = origin.time_to(destination)

        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination)

        self.assertEqual(origin.position, trip.origin_position)
        self.assertEqual(destination.position, trip.destination_position)
        self.assertEqual(0.0, trip.origin_earliest)
        self.assertEqual(trip.origin_latest, jit.MAX_FLOAT)
        self.assertEqual(0, trip.origin_duration)
        self.assertEqual(1, trip.capacity)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))

    def test_trip_with_capacity(self):
        identifier = str()
        capacity = 3
        origin = jit.Service(
            position=generate_one_position(),
            earliest=0.0,
        )
        destination = jit.Service(
            position=generate_one_position()
        )

        distance = origin.distance_to(destination)
        duration = origin.time_to(destination)

        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination, capacity=capacity)

        self.assertEqual(origin.position, trip.origin_position)
        self.assertEqual(destination.position, trip.destination_position)
        self.assertEqual(0, trip.origin_earliest)
        self.assertEqual(trip.origin_latest, jit.MAX_FLOAT)
        self.assertEqual(0, trip.origin_duration)
        self.assertEqual(capacity, trip.capacity)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))

    def test_trip_with_timeout(self):
        identifier = str()
        origin = jit.Service(
            position=generate_one_position(),
            earliest=0.0,
            latest=3600,
        )
        destination = jit.Service(
            position=generate_one_position()
        )
        distance = origin.distance_to(destination)
        duration = origin.time_to(destination)

        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination)

        self.assertEqual(origin.position, trip.origin_position)
        self.assertEqual(destination.position, trip.destination_position)
        self.assertEqual(0, trip.origin_earliest)
        self.assertEqual(3600, trip.origin_latest)
        self.assertEqual(0, trip.origin_duration)
        self.assertEqual(1, trip.capacity)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))

    def test_trip_with_load_time(self):
        identifier = str()
        origin = jit.Service(
            position=generate_one_position(),
            earliest=0.0,
            duration=1800,
        )
        destination = jit.Service(
            position=generate_one_position()
        )
        distance = origin.distance_to(destination)
        duration = origin.time_to(destination)

        trip = jit.Trip(identifier=identifier, origin=origin, destination=destination)

        self.assertEqual(origin.position, trip.origin_position)
        self.assertEqual(destination.position, trip.destination_position)
        self.assertEqual(trip.origin_latest, jit.MAX_FLOAT)
        self.assertEqual(1800, trip.origin_duration)
        self.assertEqual(1, trip.capacity)
        self.assertEqual(0.0, trip.origin_earliest)
        self.assertEqual(distance, trip.distance)
        self.assertEqual(duration, trip.duration(trip.origin_earliest))


if __name__ == '__main__':
    unittest.main()
