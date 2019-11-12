from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
import jinete as jit
from .abc import (
    TestRouteCriterion,
)

if TYPE_CHECKING:
    pass


class TestLongestTimePlannedTripCriterion(TestRouteCriterion):

    def test_creation(self):
        criterion = jit.LongestTimeRouteCriterion()
        self.assertEqual(jit.OptimizationDirection.MAXIMIZATION, criterion.direction)
        self.assertEqual('Longest-Time', criterion.name)

    def test_sorting(self):
        criterion = jit.LongestTimeRouteCriterion()

        self.assertEqual(
            self.routes[::-1],
            criterion.sorted(self.routes),
        )

    def test_scoring(self):
        criterion = jit.LongestTimeRouteCriterion()

        self.assertEqual(
            4.0,
            criterion.scoring(self.routes[0]),
        )

        self.assertEqual(
            41.0,
            criterion.scoring(self.routes[1]),
        )

    def test_best(self):
        criterion = jit.LongestTimeRouteCriterion()

        self.assertEqual(
            self.routes[1],
            criterion.best(*self.routes),
        )


if __name__ == '__main__':
    unittest.main()
