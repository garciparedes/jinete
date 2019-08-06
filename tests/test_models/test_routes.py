import unittest
from uuid import UUID

import jinete as jit

from .utils import (
    generate_one_vehicle,
    generate_one_route,
)


class TestRoutes(unittest.TestCase):

    def test_route(self):
        planned_trips = list()
        vehicle = generate_one_vehicle()
        route = jit.Route(vehicle, planned_trips)
        self.assertIsInstance(route.uuid, UUID)
        self.assertEqual(planned_trips, route.planned_trips)
        self.assertEqual(vehicle, route.vehicle)

    def test_feasible_route(self):
        route = generate_one_route(True)
        self.assertTrue(route.feasible)

    def test_not_feasible_route(self):
        route = generate_one_route(False)
        self.assertFalse(route.feasible)


if __name__ == '__main__':
    unittest.main()
