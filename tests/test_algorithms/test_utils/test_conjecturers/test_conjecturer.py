import unittest

import jinete as jit

from tests.utils import (
    generate_one_route,
    generate_trips,
    generate_one_trip,
)


class TestConjecturer(unittest.TestCase):

    def test_compute_one(self):
        conjecturer = jit.Conjecturer()
        route = generate_one_route()
        trip = generate_one_trip()

        conjectured_route = conjecturer.compute_one(route, trip)

        self.assertIsInstance(conjectured_route, jit.Route)
        # TODO: Improve assertions

    def test_compute(self):
        conjecturer = jit.Conjecturer()
        route = generate_one_route()
        trips = generate_trips(5)

        conjectured_routes = conjecturer.compute(route, trips)
        self.assertEqual(len(trips), len(conjectured_routes))
        # TODO: Improve assertions


if __name__ == '__main__':
    unittest.main()
