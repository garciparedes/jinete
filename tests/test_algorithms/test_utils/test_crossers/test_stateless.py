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
        self.assertEqual(job, dispatcher.job)
        self.assertEqual(fleet, dispatcher.fleet)
        self.assertEqual(len(job.trips), len(list(dispatcher.iterator)))

    def test_flush(self):
        job = jit.Job(generate_trips(10), objective_cls=jit.DialARideObjective)
        fleet = jit.Fleet(generate_vehicles(10))
        dispatcher = jit.StatelessCrosser(
            job=job,
            fleet=fleet,
        )
        self.assertNotIn('iterator', dispatcher.__dict__)
        list(dispatcher.iterator)
        self.assertIn('iterator', dispatcher.__dict__)
        dispatcher.flush()
        self.assertNotIn('iterator', dispatcher.__dict__)


if __name__ == '__main__':
    unittest.main()
