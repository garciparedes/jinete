import unittest

import jinete as jit

from tests.utils import (
    generate_one_planned_trip,
    generate_one_vehicle,
)


class TestPlannedTrip(unittest.TestCase):

    def test_feasible_planned_trip(self):
        vehicle = generate_one_vehicle()
        route = jit.Route(vehicle)

        planned_trip = generate_one_planned_trip(True, route)
        self.assertTrue(planned_trip.feasible)

    def test_not_feasible_planned_trip(self):
        vehicle = generate_one_vehicle()
        route = jit.Route(vehicle)

        planned_trip = generate_one_planned_trip(False, route)
        self.assertFalse(planned_trip.feasible)


if __name__ == '__main__':
    unittest.main()
