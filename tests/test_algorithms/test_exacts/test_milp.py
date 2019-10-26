import unittest

import jinete as jit

from tests.utils import (
    generate_one_loader,
)


class TestMilpAlgorithm(unittest.TestCase):
    loader: jit.Loader

    @classmethod
    def setUpClass(cls) -> None:
        loader_cls = generate_one_loader()
        cls.loader = loader_cls()

    @property
    def job(self) -> jit.Job:
        return self.loader.job

    @property
    def fleet(self) -> jit.Fleet:
        return self.loader.fleet

    def test_creation(self):
        algorithm = jit.MilpAlgorithm(
            job=self.job,
            fleet=self.fleet,
        )
        self.assertEqual(algorithm.job, self.job)
        self.assertEqual(algorithm.fleet, self.fleet)

    def test_optimize(self):
        algorithm = jit.MilpAlgorithm(
            job=self.job,
            fleet=self.fleet,
        )
        result = algorithm.optimize()

        # TODO: Properly validate  behaviour of the provided "Result" object.
        self.assertIsNotNone(result)
        self.assertIsInstance(result, jit.Result)
        self.assertEqual(1, result.coverage_rate)
        self.assertAlmostEqual(85.4, result.optimization_function, delta=0.1)


if __name__ == '__main__':
    unittest.main()
