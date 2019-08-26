import unittest
from uuid import UUID

import jinete as jit

from tests.utils import (
    generate_one_vehicle,
    generate_one_route,
)


class TestRoutes(unittest.TestCase):

    def test_route(self):
        vehicle = generate_one_vehicle()
        route = jit.Route(vehicle)
        self.assertIsInstance(route.uuid, UUID)
        self.assertEqual(list(), list(route.planned_trips))
        self.assertEqual(vehicle, route.vehicle)

    def test_feasible_route(self):
        route = generate_one_route(True)
        self.assertTrue(route.feasible)

    def test_not_feasible_route(self):
        route = generate_one_route(False)
        self.assertFalse(route.feasible)


if __name__ == '__main__':
    unittest.main()
