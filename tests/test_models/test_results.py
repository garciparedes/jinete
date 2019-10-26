from __future__ import annotations

import unittest
from typing import (
    TYPE_CHECKING,
)

import jinete as jit

from tests.utils import (
    generate_one_planning,
)

if TYPE_CHECKING:
    from typing import (
        Type,
    )


class TestResult(unittest.TestCase):
    planning: jit.Planning
    fleet: jit.Fleet
    job: jit.Job
    algorithm_cls: Type[jit.Algorithm]
    computation_time: float

    @classmethod
    def setUpClass(cls) -> None:
        cls.planning = generate_one_planning()
        cls.fleet = jit.Fleet(set(cls.planning.vehicles))
        cls.job = jit.Job(set(cls.planning.trips), jit.DialARideObjective)
        cls.algorithm_cls = jit.Algorithm
        cls.computation_time = 1

    def test_construction(self):
        result = jit.Result(
            fleet=self.fleet,
            job=self.job,
            algorithm_cls=self.algorithm_cls,
            planning=self.planning,
            computation_time=self.computation_time
        )

        self.assertIsInstance(result, jit.Result)
        self.assertEqual(self.fleet, result.fleet)
        self.assertEqual(self.fleet.vehicles, result.vehicles)

        self.assertEqual(self.job, result.job)
        self.assertEqual(self.job.trips, result.trips)
        self.assertEqual(self.job.objective, result.objective)
        self.assertEqual(self.job.objective.optimization_function(result), result.optimization_function)
        self.assertEqual(self.job.objective.direction, result.direction)

        self.assertEqual(self.algorithm_cls, result.algorithm_cls)

        self.assertEqual(self.planning, result.planning)
        self.assertEqual(self.planning.uuid, result.planning_uuid)
        self.assertEqual(self.planning.routes, result.routes)

        self.assertEqual(self.computation_time, result.computation_time)

    def test_as_tuple(self):
        result = jit.Result(
            fleet=self.fleet,
            job=self.job,
            algorithm_cls=self.algorithm_cls,
            planning=self.planning,
            computation_time=self.computation_time
        )

        expected = (
            ('fleet_uuid', tuple(self.fleet)),
            ('job', tuple(self.job)),
            ('algorithm_name', self.algorithm_cls.__name__),
            ('planning_uuid', self.planning.uuid)
        )
        self.assertEqual(expected, tuple(result))


if __name__ == '__main__':
    unittest.main()
