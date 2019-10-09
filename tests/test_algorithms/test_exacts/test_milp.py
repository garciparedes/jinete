import unittest
from pathlib import Path

import jinete as jit


class TestMilpAlgorithm(unittest.TestCase):
    job: jit.Job
    fleet: jit.Fleet
    initial: jit.Result

    @classmethod
    def setUpClass(cls) -> None:
        file_path = Path(__file__).parents[2] / 'res' / 'problem-4.txt'

        class MyLoader(jit.FileLoader):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    file_path=file_path,
                    formatter_cls=jit.CordeauLaporteLoaderFormatter,
                    *args, **kwargs,
                )

        cls.loader = MyLoader()

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
