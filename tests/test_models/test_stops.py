import unittest

import jinete as jit

from tests.utils import (
    generate_one_vehicle,
    generate_one_position,
    generate_one_route)


class TestStop(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.vehicle = generate_one_vehicle()
        cls.route = jit.Route(cls.vehicle)

        cls.position = generate_one_position()

    def test_creation(self):
        stop = jit.Stop(self.route, self.position, None)

        self.assertEqual(stop.route, self.route)
        self.assertEqual(stop.position, self.position)
        self.assertEqual(stop.previous, None)
        self.assertEqual(stop.previous_position, self.vehicle.initial)
        self.assertEqual(stop.previous_departure_time, self.vehicle.earliest)
        self.assertEqual(
            stop.navigation_time,
            stop.position.time_to(self.vehicle.initial, stop.previous_departure_time),
        )
        self.assertEqual(stop.waiting_time, 0.0)
        self.assertEqual(stop.down_time, 0.0)
        self.assertEqual(stop.load_time, 0.0)

    def test_creation_with_previous(self):
        previous_position = generate_one_position()
        previous_stop = jit.Stop(self.route, previous_position, None)

        stop = jit.Stop(self.route, self.position, previous_stop)
        previous_stop.following = stop

        self.assertEqual(previous_stop.following, stop)

        self.assertEqual(stop.route, self.route)
        self.assertEqual(stop.position, self.position)
        self.assertEqual(stop.previous, previous_stop)
        self.assertEqual(stop.distance, stop.position.distance_to(previous_stop.position))
        self.assertEqual(stop.previous_position, previous_stop.position)
        self.assertEqual(stop.previous_departure_time, previous_stop.departure_time)
        self.assertEqual(
            stop.navigation_time,
            stop.position.time_to(previous_stop.position, stop.previous_departure_time),
        )

    def test_stops(self):
        route = generate_one_route()
        stop = route.stops[0]
        self.assertEqual(route.stops, stop.stops)

    def test_flush(self):
        stop = jit.Stop(self.route, self.position, None)

        self.assertIsNone(stop._down_time)
        self.assertIsNone(stop._load_time)
        self.assertIsNone(stop._earliest)
        self.assertIsNone(stop._arrival_time)

        self.assertIsInstance(stop.departure_time, float)

        self.assertIsNotNone(stop._down_time)
        self.assertIsNotNone(stop._load_time)
        self.assertIsNotNone(stop._earliest)
        self.assertIsNotNone(stop._arrival_time)

        stop.flush()

        self.assertIsNone(stop._down_time)
        self.assertIsNone(stop._load_time)
        self.assertIsNone(stop._earliest)
        self.assertIsNone(stop._arrival_time)

    def test_all_following(self):
        stop0 = jit.Stop(self.route, self.position, None)

        stop1 = jit.Stop(self.route, generate_one_position(), stop0)
        stop0.following = stop1

        stop2 = jit.Stop(self.route, generate_one_position(), stop1)
        stop1.following = stop2

        stop3 = jit.Stop(self.route, generate_one_position(), stop2)
        stop2.following = stop3

        stop4 = jit.Stop(self.route, generate_one_position(), stop3)
        stop3.following = stop4

        stops = [stop0, stop1, stop2, stop3, stop4]

        for stop in stops:
            self.assertIsNone(stop._down_time)
            self.assertIsNone(stop._load_time)
            self.assertIsNone(stop._earliest)
            self.assertIsNone(stop._arrival_time)

        self.assertIsInstance(stops[-1].departure_time, float)

        for stop in stops:
            self.assertIsNotNone(stop._down_time)
            self.assertIsNotNone(stop._load_time)
            self.assertIsNotNone(stop._earliest)
            self.assertIsNotNone(stop._arrival_time)

        stop2.flush_all_following()

        for stop in stops[:2]:
            self.assertIsNotNone(stop._down_time)
            self.assertIsNotNone(stop._load_time)
            self.assertIsNotNone(stop._earliest)
            self.assertIsNotNone(stop._arrival_time)
        for stop in stops[2:]:
            self.assertIsNone(stop._down_time)
            self.assertIsNone(stop._load_time)
            self.assertIsNone(stop._earliest)
            self.assertIsNone(stop._arrival_time)

    def test_all_previous(self):
        stop0 = jit.Stop(self.route, self.position, None)

        stop1 = jit.Stop(self.route, generate_one_position(), stop0)
        stop0.following = stop1

        stop2 = jit.Stop(self.route, generate_one_position(), stop1)
        stop1.following = stop2

        stop3 = jit.Stop(self.route, generate_one_position(), stop2)
        stop2.following = stop3

        stop4 = jit.Stop(self.route, generate_one_position(), stop3)
        stop3.following = stop4

        stops = [stop0, stop1, stop2, stop3, stop4]

        for stop in stops:
            self.assertIsNone(stop._down_time)
            self.assertIsNone(stop._load_time)
            self.assertIsNone(stop._earliest)
            self.assertIsNone(stop._arrival_time)

        self.assertIsInstance(stops[-1].departure_time, float)

        for stop in stops:
            self.assertIsNotNone(stop._down_time)
            self.assertIsNotNone(stop._load_time)
            self.assertIsNotNone(stop._earliest)
            self.assertIsNotNone(stop._arrival_time)

        stop2.flush_all_previous()

        for stop in stops[:3]:
            self.assertIsNone(stop._down_time)
            self.assertIsNone(stop._load_time)
            self.assertIsNone(stop._earliest)
            self.assertIsNone(stop._arrival_time)

        for stop in stops[3:]:
            self.assertIsNotNone(stop._down_time)
            self.assertIsNotNone(stop._load_time)
            self.assertIsNotNone(stop._earliest)
            self.assertIsNotNone(stop._arrival_time)


if __name__ == '__main__':
    unittest.main()
