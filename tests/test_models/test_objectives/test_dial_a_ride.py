import unittest

import jinete as jit
from .abc import (
    TestObjective,
)


class TestDialARideObjective(TestObjective):

    def test_creation(self):
        objective = jit.DialARideObjective()
        self.assertEqual('Dial-a-Ride', objective.name)

    def test_result(self):
        objective = jit.DialARideObjective()

        self.assertEqual(
            (2, -40.0),
            objective.optimization_function(self.result),
        )

    def test_planning(self):
        objective = jit.DialARideObjective()

        self.assertEqual(
            (2, -40.0),
            objective.optimization_function(self.planning),
        )

    def test_route(self):
        objective = jit.DialARideObjective()

        self.assertEqual(
            (2, -40.0),
            objective.optimization_function(self.route),
        )

    def test_stop(self):
        objective = jit.DialARideObjective()

        self.assertEqual(
            (1, -2.0),
            objective.optimization_function(self.stop),
        )

    def test_planning_trip(self):
        objective = jit.DialARideObjective()

        self.assertEqual(
            (1, -2.0),
            objective.optimization_function(self.planned_trip),
        )

    def test_best(self):
        objective = jit.DialARideObjective()

        self.assertEqual(
            next(self.route.planned_trips),
            objective.best(*self.route.planned_trips),
        )


if __name__ == '__main__':
    unittest.main()
