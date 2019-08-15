import unittest

import jinete as jit

from tests.utils import (
    generate_vehicles,
    generate_trips,
)


class TestStatelessCrosser(unittest.TestCase):

    def test_creation(self):
        job = jit.Job(generate_trips(10), objective_cls=jit.DialARideObjective)
        fleet = jit.Fleet(generate_vehicles(10))
        dispatcher = jit.StatelessCrosser(
            job=job,
            fleet=fleet,
        )
        self.assertEqual(dispatcher.job, job)
        self.assertEqual(dispatcher.fleet, fleet)


if __name__ == '__main__':
    unittest.main()
