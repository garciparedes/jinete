import unittest

import jinete as jit
from tests.utils import generate_one_planned_trip, generate_one_route


class TestJineteException(unittest.TestCase):

    def test_creation(self):
        message = 'This is a test exception'
        exc = jit.JineteException(message)

        self.assertIsInstance(exc, jit.JineteException)
        self.assertEqual(exc.message, message)


class TestStopPlannedTripIterationException(unittest.TestCase):

    def test_creation(self):
        exc = jit.StopPlannedTripIterationException()

        self.assertIsInstance(exc, jit.JineteException)
        self.assertEqual(exc.message, 'There are no more Planned Trips to iterate over them.')


class TestNonFeasiblePlannedTripException(unittest.TestCase):

    def test_creation(self):
        planned_trip = generate_one_planned_trip(False)
        exc = jit.NonFeasiblePlannedTripException(planned_trip)

        self.assertIsInstance(exc, jit.JineteException)
        self.assertEqual(exc.planned_trip, planned_trip)
        self.assertEqual(exc.message, f'Planned Trip "{planned_trip}" is not feasible.')


class TestNonFeasibleRouteException(unittest.TestCase):

    def test_creation(self):
        route = generate_one_route(False)
        exc = jit.NonFeasibleRouteException(route)

        self.assertIsInstance(exc, jit.JineteException)
        self.assertEqual(exc.route, route)
        self.assertEqual(exc.message, f'Route "{route}" is not feasible.')


if __name__ == '__main__':
    unittest.main()
