import unittest

import jinete as jit

from tests.utils import (
    generate_vehicles,
    generate_trips,
)


class TestRandomizedCrosser(unittest.TestCase):

    def test_creation(self):
        job = jit.Job(generate_trips(10))
        fleet = jit.Fleet(generate_vehicles(10))
        randomized_size = 2
        dispatcher = jit.RandomizedCrosser(
            randomized_size=randomized_size,
            job=job,
            fleet=fleet,
        )
        self.assertEqual(dispatcher.randomized_size, randomized_size)
        self.assertEqual(dispatcher.job, job)
        self.assertEqual(dispatcher.fleet, fleet)


if __name__ == '__main__':
    unittest.main()
