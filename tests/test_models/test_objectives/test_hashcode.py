import unittest

import jinete as jit
from .abc import TestObjective


class TestHashCodeObjective(TestObjective):
    def test_creation(self):
        objective = jit.HashCodeObjective()
        self.assertEqual("HashCode-2018", objective.name)

    def test_result(self):
        objective = jit.HashCodeObjective()

        self.assertEqual(
            (20.0,), objective.optimization_function(self.result),
        )

    def test_planning(self):
        objective = jit.HashCodeObjective()

        self.assertEqual(
            (20.0,), objective.optimization_function(self.planning),
        )

    def test_route(self):
        objective = jit.HashCodeObjective()

        self.assertEqual(
            (20.0,), objective.optimization_function(self.route),
        )

    def test_stop(self):
        objective = jit.HashCodeObjective()

        self.assertEqual(
            (2.0,), objective.optimization_function(self.stop),
        )

    def test_planning_trip(self):
        objective = jit.HashCodeObjective()

        self.assertEqual(
            (2.0,), objective.optimization_function(self.planned_trip),
        )

    def test_best(self):
        objective = jit.HashCodeObjective()

        self.assertEqual(
            tuple(self.route.planned_trips)[1], objective.best(*self.route.planned_trips),
        )


if __name__ == "__main__":
    unittest.main()
