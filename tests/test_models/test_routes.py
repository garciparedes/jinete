import unittest
from uuid import UUID

import jinete as jit

from tests.utils import (
    generate_one_vehicle,
    generate_one_route,
    generate_one_planned_trip,
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

    def test_un_finish(self):
        route = generate_one_route()
        vehicle = route.vehicle

        self.assertEqual(vehicle.destination_position, route.last_position)
        route.un_finish()
        self.assertNotEqual(vehicle.destination_position, route.last_position)

        stops_count = len(route.stops)
        route.un_finish()
        self.assertEqual(stops_count, len(route.stops))

        planned_trip = generate_one_planned_trip(
            feasible=True,
            route=route,
            earliest=route.last_departure_time,
            origin=route.last_position,
            destination=vehicle.destination_position,
        )
        route.append_planned_trip(planned_trip)
        self.assertEqual(vehicle.destination_position, route.last_position)

        stops_count = len(route.stops)
        route.un_finish()
        self.assertEqual(stops_count, len(route.stops))


if __name__ == '__main__':
    unittest.main()
