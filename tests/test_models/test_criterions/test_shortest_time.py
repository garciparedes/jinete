from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

import jinete as jit

from .abc import TestRouteCriterion

if TYPE_CHECKING:
    pass


class TestShortestTimeRouteCriterion(TestRouteCriterion):
    def test_creation(self):
        criterion = jit.ShortestTimeRouteCriterion()
        self.assertEqual(jit.OptimizationDirection.MINIMIZATION, criterion.direction)
        self.assertEqual("Shortest-Time", criterion.name)

    def test_sorting(self):
        criterion = jit.ShortestTimeRouteCriterion()

        self.assertEqual(
            [self.routes[0], self.routes[1], self.routes[2]], criterion.sorted(self.routes),
        )

    def test_scoring(self):
        criterion = jit.ShortestTimeRouteCriterion()

        self.assertEqual(
            4.0, criterion.scoring(self.routes[0]),
        )

        self.assertEqual(
            41.0, criterion.scoring(self.routes[1]),
        )

        self.assertEqual(
            jit.MAX_FLOAT, criterion.scoring(self.routes[2]),
        )

    def test_best(self):
        criterion = jit.ShortestTimeRouteCriterion()

        self.assertEqual(
            self.routes[0], criterion.best(*self.routes),
        )

    def test_nbest(self):
        criterion = jit.ShortestTimeRouteCriterion()

        self.assertEqual(
            [self.routes[0], self.routes[1]], criterion.nbest(2, self.routes),
        )


if __name__ == "__main__":
    unittest.main()
