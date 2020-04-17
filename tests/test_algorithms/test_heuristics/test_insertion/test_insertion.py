import unittest

import jinete as jit

from tests.utils import (
    generate_vehicles,
    generate_trips,
)


class TestInsertionAlgorithm(unittest.TestCase):
    job: jit.Job
    fleet: jit.Fleet

    @classmethod
    def setUpClass(cls) -> None:
        cls.job = jit.Job(generate_trips(10), objective_cls=jit.DialARideObjective)
        cls.fleet = jit.Fleet(generate_vehicles(10))

    def test_creation(self):
        algorithm = jit.InsertionAlgorithm(iterator_cls=jit.InsertionIterator, job=self.job, fleet=self.fleet,)
        self.assertEqual(algorithm.iterator_cls, jit.InsertionIterator)
        self.assertEqual(algorithm.job, self.job)
        self.assertEqual(algorithm.fleet, self.fleet)

    def test_optimize(self):
        algorithm = jit.InsertionAlgorithm(job=self.job, fleet=self.fleet,)
        result = algorithm.optimize()

        # TODO: Properly validate  behaviour of the provided "Result" object.
        self.assertIsNotNone(result)
        self.assertIsInstance(result, jit.Result)


if __name__ == "__main__":
    unittest.main()
