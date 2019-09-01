import unittest
from copy import deepcopy

import jinete as jit

from tests.utils import (
    generate_trips,
    generate_one_job,
)


class TestJob(unittest.TestCase):

    def test_construction(self):
        trips = generate_trips(3)
        objective_cls = jit.HashCodeObjective
        job = jit.Job(trips, objective_cls)

        self.assertIsInstance(job, jit.Job)
        self.assertEqual(job.trips, trips)
        self.assertEqual(job.objective_cls, objective_cls)

    def test_deepcopy(self):
        job = generate_one_job(True)
        copied_job = deepcopy(job)
        self.assertEqual(job, copied_job)


if __name__ == '__main__':
    unittest.main()
