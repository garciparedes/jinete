import unittest

from tests.utils import (
    generate_one_planned_trip,
)


class TestPlannedTrip(unittest.TestCase):

    def test_feasible_planned_trip(self):
        planned_trip = generate_one_planned_trip(True)
        self.assertTrue(planned_trip.feasible)

    def test_not_feasible_planned_trip(self):
        planned_trip = generate_one_planned_trip(False)
        self.assertFalse(planned_trip.feasible)


if __name__ == '__main__':
    unittest.main()
