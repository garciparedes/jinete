import unittest

import jinete as jit
from .abc import TestObjective


class TestTaxiSharingObjective(TestObjective):
    def test_creation(self):
        objective = jit.TaxiSharingObjective()
        self.assertEqual("Taxi-Sharing", objective.name)

    def test_result(self):
        objective = jit.TaxiSharingObjective()

        self.assertEqual(
            (20.0,), objective.optimization_function(self.result),
        )

    def test_planning(self):
        objective = jit.TaxiSharingObjective()

        self.assertEqual(
            (20.0,), objective.optimization_function(self.planning),
        )

    def test_route(self):
        objective = jit.TaxiSharingObjective()

        self.assertEqual(
            (20.0,), objective.optimization_function(self.route),
        )

    def test_stop(self):
        objective = jit.TaxiSharingObjective()

        self.assertEqual(
            (2.0,), objective.optimization_function(self.stop),
        )

    def test_planning_trip(self):
        objective = jit.TaxiSharingObjective()

        self.assertEqual(
            (2.0,), objective.optimization_function(self.planned_trip),
        )

    def test_best(self):
        objective = jit.TaxiSharingObjective()

        self.assertEqual(
            tuple(self.route.planned_trips)[1], objective.best(*self.route.planned_trips),
        )


if __name__ == "__main__":
    unittest.main()
