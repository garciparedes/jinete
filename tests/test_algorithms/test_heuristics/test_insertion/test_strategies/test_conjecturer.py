import unittest

import jinete as jit

from tests.utils import (
    generate_one_route,
    generate_trips,
    generate_one_trip,
)


class TestStrategy(unittest.TestCase):

    def test_compute_one(self):
        strategy = jit.InsertionStrategy()
        route = generate_one_route()
        trip = generate_one_trip()

        conjectured_route = strategy.compute_one(route, trip)

        self.assertIsInstance(conjectured_route, jit.Route)
        # TODO: Improve assertions

    def test_compute(self):
        strategy = jit.InsertionStrategy()
        route = generate_one_route()
        trips = generate_trips(5)

        conjectured_routes = strategy.compute(route, trips, only_feasible=False)
        self.assertEqual(len(trips), len(conjectured_routes))
        # TODO: Improve assertions

        self.assertEqual(
            sum(route.feasible for route in conjectured_routes),
            len(strategy.compute(route, trips, only_feasible=True)),
        )
        # TODO: Improve assertions


if __name__ == '__main__':
    unittest.main()
