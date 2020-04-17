import unittest

import jinete as jit

from tests.utils import (
    generate_one_route,
    generate_trips,
)


class TestSamplingStrategy(unittest.TestCase):
    def test_compute(self):
        strategy = jit.SamplingInsertionStrategy()
        route = generate_one_route(planned_trips_min=10)
        trips = generate_trips(5)

        conjectured_routes = strategy.compute(route, trips)  # noqa
        self.assertTrue(True)
        # TODO: Improve assertions


if __name__ == "__main__":
    unittest.main()
