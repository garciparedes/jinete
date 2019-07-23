import unittest
from uuid import UUID

import jinete as jit

from .utils import (
    generate_trips,
    generate_one_vehicle,
)


class TestRoutes(unittest.TestCase):

    def test_route(self):
        planned_trips = tuple()
        vehicle = generate_one_vehicle()
        route = jit.Route(planned_trips, vehicle)
        self.assertIsInstance(route.uuid, UUID)
        self.assertEqual(planned_trips, route.planned_trips)
        self.assertEqual(vehicle, route.vehicle)


if __name__ == '__main__':
    unittest.main()
