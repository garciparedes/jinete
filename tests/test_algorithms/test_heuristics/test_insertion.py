import unittest

import jinete as jit

from tests.utils import (
    generate_vehicles,
    generate_trips,
)


class TestInsertionAlgorithm(unittest.TestCase):

    def test_creation(self):
        job = jit.Job(generate_trips(10), objective_cls=jit.DialARideObjective)
        fleet = jit.Fleet(generate_vehicles(10))
        dispatcher = jit.InsertionAlgorithm(
            jit.Crosser,
            job=job,
            fleet=fleet,
        )
        self.assertEqual(dispatcher.crosser_cls, jit.Crosser)
        self.assertEqual(dispatcher.job, job)
        self.assertEqual(dispatcher.fleet, fleet)


if __name__ == '__main__':
    unittest.main()
