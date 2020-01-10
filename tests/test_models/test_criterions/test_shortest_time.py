from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

import jinete as jit

from .abc import (
    TestRouteCriterion,
)

if TYPE_CHECKING:
    pass


class TestShortestTimeRouteCriterion(TestRouteCriterion):
    def test_creation(self):
        criterion = jit.ShortestTimeRouteCriterion()
        self.assertEqual(jit.OptimizationDirection.MINIMIZATION, criterion.direction)
        self.assertEqual('Shortest-Time', criterion.name)

    def test_sorting(self):
        criterion = jit.ShortestTimeRouteCriterion()

        self.assertEqual(
            self.routes,
            criterion.sorted(reversed(self.routes)),
        )

    def test_scoring(self):
        criterion = jit.ShortestTimeRouteCriterion()

        self.assertEqual(
            4.0,
            criterion.scoring(self.routes[0]),
        )

        self.assertEqual(
            41.0,
            criterion.scoring(self.routes[1]),
        )

    def test_best(self):
        criterion = jit.ShortestTimeRouteCriterion()

        self.assertEqual(
            self.routes[0],
            criterion.best(*self.routes),
        )


if __name__ == '__main__':
    unittest.main()
