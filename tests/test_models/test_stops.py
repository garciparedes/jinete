import unittest

import jinete as jit

from tests.utils import (
    generate_one_vehicle,
    generate_one_position,
)


class TestStop(unittest.TestCase):

    def test_creation(self):
        vehicle = generate_one_vehicle()
        route = jit.Route(vehicle)

        position = generate_one_position()
        stop = jit.Stop(route, position, None)

        self.assertEqual(stop.route, route)
        self.assertEqual(stop.position, position)
        self.assertEqual(stop.previous, None)

    def test_creation_with_previous(self):
        vehicle = generate_one_vehicle()
        route = jit.Route(vehicle)

        previous_position = generate_one_position()
        previous_stop = jit.Stop(route, previous_position, None)

        position = generate_one_position()
        stop = jit.Stop(route, position, previous_stop)
        previous_stop.following = stop

        self.assertEqual(previous_stop.following, stop)

        self.assertEqual(stop.route, route)
        self.assertEqual(stop.position, position)
        self.assertEqual(stop.previous, previous_stop)
        self.assertEqual(stop.distance, stop.position.distance_to(previous_stop.position))


if __name__ == '__main__':
    unittest.main()
